from flask import Flask, request
from markupsafe import escape
from ConfigFileManager import ConfigFileManager

app = Flask(__name__)

@app.route("/bluetooth/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        name = request.args.get("capability", "KeyboardOnly")
        return(f"capability: {escape(name)}")
    else:
        config_file_manager = ConfigFileManager()
        return {
            "capability": config_file_manager.capability
        }
