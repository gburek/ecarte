import os, sys
import json
import falcon
import jwt
import six
import inspect
from falcon_cors import CORS
import logging
from datetime import datetime, date, time, timedelta
import pprint
import collections
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


logging.basicConfig(format='%(asctime)s %(levelname)s - %(name)s %(message)s',
                    datefmt='%b %d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger('api')

# TODO: using in-memmory sqlite for unit tests would speed things up
# This is public so unit tests can access it for DB schema drop/create
sqla_engine = create_engine(
    	'postgresql://{}:{}@localhost/{}'.format(
    		os.environ.get('ECARTE_DBUSER', 'ecarte'),
    		os.environ.get('ECARTE_DBPWD'),
    		os.environ.get('ECARTE_DB', 'ecarte')))
# Unit tests need this. Alembic probably too.
DBSession = scoped_session(sessionmaker(bind=sqla_engine))


# Usual 'datetime is not JSON serializable'...
def _custom_serialize(_self, media):
	class ExtEncoder(json.JSONEncoder):
		def default(self, obj):
			if isinstance(obj, (datetime, date, time)):
				return obj.isoformat(sep=' ', timespec='milliseconds')
			return json.JSONEncoder(self, obj)
	result = json.dumps(media, cls=ExtEncoder)
	if six.PY3 or not isinstance(result, bytes):
		return result.encode('utf-8')
	return result
# Why provide your own handler when you can monkey patch? ;)
falcon.media.JSONHandler.serialize = _custom_serialize


# It would be more elegant to wrap at the class level but too difficult ATM
def needs_auth(meth):
	def boo():
		raise falcon.HTTPUnauthorized(
				title='401 Unauthorized',
				headers= [('Access-Control-Allow-Origin', 'http://localhost:8081'),
				          ('WWW-Authenticate', 'JWT')])

	def wrapped(self, req, resp):
		token = req.get_header('Authorization')
		if not token:
			boo()			
		# TODO: token may be junk
		try:
			payload = jwt.decode(token, key=APP_JWT_SECRET, algoriths=['HS256'])
			logger.debug('** payload:'+pprint.pformat(payload))
			self.user_auth_token = payload
			meth(self, req, resp)
		except jwt.DecodeError as ex:
			logger.error('Junk JWT received')
			boo()
		except jwt.ExpiredSignatureError as ex:
			logger.info('JWT signature expired. Client needs to re-login')
			boo()
	return wrapped


class DBMiddleware(object):
	def process_resource(self, req, resp, resource, params):
		resource.session = DBSession()

	def process_response(self, req, resp, resource, req_succeeded):
		if hasattr(resource, 'session'):
			if not req_succeeded:
				resource.session.rollback()
			DBSession.remove()


class FooResource(object):
	@needs_auth
	def on_get(self, req, resp):
		logger.debug('foo')
		resp.media = {'success': True, 'now': datetime.now()}

	@needs_auth
	def on_post(self, req, resp):
		logger.debug('post data:' + pprint.pformat(req.params))
		resp.media = {'success': True}


APP_JWT_SECRET = 'n4 POHYB3l 5KURwYsYnO]\/['

from .admin import AccountSvc
from .models import Account, Role


class LoginResource(object):
	def on_post(self, req, resp):
		logger.info('/api/login | post data:' + pprint.pformat(req.media))
		usernm, pwd = req.media['username'], req.media['password']
		acc = AccountSvc(DBSession).authentificate(usernm, pwd)
		if acc is not None:
			payload = {
				'userid': acc.id,
				'username': acc.username,
				'email': acc.email,
				'fullname': acc.fullName,
				'exp': datetime.utcnow() + timedelta(minutes=60*24*3), # TODO: make it a long time after testing expiry
				'roles': [r.name for r in acc.roles],
				'is_admin': acc.is_admin
			}
			global APP_JWT_SECRET
			token = jwt.encode(payload, APP_JWT_SECRET, 'HS256').decode('utf-8')
			logger.debug('authToken: %s', token)
			payload['authToken'] = token
			resp.media = payload
		else:
			resp.media = {'error': 'User name or password do not match'}


class AccountResource(object):
	def on_patch(self, req, resp, accountId):
		errors = AccountSvc(DBSession).update(
			accountId,
			email=req.media['email'],
			password1=req.media['password1'],
			password2=req.media['password2'])
		resp.media = {'errors': errors} if errors else {'success': True}
		

#########################

cors = CORS(allow_origins_list=['http://localhost:8080', 'http://localhost:8081'],
	        allow_all_headers=True, allow_all_methods=True)

app = falcon.API(middleware=[cors.middleware,
                             DBMiddleware()])
	                         #AuthMiddleware()])
# Make POST params available in req.params
app.req_options.auto_parse_form_urlencoded = True

# Could the routes be added in bulk? Check the API docs
app.add_route('/api/foo', FooResource())
app.add_route('/api/login', LoginResource())
app.add_route('/api/account/{accountId:int}', AccountResource())
