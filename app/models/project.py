from tortoise.models import Model
from tortoise import fields


class Project(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    api_token = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="projects")
