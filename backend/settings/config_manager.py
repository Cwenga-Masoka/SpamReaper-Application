import json
import os

CONFIG_FILE = "config.json"

_config_cache = None


def load_config() -> dict:
    """
    Reads config.json and returns all the settings as a python dictionary.
    Only reads from disk once per app run — after that, serves from the
    in-memory cache. If the file is missing or broken, it returns a set
    of safe default values so the app never crashes just because of a
    bad config file (and doesn't cache the defaults, so a future call
    will retry reading the real file instead of getting stuck).
    """
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    # Check if the config file exists
    if not os.path.exists(CONFIG_FILE):

        #if it does not exist we log a warning and return defaults
        print(f"Warning: {CONFIG_FILE} not found using default settings.")
        return get_default_config()
    try:
        # We open the file in read mode ('r')
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:

            #json.load() reads the file and converts it into a python dictionary
            config = json.load(f)
            _config_cache = config
            return _config_cache

    except json.JSONDecodeError as e:
        # Will happen if the JSON file has a syntax error
        # The user is warned and the defaults are sed instead of crashing
        print(f"Config file has syntax error: {e}. Using default settings.")
        return get_default_config()

    
def get_default_config() -> dict:
    """
    This resturns a hardcoded set of default settings.
    This is the fallback to prevent the app from crashing
    if config.json is broken or missing
    """
    return{
        "days_before_deletion": 5,
        "scan_interval_hours": 24,
        "max_notification_previews": 3,
        "spam_keywords": [
            "winner", "won", "prize", "claim", "free", "urgent",
            "click here", "limited time", "offer", "congratulations",
            "verify your account", "suspended", "unusual activity",
            "OTP", "one time pin", "lucky draw", "selected",
            "cash prize", "risk free", "act now", "expires today",
            "loan approved", "debt relief", "you have been chosen", 
            "SASSA approved", "airtime reward", "airtime giveaway",
            "data bundle", "data giveaway", "data reward", "data prize",
            "absa", "fnb", "standard bank", "nedbank", "capitec"
        ],
        "auto_delete_enabled": True,
        "notification_enabled": True,
        "database_name": "spamreaper.db"
    }

def get_setting(key: str):
    """
    This is a convinience function that fetches a settin by its key name
    """
    #Load the full config first
    config = load_config()

    return config.get(key, None)


def get_setting_or_default(key: str):
    """
    Returns the saved value of a setting. If the key is not saved in
    config.json, returns the built-in default for that key instead.
    """
    saved_value = get_setting(key)
    if saved_value is not None:
        return saved_value
    return get_default_config()[key]


def save_setting(key: str, value) -> bool:
    """
    This function updates a single setting in config.json and saves it
    Returns True if saved successfully and False otherwise
    """
    global _config_cache

    try:
        config = load_config()

        config[key]= value

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:

            #json.dump() converst the dictionary back to a JSON file
            json.dump(config, f, indent=4)

        # Keep the in-memory cache in sync so the change is reflected
        # immediately, without waiting for the next disk read
        _config_cache = config

        print(f"Setting '{key}' updated to '{value}'.")
        return True

    except Exception as e:
        print(f"Failed to save setting '{key}': {e}")
        return False