from . import api
from ..models import User
from flask_restplus import Resource, fields

model_login = api.model('login', {
    'username': fields.String,
    'password': fields.String,
})


@api.route("/login")
class Login(Resource):
    @api.expect(model_login)
    def post(self):
        data = api.payload
        user = User.query.filter(User.username == data.get('username')).first()
        if user and user.verify_password(data.get('password')):
            user.ping()
            return {'access_token': user.encode_token()}, 200
        else:
            return {'error': 'login failed'}, 400
