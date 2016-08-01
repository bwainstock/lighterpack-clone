import os
import tempfile
import unittest

from application import application, db, Item

class LighterpackTestCase(unittest.TestCase):

    db_path = '/'.join([application.root_path, 'test.db'])
    application.config.update(dict(
        SQLALCHEMY_DATABASE_URI = '/'.join(["sqlite://", db_path]),
        WTF_CSRF_ENABLED = False,
        TESTING = True
    ))

    def create_application(self):
        return application

    def setUp(self):
        db.create_all()
        self.application = application.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        rv = self.application.get('/')
        assert b'No entries here so far' in rv.data

    def test_add_item(self):
        rv = self.application.post('/additem', data=dict(
            make = 'ULA',
            model = 'Catalyst',
            color = 'Blue',
            weight = 1.0,
            count = 1,
            description = 'A nice backpack'
        ), follow_redirects=True)
        assert b'Item added' in rv.data
        assert b'No entries here so far' not in rv.data
        assert b'ULA - Catalyst' in rv.data

        items = Item.query.filter_by(make='ULA', model='Catalyst').all()
        assert len(items) == 1


if __name__ == '__main__':

    unittest.main()
