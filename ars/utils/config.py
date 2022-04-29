import yaml


class ConfigLoader:
    _path = None
    _config = None

    @staticmethod
    def set_path(path):
        ConfigLoader._path = path

    @staticmethod
    def get_path():
        return ConfigLoader._path
        
    @staticmethod
    def load():
        with open(ConfigLoader._path, "r") as f:
            ConfigLoader._config = yaml.safe_load(f)
        return ConfigLoader._config
    
    @staticmethod
    def get():
        return ConfigLoader._config

    @staticmethod
    def set(config):
        ConfigLoader._config = config
