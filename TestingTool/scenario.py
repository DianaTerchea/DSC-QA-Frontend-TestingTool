import json

from os import path
from mongoengine import EmbeddedDocument
from mongoengine import StringField, EmbeddedDocumentListField
from .task import Task
from .result import Result
from selenium import webdriver


class Scenario(EmbeddedDocument):
    name = StringField(max_length=128, required=True)
    url = StringField(max_length=512, required=True)
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
        if driver_type == "Firefox":
            driver = webdriver.Firefox(executable_path=driver_path)
        elif driver_type == "Chrome":
            driver = webdriver.Chrome(executable_path=driver_path)
        else:
            raise Exception("Invalid type of path")
        driver.maximize_window()
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
