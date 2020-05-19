import configparser

class MyConfig:

    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self._config_path = config_path
        self._wordlib_path = self.config.get("Path", "wordlib_path")
        self._wordlist_path = self.config.get("Path", "wordlist_path")
        self._country = self.config.get("Detail", "country")
        self._margin = self.config.getfloat("Detail", "margin")
        self._default_wordlist_name = self.config.get("Wordlist", "default_wordlist_name")
        self._max_number = self.config.getint("Wordlist", "maximum_number_of_words_in_each_group")

    def _save(self):
        with open(self._config_path, "w+") as f:
            self.config.write(f)
    
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        self._country = value
        self.config.set("Detail", "country", value)
        self._save()

    @property
    def max_number(self):
        return self._max_number

    @property
    def wordlib_path(self):
        return self._wordlib_path
    
    @property
    def wordlist_path(self):
        return self._wordlist_path
    
    @property
    def default_wordlist_name(self):
        return self._default_wordlist_name
    
    @default_wordlist_name.setter
    def default_wordlist_name(self, value):
        self._default_wordlist_name = value
        self.config.set("Wordlist", "default_wordlist_name", value)
        self._save()

    @property
    def margin(self):
        return self._margin
    
    @margin.setter
    def margin(self, value):
        self._margin = value
        self.config.set("Detail", "margin", str(value))
        self._save()
