from flask import Flask, request
from markupsafe import escape
from ConfigFileManager import ConfigFileManager

app = Flask(__name__)

@app.route("/bluetooth/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        config_file_manager = ConfigFileManager()

        capability = request.args.get("capability", "KeyboardOnly")
        config_file_manager.set_config_value("Bluetooth", "capability", capability)


        return("Config saved.")
    else:
        config_file_manager = ConfigFileManager()

        return {
            "capability": config_file_manager.capability
        }
