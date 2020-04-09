import json

from mongoengine import EmbeddedDocument
from mongoengine import StringField, DictField, BooleanField, EmbeddedDocumentField
from .result import Result
from .actions import ACTION_LIST


class Task(EmbeddedDocument):
    name = StringField(max_length=128, required=True)
    action = StringField(max_length=128, required=True)
    args = DictField()
    reverse_result = BooleanField(default=False)
    result = EmbeddedDocumentField(Result)


def run(self, browser_instance):
    data = DictField()
    result = BooleanField()
    for key in ACTION_LIST:
        if key == self.action:
            result, data = ACTION_LIST[key](self.args, browser_instance)
        if self.reverse_result:
            self.result = Result(not result, data)
        else:
            self.result = Result(result, data)
