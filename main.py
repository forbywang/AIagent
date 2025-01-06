from handler.UserHandler import LoginWithMobileHandler, UserUpdateHandler
from tornado.ioloop import IOLoop
from tornado.web import Application
from aredis import StrictRedis
from db.DbSession import start_mysql_db

def setup_redis(application: Application, host: str, port: int, password: str, decode_responses: bool):
    redis = StrictRedis(host=host, port=port, password=password, db=0, decode_responses=decode_responses)
    setattr(application, 'redis', redis)
    


def make_app():
    app = Application([
        (r"/login_with_mobile", LoginWithMobileHandler),
        (r"/user_update", UserUpdateHandler),
    ])
    setattr(app, 'secret_key', 'AI-abc-123')
    setup_redis(app, '127.0.0.1', 6379, None, True)
    start_mysql_db('admin:vshowat501@tcp(vshow.cl40o6mmw7v5.rds.cn-north-1.amazonaws.com.cn:3306)/AIagent?charset=utf8mb4&parseTime=True')
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()