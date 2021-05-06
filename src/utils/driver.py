from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Driver(webdriver.Chrome):
    @classmethod
    def initialize(cls, target_dir=""):
        options = Options()
        if target_dir:
            prefs = {
                "download.default_directory": target_dir
            }
            options.add_experimental_option('prefs', prefs)
        setattr(cls, 'download_directory', target_dir)
        return cls(ChromeDriverManager().install(), options=options)