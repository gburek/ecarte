import enum
from sqlalchemy import Table, Column, Integer, Float, String, Unicode, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt

DBModel = declarative_base()

class NotFoundError(Exception):
	pass

	
class AuthType(enum.Enum):
	local = 'local'
	facebook = 'facebook'
	google = 'google'
	twitter = 'twitter'


class Role(DBModel):
	__tablename__ = 'role'
	id = Column(Integer, primary_key=True, unique=True)
	name = Column(String(32))


account_roles = Table('account_role',
                      DBModel.metadata,
                      Column('username', String, ForeignKey('account.username')),
                      Column('role_id', Integer, ForeignKey('role.id')))

account_restaurants = Table('account_restaurant',
	                        DBModel.metadata,
	                        Column('username', ForeignKey('account.username')),
	                        Column('restaurant_id', ForeignKey('restaurant.id')))


class Account(DBModel):
	__tablename__ = 'account'

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, index=True)
	fullName = Column(Unicode)
	email = Column(String, unique=True, index=True)
	login_method = Column(Enum(AuthType), name='auth_type', nullable=False, default=AuthType.local)
	pwd = Column(String)
	active = Column(Boolean, default=True)
	roles = relationship('Role', secondary=account_roles, lazy='subquery')

	def set_password(self, pwd):
		self.pwd = sha256_crypt.hash(pwd)
    
	def check_password(self, pwd):
		return sha256_crypt.verify(pwd, self.pwd or '')

	@property
	def is_admin(self):
		if not hasattr(self, '_is_admin'):
			self._is_admin = False
			for r in self.roles:
				if r.id == 'admin':
					self._is_admin = True
		return self._is_admin


# All language codes are ISO 639-1
# Anything named *_intln contains translation(s) to secondary language(s) stored as JSON {lang-code: value}

class Restaurant(DBModel):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key=True)
	active = Column(Boolean, default=True)
	name = Column(Unicode, index=True)
	primary_lang = Column(String(2), default='en')
	# list of language codes
	extra_langs = Column(JSONB)
	description = Column(Unicode)
	# {'ko': 'Korean translation'}
	description_intl = Column(JSONB)
	keywords = Column(Unicode)
	address1 = Column(Unicode(100))
	address2 = Column(Unicode(100))
	city = Column(Unicode(100), index=True)
	postal_code = Column(String(12))
	province_code = Column(String(2))
	country = Column(Unicode(20))
	lat = Column(Float, index=True)
	long = Column(Float, index=True)
	order_phone = Column(String(20))
	managing_users = relationship('Account', secondary=account_restaurants, lazy='subquery')