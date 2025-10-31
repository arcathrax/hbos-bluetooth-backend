from flask import Flask, request
from flask_cors import CORS
from markupsafe import escape
from ConfigFileManager import ConfigFileManager

app = Flask(__name__)
CORS(app)

@app.route("/bluetooth/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        config_file_manager = ConfigFileManager()

        capability = request.args.get("capability", "KeyboardOnly")
        config_file_manager.set_config_value("Bluetooth", "capability", capability)

        return {
            "capability": config_file_manager.capability,
            "discoverable": config_file_manager.discoverable,
            "discoverableTimeout": config_file_manager.discoverable_timeout,
            "pairable": config_file_manager.pairable,
            "pairableTimeout": config_file_manager.pairable_timeout,
        }
    else:
        config_file_manager = ConfigFileManager()

        return {
            "capability": config_file_manager.capability,
            "discoverable": config_file_manager.discoverable,
            "discoverableTimeout": config_file_manager.discoverable_timeout,
            "pairable": config_file_manager.pairable,
            "pairableTimeout": config_file_manager.pairable_timeout,
        }
