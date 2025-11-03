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


@app.route("/bluetooth/unpair", methods=["POST"])
def unpair_device():
    """
    Unpair a Bluetooth device by its address.
    Expects a POST request with query parameter: ?address=XX:XX:XX:XX:XX:XX
    """
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Missing 'address' query parameter"}), 400

    address = address.upper()
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                             "org.freedesktop.DBus.ObjectManager")
    objects = manager.GetManagedObjects()

    # Find the device object path and its adapter
    for path, interfaces in objects.items():
        if "org.bluez.Device1" in interfaces:
            device = interfaces["org.bluez.Device1"]
            if device.get("Address", "").upper() == address:
                # Find the adapter this device belongs to
                adapter_path = "/".join(path.split("/")[:-1])
                adapter_obj = dbus.Interface(bus.get_object("org.bluez", adapter_path),
                                             "org.bluez.Adapter1")
                try:
                    adapter_obj.RemoveDevice(path)
                    return jsonify({"status": "unpaired", "address": address})
                except dbus.exceptions.DBusException as e:
                    return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Device not found"}), 404
