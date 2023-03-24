from django.db import models


class ImportFromFile:

    def __init__(self, model: models.Model, file: object):
        self.model = model
        self.file = file
