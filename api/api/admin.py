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

	def update(self, id, **kwargs):
		for key in kwargs:
			logger.debug('** %s: [%s]', key, kwargs[key])
		acc = self.dbsess.query(models.Account).get(id)
		if acc is None:
			raise models.NotFoundError()
		errors = {}
		# TODO: centralize error messages
		if 'email' in kwargs:
			from validate_email import validate_email
			if not validate_email(kwargs['email']):
				errors['email'] = 'Invalid email address'
			else:
				if self.dbsess.query(models.Account).filter(
						models.Account.email == kwargs['email'],
						models.Account.id != id).count() != 0:
					errors['email'] = 'This email is already in use'
				acc.email = kwargs['email']
		if 'password1' in kwargs and 'password2' in kwargs:
			pwtest = ''+kwargs['password1']+kwargs['password2']
			if pwtest != '':
				blank = False
				if not kwargs['password1']:
					errors['password1'] = 'This can not be blank'
					blank = True
				if not kwargs['password2']:
					errors['password2'] = 'This can not be blank'
					blank = True
				if not blank and kwargs['password1'] != kwargs['password2']:
					errors['password2'] = 'Passwords do not match'
				if not errors:
					acc.set_password(kwargs['password1'])				
		if errors:
			self.dbsess.rollback()
			return errors
		self.dbsess.commit()
		# return nothing in case of success

