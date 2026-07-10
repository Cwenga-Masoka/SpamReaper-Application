# requests lets us make HTTP calls — GET, POST, etc — to any web address
import requests

# json lets us read our saved credentials file and save our token to disk
import json

# os lets us check if files exist
import os

# time lets us check if our saved token has expired, and pace our polling
import time

# platform lets us detect Android vs Desktop for storage paths
import platform

# The credentials file downloaded from the "TVs and Limited Input devices"
# OAuth client in Google Cloud Console
DEVICE_CREDENTIALS_FILE = 'device_client_secret.json'


def open_url_natively(url):
    """
    Opens a URL using Android's native browser intent — purely a
    convenience so the user doesn't have to type google.com/device
    by hand. On Desktop, just opens the default browser.
    """
    if platform.system() == 'Linux':  # Kivy on Android identifies as Linux
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            activity = PythonActivity.mActivity
            activity.startActivity(intent)
        except Exception as e:
            print(f"Failed to open native intent: {e}")
            import webbrowser
            webbrowser.open(url)
    else:
        import webbrowser
        webbrowser.open(url)


def get_storage_path():
    """
    Returns a reliable, persistent folder to store our files in.
    On Android, uses Android's native Context API via Pyjnius to get
    the app's internal files directory. On PC, just uses the current folder.
    """
    if platform.system() == "Linux":
        try:
            from jnius import autoclass  # type: ignore

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            files_dir = activity.getFilesDir().getAbsolutePath()
            return files_dir

        except Exception as e:
            print(f"Could not get Android files dir: {e}")
            return '.'
    else:
        return '.'


TOKEN_FILE = f'{get_storage_path()}/gmail_token.json'

# The permission scope we're asking for
SCOPE = 'https://www.googleapis.com/auth/gmail.modify'

# Google's OAuth endpoints for the device flow
DEVICE_CODE_URL = 'https://oauth2.googleapis.com/device/code'
TOKEN_URL = 'https://oauth2.googleapis.com/token'


def load_device_client_credentials():
    """
    Reads device_client_secret.json (downloaded from the "TVs and Limited
    Input devices" OAuth client in Cloud Console) and pulls out the
    client_id and client_secret we need to talk to Google.
    """
    with open(DEVICE_CREDENTIALS_FILE, 'r') as f:
        data = json.load(f)

    # Handles both possible download shapes — nested under "installed"
    # (like Desktop-type downloads) or flat at the top level
    client_info = data.get('installed', data)
    return client_info['client_id'], client_info['client_secret']


def save_token(token_data):
    """
    Saves our token information to a local JSON file so we don't
    need to log in every time the app starts.
    """
    token_data['saved_at'] = time.time()
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f)
    except Exception as e:
        raise


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return None


def request_device_code(client_id):
    """
    Asks Google for a device code — this is step one of the device flow.
    """
    payload = {'client_id': client_id, 'scope': SCOPE}
    response = requests.post(DEVICE_CODE_URL, data=payload)

    if response.status_code != 200:
        print(f"Device code request failed: {response.status_code} {response.text}")

    response.raise_for_status()
    return response.json()

def poll_for_token(client_id, client_secret, device_code, interval, expires_in):
    """
    Repeatedly asks Google "has the user approved yet?" every `interval`
    seconds, until they approve, the code expires, or they deny it.
    This replaces the old local server — instead of waiting for an
    incoming connection, we just make outgoing requests, which Android
    doesn't throttle the way it throttles inbound sockets.
    """
    elapsed = 0
    while elapsed < expires_in:
        time.sleep(interval)
        elapsed += interval

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }
        response = requests.post(TOKEN_URL, data=payload)
        data = response.json()

        if response.status_code == 200:
            return data

        error = data.get('error')
        if error == 'authorization_pending':
            continue
        elif error == 'slow_down':
            interval += 5
            continue
        elif error == 'access_denied':
            raise Exception("Login was denied.")
        elif error == 'expired_token':
            raise Exception("Login code expired — please try again.")
        else:
            raise Exception(f"Login failed: {error or 'unknown error'}")

    raise Exception("Login timed out — please try again.")


def start_device_login_flow():
    """
    Stage 1: requests a device code from Google. Returns the full
    response dict — the caller shows device_data['user_code'] and
    device_data['verification_url'] to the user, then passes this
    same dict into complete_device_login_flow() to finish up.
    """
    client_id, client_secret = load_device_client_credentials()
    return request_device_code(client_id)


def complete_device_login_flow(device_data):
    """
    Stage 2: polls Google until the user enters the code and approves,
    then saves the resulting tokens.
    """
    client_id, client_secret = load_device_client_credentials()
    token_data = poll_for_token(
        client_id, client_secret,
        device_data['device_code'],
        device_data.get('interval', 5),
        device_data.get('expires_in', 1800)
    )
    save_token(token_data)
    print("Login completed and token saved.")
    return token_data['access_token']


def refresh_access_token(client_id, client_secret, refresh_token):
    """
    Access tokens expire after about an hour. Instead of making the
    user log in again every hour, we use the refresh_token (which
    lasts much longer) to silently get a brand new access_token.
    """
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()


def get_access_token():
    """
    The main function other files call to get a valid access token.
    Assumes login has already happened via the device flow above.
    """
    client_id, client_secret = load_device_client_credentials()
    token_data = load_token()

    if token_data is None:
        raise Exception("Not logged in yet — please connect your Gmail account first.")

    age = time.time() - token_data['saved_at']

    if age < (token_data['expires_in'] - 60):
        return token_data['access_token']
    else:
        print("Access token expired. Refreshing...")
        new_token_data = refresh_access_token(
            client_id, client_secret, token_data['refresh_token']
        )
        new_token_data['refresh_token'] = token_data['refresh_token']
        save_token(new_token_data)
        return new_token_data['access_token']