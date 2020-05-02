import json
import os

from mongoengine import EmbeddedDocument
from mongoengine import Document
from mongoengine import StringField, EmbeddedDocumentListField
from .scenario import Scenario
from .result import Result


class TestSuite(Document):
    name = StringField(max_length=128, required=True)
    scenarios = EmbeddedDocumentListField(Scenario)

    def run(self):
        data = []
        result = True
        for scenario in self.scenarios:
            scenario.run()
            result = scenario.result.result
            if result is False:
                data.append(scenario.result.data)

        if data:
            result = False

        response_result = Result(result=result, data=data)
        return response_result

    def from_folder(self, directory):
        file_names = os.listdir(directory)

        for file_name in file_names:
            file_path = os.path.join(directory, file_name)
            with open(file_path, "r") as file:
                scenario = Scenario.from_json(file.read())
                self.scenarios.append(scenario)


