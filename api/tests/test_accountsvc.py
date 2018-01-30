import unittest

from api import sqla_engine, DBSession
from api.models import DBModel, Account, Role
from api.admin import AccountSvc

class TestAccountSvc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DBModel.metadata.drop_all(sqla_engine)
        DBModel.metadata.create_all(sqla_engine)
        r1 , r2 = Role(name='admin'), Role(name='pikus')
        DBSession.add(r1)
        DBSession.add(r2)
        a = Account(username='gburek', fullName='Greg Burek', email='gru@mailinator.com')
        a.set_password('dupa')
        a.roles.extend((r1, r2))
        DBSession.add(a)
        DBSession.commit()
        cls.DBSession = DBSession

    def test_authentificate(self):
        accsvc = AccountSvc(self.DBSession)
        usr = accsvc.authentificate('chuj', '')
        self.assertIsNone(usr, 'Expected None if username not found')
        usr = accsvc.authentificate('gburek', 'dupa')
        self.assertIsNotNone(usr,  msg='Expected gburek found and password test pass')
        usr = accsvc.authentificate('gru@mailinator.com', 'dupa')
        self.assertIsNotNone(usr,  msg='Expected gru@mailinator.com found and password test pass')
        usr = accsvc.authentificate('gburek', 'doopa')
        self.assertIsNone(usr, 'Expected password test fail')
