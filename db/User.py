from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk = True)
    username = fields.CharField(max_length = 128)
    email = fields.CharField(max_length = 100)
    phone = fields.CharField(max_length = 20)
    password = fields.CharField(max_length = 128)
    openid = fields.CharField(max_length = 128)
    unionid = fields.CharField(max_length = 128)
    avatar = fields.CharField(max_length = 255)
    opentype = fields.SmallIntField(default = 0) # 0: 手机号登录 1:微信登录 2:QQ登录 3:微博登录
    status = fields.SmallIntField(default = 1)
    bitmap = fields.IntField(default = 0)
    remark = fields.CharField(max_length = 255)
    created_at = fields.DatetimeField(auto_now_add = True)
    updated_at = fields.DatetimeField(auto_now = True)

    class Meta:
        table = "users"