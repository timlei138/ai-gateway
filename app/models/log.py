from tortoise.models import Model
from tortoise import fields


class APICallLog(Model):
    id = fields.IntField(pk=True)
    project = fields.ForeignKeyField("models.Project")
    created_at = fields.DatetimeField(auto_now_add=True)
    duration = fields.FloatField()
    input_tokens = fields.IntField()
    output_tokens = fields.IntField()
