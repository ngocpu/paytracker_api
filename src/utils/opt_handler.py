class OptionHandler:
    def __init__(self):
        self.options = {}

    def set_option(self, key: str, value: str):
        self.options[key] = value

    def get_option(self, key: str) -> str:
        return self.options.get(key, "")

    def get_all_options(self) -> dict:
        return self.options
