from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, g
from app import db
from functools import wraps


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    head_img = db.Column(db.Unicode(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribut')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def decode_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            return data
        except BaseException:
            return None

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        current_app.logger.info('用户%s确认！' % self.username)

    def can(self, permissions):
        return True

    def is_administrator(self):
        return True


def ckeck_token():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get('Authorization', None)
            data = User.decode_token(token)
            if not data:
                return {'error': 'Invalid token'}, 401
            g.current_user = User.query.filter(
                User.id == data.get('id')).first()
            g.current_user.ping()
            return fn(*args, **kwargs)

        return decorator

    return wrapper
