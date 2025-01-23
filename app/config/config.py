import json
import os
import threading
from collections import UserDict


class AppConfig(UserDict):
    _instance = None
    _lock = threading.Lock()  # 增加线程安全

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, main_path=""):
        if hasattr(self.__dict__, "_initialized"):  # Check if already initialized
            return
        self._initialized = True
        self.main_path = main_path
        self.config_file = os.path.join(main_path, "app/config/config.json")
        self.data = {}  # Initialize data
        self._ensure_config_file()
        self.load_config()
        
        print("加载配置管理器成功")
        
        
    def _ensure_config_file(self):
        """Ensures the config file and directories exist."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        """Creates a default configuration."""
        self.data = {
            "Theme": {"mode": "dark", "color": "ft.Colors.BLUE", "background_image": "images/backgrounds/background1.jpg"},
            "Window": {
                "width": 1300,
                "height": 800,
                "min_width": 500,
                "min_height": 400,
                "font": {
                    "windows": [
                        "Segoe UI",
                        "Microsoft YaHei UI",
                        "Arial",
                    ],
                    "macos": [
                        "SF Pro",
                        "Helvetica Neue",
                        "PingFang SC",
                        "Hiragino Sans GB",
                    ],
                    "linux": [
                        "Ubuntu",
                        "Noto Sans CJK SC",
                        "DejaVu Sans",
                    ],
                },
            },
            "App": {"title": "PyDracula"}
        }
        self.save_config()

    def load_config(self):
        """Loads the configuration from the file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_default_config()

    def save_config(self):
        """Saves the current configuration to the file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get(self, section, key, default=None):
        """Retrieves a configuration value."""
        return self.data.get(section, {}).get(key, default)

    def set(self, section, key, value):
        """Sets a configuration value and saves it."""
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.save_config()

    def __getattr__(self, item):
        """Dynamic attribute access from the config data."""
        if item in self.__dict__:  # Check if it's an instance attribute first
            return self.__dict__[item]
        for section, settings in self.data.items():
            if item in settings:
                return settings[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        """Dynamic attribute setting and updating config."""
        if key in ['data', '_initialized', 'config_file', 'main_path']:  # Exempt internal attributes
            super().__setattr__(key, value)
        else:
            print(f"Setting {key} to {value}")
            self.set("App", key, value)
            raise AttributeError("Cannot set attributes directly. Use 'set' method instead.")

    def add_section(self, section):
        """Adds a new section to the config if it doesn't exist."""
        if section not in self.data:
            self.data[section] = {}
            self.save_config()

    def remove_section(self, section):
        """Removes a section from the config if it exists."""
        if section in self.data:
            del self.data[section]
            self.save_config()

    def config_sections(self):
        """Returns a list of all section names in the config."""
        return list(self.data.keys())
