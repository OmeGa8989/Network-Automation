import yaml
import os

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise Exception(f"Error parsing YAML: {exc}")

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value
