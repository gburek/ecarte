import enum
from sqlalchemy import Table, Column, Integer, String, Enum, DateTime, Boolean, ForeignKey
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


class Account(DBModel):
	__tablename__ = 'account'

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, index=True)
	fullName = Column(String)
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


class Business(DBModel):
	__tablename__ = 'business'

	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	
