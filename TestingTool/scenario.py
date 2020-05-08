import json

from os import path
from mongoengine import EmbeddedDocument, BooleanField
from mongoengine import StringField, EmbeddedDocumentListField
from .task import Task
from .result import Result
from selenium import webdriver


class Scenario(EmbeddedDocument):
    name = StringField(max_length=128, required=True)
    url = StringField(max_length=512, required=True)
    mobile_mode = BooleanField(default=False)
    tasks = EmbeddedDocumentListField(Task)

    def run(self):
        if not path.exists("./TestingTool/config.json"):
            raise Exception("File config.json doesn't exist")
        with open("./TestingTool/config.json", "r") as file:
            config_json_data = json.loads(file.read())
        driver_path = config_json_data.get("selenium_driver_path")
        driver_type = config_json_data.get("selenium_driver_type")
        if driver_path is None:
            raise Exception("You didnt give me a selenium_driver_path")
        if self.mobile_mode is False:
            if driver_type == "Firefox":
                driver = webdriver.Firefox(executable_path=driver_path)
            elif driver_type == "Chrome":
                driver = webdriver.Chrome(executable_path=driver_path)
            else:
                raise Exception("Invalid driver type")
        else:
            if driver_type == "Firefox":
                user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) " \
                             "AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", user_agent)
                driver = webdriver.Firefox(firefox_profile=profile, executable_path=driver_path)
                driver.set_window_size(414, 736)
            elif driver_type == "Chrome":
                mobile_emulation = {"deviceName": "Pixel 2"}
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                driver = webdriver.Chrome(
                    executable_path=driver_path, desired_capabilities=chrome_options.to_capabilities())
            else:
                raise Exception("Invalid driver type")
        # driver.maximize_window()
        data = []
        result = True
        for task in self.tasks:
            task.run(driver)
            result = task.result.result
            if result is False:
                data.append(task.result.data)
                break
        if data:
            result = False
        response_result = Result(result=result, data=data)
        driver.close()
        return response_result
