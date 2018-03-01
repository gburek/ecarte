from . import models
from sqlalchemy import or_
import logging

logger = logging.getLogger('admin')
class AccountSvc(object):
	def __init__(self, dbsess):
		self.dbsess = dbsess

	def authentificate(self, usrnm_or_email, pwd):
		logger.debug('usrnm_or_email: %s', usrnm_or_email)
		usr = self.dbsess.query(models.Account).filter(or_(models.Account.username == usrnm_or_email,
			                                               models.Account.email == usrnm_or_email),
		                                               models.Account.active == True).one_or_none()
		logger.debug('usr: %s', usr)
		if usr is not None and usr.check_password(pwd):
			return usr
