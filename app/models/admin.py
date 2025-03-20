from tortoise.models import Model
from tortoise import fields

class AdminApplication(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="applications")
    reason = fields.TextField()
    status = fields.CharField(max_length=20, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)
    reviewed_at = fields.DatetimeField(null=True)