from flask import Flask, request
from flask_cors import CORS
from ConfigFileManager import ConfigFileManager

app = Flask(__name__)
CORS(app)

@app.route("/bluetooth/", methods=["GET", "POST"])
def bluetooth():
    config_file_manager = ConfigFileManager()

    if request.method == "POST":
        # Define allowed keys
        valid_keys = [
            "capability",
            "discoverable",
            "discoverable_timeout",
            "pairable",
            "pairable_timeout",
        ]

        # Iterate through provided args and update only those that exist
        for key in valid_keys:
            if key in request.args:
                value = request.args.get(key)
                config_file_manager.set_config_value("Bluetooth", key, value)

        return {
            "capability": config_file_manager.capability,
            "discoverable": config_file_manager.discoverable,
            "discoverableTimeout": config_file_manager.discoverable_timeout,
            "pairable": config_file_manager.pairable,
            "pairableTimeout": config_file_manager.pairable_timeout,
        }

    # For GET, just return the current config
    return {
        "capability": config_file_manager.capability,
        "discoverable": config_file_manager.discoverable,
        "discoverableTimeout": config_file_manager.discoverable_timeout,
        "pairable": config_file_manager.pairable,
        "pairableTimeout": config_file_manager.pairable_timeout,
    }

