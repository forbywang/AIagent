import tornado.web
import jwt
import time
import json
from db.User import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        token = self.get_secure_cookie("token")
        if token is None:
            return None
        try:
            payload = jwt.JWT.decode(token, self.application.secret_key, algorithms=['HS256'])
            return payload
        except:
            return None
        
class LoginWithMobileHandler(tornado.web.RequestHandler):
    async def post(self):
        body = json.loads(self.request.body)
        mobile = body.get('mobile')
        code = body.get('code')
        if mobile is None or code is None:
            self.write({'code': 400, 'msg': '参数错误'})
            return
        redis = self.application.redis
        if redis is None:
            self.write({'code': 500, 'msg': '服务器错误'})
            return

        redisCode = await redis.get(mobile)
        if redisCode is None:
            self.write({'code': 400, 'msg': '验证码已过期'})
            return

        if redisCode != code:
            self.write({'code': 400, 'msg': '验证码错误'})
            return
        
        user = await User.filter(phone=mobile).first()
        if user is None:
            userName = '用户' + mobile[-4:]
            user = await User.create(phone=mobile, username=userName)
        payload = {
            'id': user.id,
            'mobile': user.phone,
            'username': user.username,
            'iat': int(time.time()),
        }
        token = jwt.JWT.encode(payload, self.application.secret_key, algorithm='HS256')
        self.set_secure_cookie('token', token)
        self.write({'code': 200, 'msg': '登录成功'})


        
class UserUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    async def post(self):
        body = json.loads(self.request.body)
        nickName = body.get('nickName')
        avatarUrl = body.get('avatarUrl')
        if nickName is None or avatarUrl is None:
            self.write({'code': 400, 'msg': '参数错误'})
            return
        userId = self.current_user.get('id')
        user = await User.filter(id=userId).first()
        if user is None:
            self.write({'code': 400, 'msg': '用户不存在'})
            return
        if nickName is not None:
            user.username = nickName
        if avatarUrl is not None:
            user.avatar = avatarUrl
        await user.save()
        self.write({'code': 200, 'msg': '更新成功'})

        
