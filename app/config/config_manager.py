import configparser
import os

class ConfigManager:
    def __init__(self, config_file="app/config/config.ini", main_path=""):
        self.config_file = os.path.join(main_path, config_file)
        print(self.config_file)
        self.config = configparser.ConfigParser()
        self._ensure_config_file()
        self.load()

    def _ensure_config_file(self):
        """确保配置文件和目录存在"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        """创建默认配置"""
        self.config["Theme"] = {
            "mode": "dark",
        }
        self.config["Window"] = {
            "width": "1300",
            "height": "800",
            "min_width": "500",
            "min_height": "400",
        }
        self.config["App"] = {
            "title": "PyDracula",
        }
        self.save()

    def load(self):
        """加载配置"""
        self.config.read(self.config_file, encoding='utf-8')

    def save(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def get(self, section, key, fallback=None):
        """获取配置值"""
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        """设置配置值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save() 