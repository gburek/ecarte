from . import models
from sqlalchemy import or_

class AccountSvc(object):
	def __init__(self, dbsess):
		self.dbsess = dbsess

	def authentificate(self, usrnm_or_email, pwd):
		usr = self.dbsess.query(models.Account).filter(or_(models.Account.username == usrnm_or_email,
			                                               models.Account.email == usrnm_or_email),
		                                               models.Account.active == True).one_or_none()
		if usr is not None and usr.check_password(pwd):
			return usr
