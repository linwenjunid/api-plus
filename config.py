import os
import logging
import logging.handlers


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL')

    DEBUG = True

    @staticmethod
    def init_app(app):
        # 日志处理
        myformat = logging.Formatter('%(asctime)s - %(levelname)s - '
                                     '%(filename)s - %(funcName)s - '
                                     '%(lineno)s - %(message)s')
        handler = logging.handlers.TimedRotatingFileHandler("log/nohup.out", when='H', interval=1,
                                                            backupCount=10, encoding='UTF-8')
        handler.suffix = "%Y%m%d-%H%M.log"
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(myformat)
        app.logger.addHandler(handler)
