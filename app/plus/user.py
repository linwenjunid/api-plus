from . import api
from .. import db
from ..models import User, ckeck_token
from flask_restplus import Resource, fields
from flask import request

parser = api.parser()
parser.add_argument('Authorization', help='令牌:JWT <token>', location='headers')

ns = api.namespace('users', description='用户接口')

model_user_r = ns.model('User_r', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
})

model_user_g = ns.model('User_g', {
    'id': fields.String,
    'username': fields.String,
    'email': fields.String,
    'uri': fields.Url('plus.user', absolute=True)
})


@ns.route('/<int:id>', endpoint='user')
@ns.expect(parser)
class UserApi(Resource):
    @ckeck_token()
    @ns.doc(params={'id': '用户编码'})
    @ns.marshal_with(model_user_g, mask='', code=200)
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        if user:
            return user, 200
        else:
            return None, 204

    @ckeck_token()
    @ns.doc(params={'id': '用户编码'})
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return None, 200
        else:
            return None, 400




parserlist = api.parser()
parserlist.add_argument(
    'Authorization',
    help='令牌:JWT <token>',
    location='headers')
parserlist.add_argument('page', type=int, location='args')
parserlist.add_argument('per_page', type=int, location='args')


@ns.route('/', endpoint='userlist')
@ns.expect(parserlist)
class UserList(Resource):
    @ckeck_token()
    @ns.marshal_with(model_user_g, mask='', code=200)
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = User.query.paginate(
            page, per_page=per_page,
            error_out=False)
        papers = pagination.items
        return papers, 200

    @ckeck_token()
    @ns.expect(model_user_r)
    @ns.marshal_with(model_user_g, mask='', code=200)
    def post(self):
        data = api.payload
        u = User(username=data.get('username'), email=data.get('email'), password=data.get('password'))
        db.session.add(u)
        db.session.commit()
        return u, 200

