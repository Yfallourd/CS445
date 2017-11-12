from flask import request
from flask_api import FlaskAPI, status
import json
from time import strftime, gmtime
from threading import Lock
# Remember to bind headers to responses !
# TRy to look for a key-based find method for dicts !
app = FlaskAPI(__name__)

lock = Lock()
#Replace by "database", maybe a conf file
shows = []
sections = []
donations = []
orders = []
tickets = []
#Replace by reading a conf file
wid = 0 #Shows
sid = 0 #Sections
did = 0 #Donations
mrid = 0 #Reports
oid = 0 #Orders
tid = 0 #Tickets

def checkData(payload, expected):
    if expected == 'POSTshow':
        data = json.loads(payload)
        if not (len(data) == 2)|(len(data["show_info"]) == 4):
            return False
        for each in data["seating_info"]:
            if not len(each) == 2:
                return False
        return True
        #Rest of the checking will be regex matching

######### SHOWS #########
@app.route('/shows', methods=['GET', 'POST'])
def viewOrCreateShow():
    global wid
    if request.method == 'GET':
        return shows
    if request.method == 'POST':
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):
            wid +=1
            dictpayload = json.loads(payload)
            dictpayload["wid"] = str(wid)
            shows.append(dictpayload)
            return json.dumps({'wid': str(wid)}), status.HTTP_200_OK


@app.route('/shows/<wid>', methods=['GET', 'PUT', 'DELETE'])
def editShow(wid):
    if request.method == 'GET':
        for dict in shows:
            if dict["wid"] == str(wid):
                return json.dumps(dict), status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        for dict in shows:
            if dict["wid"] == str(wid):
                payload = request.get_json(force=True)
                if checkData(payload, 'POSTshow'):
                    shows.remove(dict)
                    dictpayload = json.loads(payload)
                    dictpayload["wid"] = str(wid)
                    shows.append(dictpayload)
                    return status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        for dict in shows:
            if dict["wid"] == wid:
                shows.remove(dict)

@app.route('/shows/<wid>/sections', methods=['GET'])
def viewAllSections(wid):
    return sections

@app.route('/shows/<wid>/sections/<sid>', methods=['GET'])
def viewSections(wid, sid):
    showdict = {}
    for dict in shows:
        if dict["wid"] == str(wid):
            showdict = dict
    for dict in sections:
        if dict["section"] == str(sid): # Gotta add the seating when done
            if not showdict == {}:
                return {**showdict, **dict}, status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

@app.route('/shows/<wid>/donations', methods=['POST'])
def subscribeToDonations(wid):
    if request.method == 'POST':
        global did
        payload = request.get_json(Force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg ofc
            did += 1
            dictpayload = json.loads(payload)
            dictpayload["did"] = str(did)
            dictpayload["status"] = "pending"
            dictpayload["tickets"] = []
            donations.append(dictpayload)
            resp = {}
            resp["did"] = str(did)
            return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return status.HTTP_400_BAD_REQUEST

@app.route('/shows/<wid>/donations/<did>', methods=['GET'])
def viewDonationRequests(wid, did):
    for each in donations:
        if (each["wid"] == str(wid)) | (each["did"] == str(did)):
            return each, status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

######### SEATING #########
@app.route('/seating', methods=['POST', 'GET'])
def createSection():
    if request.method == 'GET':
        if request.args.get('show'):  # Check for valid data, to do
            seats = []
            count = 0
            startingseat = 1
            freeseats = []
            resp = []
            respdict = {}
            foundall = False
            for each in shows:
                if each["wid"] == str(request.args.get('show')):
                    seatinginfo = each["seating_info"]
                    # for seating in seatinginfo:
                    #    if seating["sid"] == str(request.args.get('section')):
                    # Finding if the provided sid is in this show !
                    for section in sections:
                        if section["sid"] == str(request.args.get('section')):
                            seats = section["seating"]
                            respdict = {**section, **respdict}
                    if request.args.get('starting_seat_id'):
                        for each in seats:
                            if each["seats"]["cid"] == request.args.get('starting_seat_id'):
                                startingseat = each["seats"]["seat"]
                    else:
                        startingseat = 1
                    i = int(startingseat)
                    while checkSeat(seats, i):
                        freeseats.append(i)
                        count += 1
                        i += 1
                        if count >= request.args.get('count'):
                            foundall = True
                            break
                    if not foundall:
                        i = int(startingseat)-1
                        while checkSeat(seats, i):
                            freeseats.append(i)
                            count += 1
                            i -= 1
                            if count >= request.args.get('count'):
                                foundall = True
                                break
                    if not foundall:
                        return "Sorry, no seat arrangement sastisfy your request", status.HTTP_200_OK
                    for each in seats:
                        if int(each["seats"]["seat"]) in freeseats:
                            resp.append(each)
                    respdict = {**each, **respdict}
                    respdict = {**resp, **respdict}  # Rows and shit à gérer
                    return respdict, status.HTTP_200_OK
            return status.HTTP_404_NOT_FOUND


    if request.method == 'POST':
        global sid
        payload = request.get_json(Force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg
            with lock:
                sid +=1
                dictpayload = json.loads(payload)
                dictpayload["sid"] = str(sid)
                sections.append(dictpayload)
                resp = {}
                resp["sid"] = str(sid)
                return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return status.HTTP_400_BAD_REQUEST

@app.route('/seating/<sid>', methods=['GET', 'PUT', 'DELETE'])
def editOrRequestSections(sid):
    if request.method == 'GET':
        for each in sections:
            if each["sid"] == str(sid):
                return each["seating"], status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        for each in sections:
            if each["sid"] == str(sid):
                payload = request.get_json(Force=True)
                if checkData(payload, 'POSTshow'):  # Not the right arg
                    sections.remove(each)
                    dictpayload = json.loads(payload)
                    dictpayload["sid"] = str(sid)
                    sections.append(dictpayload)
                    return status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        for each in sections:
            if each["sid"] == str(sid):
                sections.remove(each)
                return status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND

@app.route('/sections')
def viewAllSections():
    resp = []
    for each in sections:
        temp = {}
        temp["sid"] = each["sid"]
        temp["section_name"] = each["section_name"]
        resp.append(temp)
    return resp, status.HTTP_200_OK

@app.route('/sections/<sid>')
def viewSection(sid):
    for each in sections:
        if each["sid"] == str(sid):
            return each, status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

######### ORDERS #########
@app.route('/orders', methods=['GET', 'PUT', 'POST'])
def viewOrCreateOrders():

    if request.method == 'POST':
        global oid
        global tid
        price = ""
        resptickets = []
        payload = request.get_json(Force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg
            with lock:
                oid +=1
                resp = {}
                dictpayload = json.loads(payload)
                quantity = len(dictpayload["seats"])
                for each in shows:
                    if each["wid"] == dictpayload["wid"]:
                        resp = each
                        for section in each["seating_info"]:
                            if section["sid"] == dictpayload["sid"]:
                                price = section["price"]
                for i in range(quantity):
                    resptickets.append(createTicket(price, sid, cid))
                # TO DO : Build order in dictpayload, build response in resp, manage ticket creation
                dateordered = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                dictpayload["date_ordered"] = dateordered
                dictpayload["order_amount"] = quantity*int(price)
                dictpayload["number_of_tickets"] = quantity
                dictpayload.pop("seats", None)
                dictpayload.pop("sid", None)
                resp["oid"] = str(oid)
                sections.append(dictpayload)
                return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return status.HTTP_400_BAD_REQUEST
@app.route('/orders/<oid>', methods=['GET', 'PUT', 'DELETE'])
def editOrders(oid):


######### TICKETS #########
@app.route('/tickets')
def viewAllTickets():


@app.route('/tickets/<tid>', methods=['GET', 'PUT', 'DELETE'])
def editTickets(tid):


######### REPORTS #########
@app.route('/reports')
def viewAllReports():

@app.route('/reports/<mrid>')
def viewReport(mrid):


######### SEARCH #########
@app.route('/search')
def search():
    print('lol'
          )
def checkSeat(seats, number):
    for each in seats:
        if (each["seat"] == str(number)) & (each["status"] == "available"):
            return True
    return False

def createTicket(price, sid, cid):
    global tid
    tid += 1
    tickdict = {}
    tickdict["tid"] = str(tid)
    tickdict["status"] = "open"
    tickdict["sid"] = str(sid)
    tickdict["cid"] = str(cid)
    tickets.append(tickdict)
    return tid
