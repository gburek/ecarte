import enum
from sqlalchemy import Table, Column, Integer, String, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt

DBModel = declarative_base()

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


class User(DBModel):
	__tablename__ = 'account'

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, index=True)
	fullName = Column(String)
	email = Column(String, unique=True, index=True)
	login_method = Column(Enum(AuthType), name='auth_type', nullable=False, default=AuthType.local)
	pwd = Column(String)
	roles = relationship('Role', secondary=account_roles, lazy='subquery')

	def set_password(self, pwd):
		self.pwd = sha256_crypt.encrypt(pwd)
    
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
		


if __name__ == '__main__':
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	engine = create_engine('postgresql://gburek:dupa@localhost/ecarte')
	DBModel.metadata.drop_all(engine)
	DBModel.metadata.create_all(engine)
	session = sessionmaker(bind=engine)()
	r1 , r2 = Role(name='admin'), Role(name='pikus')
	session.add(r1)
	session.add(r2)
	a = User(username='gburek', fullName='Greg Burek', email='gru@mailinator.com')
	a.set_password('dupa')
	a.roles.extend((r1, r2))
	session.add(a)
	session.commit()