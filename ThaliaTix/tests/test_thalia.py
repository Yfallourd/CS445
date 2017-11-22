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
        with thalia.app.app_context():
            thalia.init("thalia/JSON_files/project-test-theatre-seating.json")

    def tearDown(self):
        self.app.get('/reset')

    def test_emptyshow(self):
        rv = self.app.get('/shows')
        self.assertEqual(rv.data, b'[]')  # Check when shows are empty
        self.assertEqual(rv.status_code, 200)

    def test_createshow(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        self.assertEqual(rv.status_code, 201)
        self.assertTrue(len(thalia.shows) == 1)
        wid = json.loads(rv.data.decode())["wid"]

        rv = self.app.get('/shows')
        self.assertIn(b'show_info', rv.data)

        rv = self.app.get('/shows/'+str(wid))
        self.assertIn(b'seating_info', rv.data)

    def test_updateshow(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        wid = json.loads(rv.data.decode())["wid"]

        rv = self.dataRequest("/shows/"+wid, "thalia/JSON_files/test-show-update-PUT-1.json", "put")
        self.assertEqual(rv.status_code, 200)
        self.assertNotIn(b'"price": 600', rv.data)

        rv = self.dataRequest("/shows/151515", "thalia/JSON_files/test-show-update-PUT-1.json", "put")
        self.assertEqual(rv.status_code, 404)

    def test_deleteshow(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        wid = json.loads(rv.data.decode())["wid"]

        self.app.delete('/shows/'+str(wid))
        rv = self.app.get('/shows')
        self.assertTrue(len(thalia.shows) == 0)

    def test_getsections(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        wid = json.loads(rv.data.decode())["wid"]

        rv = self.app.get('/shows/'+wid+"/sections")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'"Front right', rv.data)
        self.assertIn(b'"Front center', rv.data)
        self.assertIn(b'"Front left', rv.data)

        rv = self.app.get('/shows/'+wid+'/sections/1')
        self.assertEqual(rv.status_code, 200)

    def test_subscribetodonation(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        wid = json.loads(rv.data.decode())["wid"]

        rv = self.dataRequest("/shows/"+wid+"/donations", "thalia/JSON_files/test-shows-subscribe-POST-1.json", "post")
        did = json.loads(rv.data.decode())["did"]
        self.assertEqual(rv.status_code, 201)
        self.assertTrue(len(thalia.donations) == 1)

        rv = self.app.get("/shows/"+wid+"/donations/"+did)
        self.assertEqual(rv.status_code, 200)

    def test_possibleseatrequest(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.app.get('/seating', query_string=dict(show='1', section='1', count=3))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(json.loads(rv.data.decode())["status"] == "ok")

    def test_imppossibleseatrequest(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.app.get('/seating', query_string=dict(show='1', section='1', count=6))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Error" in json.loads(rv.data.decode())["status"])

    def test_getallseating(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.app.get('/seating')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_getseating(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.app.get('/seating/1')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)
        self.assertEqual(json.loads(rv.data.decode())["sid"], "1")

    def test_createorder(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        self.assertEqual(rv.status_code, 201)
        self.assertTrue(len(thalia.orders) == 1)
        self.assertTrue(len(json.loads(rv.data.decode())["tickets"]) == 3)


    def test_getallorder(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get('/orders')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_getorder(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get('/orders/1')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_getwithdateorder(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get('/orders', query_string=dict(start_date=strftime("%Y%m%d", gmtime()),
                                                       end_date=strftime("%Y%m%d", gmtime())))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_getticket(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get('/tickets/1')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_postticket(self):
        self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.post('/tickets/1', data=json.dumps("{\"tid\": \"1\",\"status\": \"used\"}").encode())
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) != 0)

    def test_donateticket(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.dataRequest("/shows/1/donations", "thalia/JSON_files/test-shows-subscribe-POST-1.json",
                              "post")
        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.dataRequest('/tickets/donations', "thalia/JSON_files/test-tickets-donate-ticket-POST.json", "post")
        self.assertEqual(rv.status_code, 201)

    def test_reports(self):
        rv = self.app.get('/reports')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get('/reports/1')
        self.assertEqual(rv.status_code, 404)

    def test_ordersearch(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get("/search", query_string={"topic": "order", "key": "John Doe"})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) == 1)

    def test_showsearch(self):
        rv = self.dataRequest("/shows", "thalia/JSON_files/test-shows-create-POST-1.json", "post")

        rv = self.dataRequest("/orders", "thalia/JSON_files/test-orders-create-request-POST-1.json", "post")

        rv = self.app.get("/search", query_string={"topic": "show", "key": "King Lear"})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(len(json.loads(rv.data.decode())) == 1)

    def test_checkseat(self):
        self.assertTrue(thalia.checkSeat({"row": "1", "seats": ["1", "2", "3"]}, 1, "1"))

    def test_sellseat(self):
        thalia.sellSeat("1")
        tempseat = {}
        for seat in thalia.seats:
            if seat["cid"] == "1":
                tempseat = seat
        self.assertEqual(tempseat["status"], "sold")

    def test_createticket(self):
        thalia.createTicket(1, "1", "1", "1", "1", {}, {})
        self.assertEqual(len(thalia.tickets), 1)
        self.assertEqual(thalia.tid, 1)

    def test_init(self):
        with thalia.app.app_context():
            thalia.init("thalia/JSON_files/project-test-theatre-seating.json")
        self.assertTrue(len(thalia.seats) != 0)

    def test_reset(self):
        rv = self.app.get('/reset')
        self.assertEqual(rv.status_code, 200)


    def dataRequest(self, endpoint, filepath, type):
        file = open(filepath, "r")
        data = file.read()
        file.close()
        if type == "post":
            return self.app.post(endpoint, data=data)
        if type == "put":
            return self.app.put(endpoint, data=data)


if __name__ == "__main__":
    unittest.main()
