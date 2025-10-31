import logging
import sys
import os
from pathlib import Path
import configparser

class ConfigFileManager:
    config_path = "~/.config/hifiberry/bluetooth.conf"
    config_path = Path(config_path).expanduser()

    def __init__(self):
        # Set up logger
        self.logger = logging.getLogger("hbos-bluetooth-service")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info("Initializing ConfigFileManager...")


        self.config_file = Path(self.config_path)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self.create_config_file()

        self.load_config_values()

    def create_config_file(self):
        try:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # Create the file
            with open(self.config_path, "w") as f:
                f.write("[Bluetooth]\n")
                f.write("capability=NoInputNoOutput\n")
            self.logger.info(f"Created config file: {self.config_path}")

        except Exception as e:
            self.logger.error(f"Error creating config file: {e}")

    def load_config_values(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.capability = self.config.get("Bluetooth", "capability", fallback="KeyboardDisplay")
        self.logger.info(f"Bluetooth capability: {self.capability}")
