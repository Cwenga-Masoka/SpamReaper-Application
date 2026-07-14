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

from urllib.parse import urlencode, urlparse, parse_qs

# --- Shared OAuth endpoints ---
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
SCOPE = 'https://www.googleapis.com/auth/gmail.modify'

# --- Android (custom scheme) OAuth client ---
ANDROID_CLIENT_ID = "333363023305-81uj8iv498rcgjakf1dc2ocu3vi5bn80.apps.googleusercontent.com"
ANDROID_REDIRECT_URI = "com.cwengamasoka.spamreaper:/oauth2redirect"

# --- Desktop (loopback) OAuth client ---
CREDENTIALS_FILE = 'client_secret.json'
REDIRECT_PORT = 8765
REDIRECT_URI = f'http://127.0.0.1:{REDIRECT_PORT}'


def open_url_natively(url):
    """Opens a URL using Android's native browser intent, forcing it into our task."""
    print(f"[OAuth] open_url_natively called, platform={platform.system()}")
    if platform.system() == 'Linux':
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            activity = PythonActivity.mActivity
            activity.startActivity(intent)
            print("[OAuth] Native intent startActivity() called successfully")
        except Exception as e:
            print(f"[OAuth] Failed to open native intent: {e}")
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


def load_client_credentials():
    """
    Reads client_secret.json (the Desktop-type OAuth client) and pulls
    out the client_id and client_secret — used only on the desktop
    loopback path, since the Android client doesn't use a secret.
    """
    with open(CREDENTIALS_FILE, 'r') as f:
        data = json.load(f)
    client_info = data['installed']
    return client_info['client_id'], client_info['client_secret']


def save_token(token_data):
    """
    Saves our token information to a local JSON file so we don't
    need to log in every time the app starts. Also records which
    platform the token was obtained under, so get_access_token()
    knows which credentials to use when refreshing later.
    """
    token_data['saved_at'] = time.time()
    token_data['obtained_on'] = platform.system()
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


# --- Android: custom-scheme flow ---

def get_authorization_url_android():
    """
    Builds the Google OAuth URL for Android using the Android client ID
    and custom scheme redirect URI. No local server needed — Android
    intercepts the redirect via the intent filter.
    """
    params = {
        'client_id': ANDROID_CLIENT_ID,
        'redirect_uri': ANDROID_REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPE,
        'access_type': 'offline',
        'prompt': 'consent'
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    print(f"[OAuth] Built Android auth URL: {url}")
    return url


def exchange_code_for_tokens_android(auth_code):
    """
    Exchanges the authorization code for tokens on Android.
    No client_secret needed — Android OAuth clients are verified
    by SHA-1 fingerprint, not a secret.
    """
    print(f"[OAuth] Exchanging Android auth code: {auth_code[:10]}...")
    payload = {
        'client_id': ANDROID_CLIENT_ID,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': ANDROID_REDIRECT_URI,
        'code_verifier': ''
    }

    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code != 200:
        print(f"[OAuth] Token exchange failed: {response.status_code} {response.text}")
    response.raise_for_status()
    return response.json()


# --- Desktop: loopback server flow ---

from http.server import HTTPServer, BaseHTTPRequestHandler


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    A tiny web server that does ONE job: catch the redirect Google
    sends back after the user logs in, grab the authorization code
    from the URL, and store it so our main code can read it.
    """
    received_code = None

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if 'code' in query_params:
            OAuthCallbackHandler.received_code = query_params['code'][0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h2>Login successful!</h2>"
                          b"<p>You can close this tab and return to SpamReaper.</p>"
                          b"</body></html>")

    def log_message(self, format, *args):
        pass


def get_authorization_code(client_id):
    """
    Desktop-only. Opens a browser for the user to log in, starts a tiny
    local web server to catch Google's redirect, and returns the
    resulting authorization code.
    """
    params = {
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPE,
        'access_type': 'offline',
        'prompt': 'consent'
    }

    full_url = f"{AUTH_URL}?{urlencode(params)}"

    server = HTTPServer(('127.0.0.1', REDIRECT_PORT), OAuthCallbackHandler)
    server.timeout = 120  # give up after 2 minutes instead of blocking forever
    server.socket.settimeout(None)

    print("[OAuth] Opening browser for Google login (Desktop)...")
    open_url_natively(full_url)

    print("[OAuth] Waiting for you to complete login in the browser...")
    server.handle_request()

    auth_code = OAuthCallbackHandler.received_code

    if auth_code is None:
        raise Exception("Login timed out or was cancelled — please try again.")

    return auth_code


def exchange_code_for_tokens(client_id, client_secret, auth_code):
    """
    Desktop-only. Trades the authorization code for tokens using the
    Desktop client's secret.
    """
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()


# --- Unified entry points, branching by platform ---

def start_login_flow():
    """
    Stage 1 of login.
    - Android: opens the browser with the Android OAuth URL and returns
      immediately — the auth code arrives later via on_new_intent.
    - Desktop: runs the full loopback server flow, blocking until the
      code is received, and returns it directly.
    """
    token_data = load_token()

    if token_data is not None:
        return None

    print("No saved login found. Starting login flow...")

    if platform.system() == "Linux":
        url = get_authorization_url_android()
        print("[OAuth] Opening browser (Android)...")
        open_url_natively(url)
        return "ANDROID_PENDING"
    else:
        client_id, client_secret = load_client_credentials()
        auth_code = get_authorization_code(client_id)
        return auth_code


def finish_login_flow(auth_code):
    """
    Stage 2 of login.
    - Android: exchanges the code using the Android client (no secret).
    - Desktop: exchanges the code using the Desktop client (with secret).
    """
    if platform.system() == "Linux":
        print("[OAuth] Finishing login (Android)...")
        token_data = exchange_code_for_tokens_android(auth_code)
    else:
        print("[OAuth] Finishing login (Desktop)...")
        client_id, client_secret = load_client_credentials()
        token_data = exchange_code_for_tokens(client_id, client_secret, auth_code)

    save_token(token_data)
    print("[OAuth] Login completed and token saved.")
    return token_data['access_token']


def refresh_access_token(client_id, refresh_token, client_secret=None):
    """
    Access tokens expire after about an hour. Instead of making the
    user log in again every hour, we use the refresh_token (which
    lasts much longer) to silently get a brand new access_token.
    client_secret is optional — the Android client doesn't use one,
    and omitting the key entirely (rather than sending it as None)
    is what Google expects in that case.
    """
    payload = {
        'client_id': client_id,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    if client_secret:
        payload['client_secret'] = client_secret

    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()


def get_access_token():
    """
    The main function other files call to get a valid access token.
    Refreshes use whichever client the token was originally obtained
    under, recorded in the saved token file via 'obtained_on'.
    """
    token_data = load_token()

    if token_data is None:
        raise Exception("Not logged in yet — please connect your Gmail account first.")

    age = time.time() - token_data['saved_at']

    if age < (token_data['expires_in'] - 60):
        return token_data['access_token']

    print("Access token expired. Refreshing...")

    obtained_on = token_data.get('obtained_on', platform.system())

    if obtained_on == "Linux":
        new_token_data = refresh_access_token(ANDROID_CLIENT_ID, token_data['refresh_token'])
    else:
        client_id, client_secret = load_client_credentials()
        new_token_data = refresh_access_token(
            client_id, token_data['refresh_token'], client_secret
        )

    new_token_data['refresh_token'] = token_data['refresh_token']
    save_token(new_token_data)
    return new_token_data['access_token']