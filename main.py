from flask import Flask, request, jsonify
from flask_cors import CORS
from ConfigFileManager import ConfigFileManager
import dbus

app = Flask(__name__)
CORS(app)

@app.route("/bluetooth/settings/", methods=["GET", "POST"])
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
                # If it's a timeout key and the value is an empty string, treat it as "0"
                if key in ["discoverable_timeout", "pairable_timeout"] and value == "":
                    value = "0"
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

@app.route("/bluetooth/paired_devices")
def list_devices():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                             "org.freedesktop.DBus.ObjectManager")
    objects = manager.GetManagedObjects()
    devices = []

    for path, interfaces in objects.items():
        if "org.bluez.Device1" in interfaces:
            device = interfaces["org.bluez.Device1"]
            if device.get("Paired", False):
                devices.append({
                    "name": str(device.get("Name", "Unknown")),
                    "address": str(device.get("Address")),
                    "connected": bool(device.get("Connected", False)),
                    "trusted": bool(device.get("Trusted", False)),
                })
    return jsonify(devices)
