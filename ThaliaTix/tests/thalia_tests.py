from thalia import thalia
from flask import request
from flask_api import FlaskAPI, status
import json
from time import strftime, gmtime
from threading import Lock
import unittest

class ThaliaTestCase(unittest.TestCase):

    def setUp(self):

        thalia.app.testing = True
        self.app = thalia.app.test_client()


    def test_shows(self):
        rv = self.app.get('/shows')
        assert rv.data == b'[]'  # Check when shows are empty
        assert rv.status_code == 200

        file = open("../thalia/JSON_files/test-shows-create-POST-1.json", "r")
        data = file.read()
        file.close()

        rv = self.app.post('/shows', data=data)
        assert rv.status_code == 201
        assert b'wid' in rv.data
        wid = json.loads(rv.data.decode())["wid"]

        rv = self.app.get('/shows')
        assert b'show_info' in rv.data

        rv = self.app.get('/shows/'+str(wid))
        assert 
if __name__ == "__main__":
    unittest.main()
