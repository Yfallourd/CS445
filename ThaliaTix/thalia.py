from flask import request
from flask_api import FlaskAPI, status
import json
from time import strftime, gmtime
from threading import Lock
# Remember to bind headers to responses !
app = FlaskAPI(__name__)

lock = Lock()
#Replace by "database", maybe a conf file
shows = []
sections = []
donations = [] # Donation requests
donated = [] # Donated tickets
orders = []
tickets = []
reports = []
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
            dictpayload["wid"] = "wid"+str(wid)
            shows.append(dictpayload)
            return json.dumps({'wid': "wid"+str(wid)}), status.HTTP_200_OK


@app.route('/shows/<wid>', methods=['GET', 'PUT', 'DELETE'])
def editShow(wid):
    if request.method == 'GET':
        for dict in shows:
            if dict["wid"] == str(wid):
                return json.dumps(dict), status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        for dic in shows:
            if dic["wid"] == str(wid):
                payload = request.get_json(force=True)
                if checkData(payload, 'POSTshow'):
                    shows.remove(dic)
                    dictpayload = json.loads(payload)
                    dictpayload["wid"] = str(wid)
                    shows.append(dictpayload)
                    return status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        for dic in shows:
            if dic["wid"] == str(wid):
                shows.remove(dic)

@app.route('/shows/<wid>/sections', methods=['GET'])
def viewAllSectionsForShow(wid):
    return json.dumps(sections)

@app.route('/shows/<wid>/sections/<sid>', methods=['GET'])
def viewSections(wid, sid):
    showdict = {}
    for dic in shows:
        if dic["wid"] == str(wid):
            showdict = dic
    for dic in sections:
        if dic["section"] == str(sid): # Gotta add the seating when done
            if not showdict == {}:
                return {**showdict, **dic}, status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

@app.route('/shows/<wid>/donations', methods=['POST'])
def subscribeToDonations(wid):
    if request.method == 'POST':
        global did
        payload = request.get_json(Force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg ofc
            did += 1
            dictpayload = json.loads(payload)
            dictpayload["did"] = "did"+str(did)
            dictpayload["status"] = "pending"
            dictpayload["tickets"] = []
            donations.append(dictpayload)
            resp = {"did": "did"+str(did)}
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
        if "show" in request.args:
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
                    if 'starting_seat_id' in request.args:
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
        else:
            resp = []
            temp = {}
            for each in sections:
                temp = each
                temp.pop("seating")
                resp.append(temp)
            return resp, status.HTTP_200_OK

    if request.method == 'POST':
        global sid
        payload = request.get_json(Force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg
            with lock:
                sid +=1
                dictpayload = json.loads(payload)
                dictpayload["sid"] = "sid"+str(sid)
                sections.append(dictpayload)
                resp = {}
                resp["sid"] = "sid"+str(sid)
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
    resp = [] # TODO : format seating
    for each in sections:
        temp = {}
        temp["sid"] = each["sid"]
        temp["section_name"] = each["section_name"]
        resp.append(temp)
    return json.dumps(resp), status.HTTP_200_OK

@app.route('/sections/<sid>')
def viewSection(sid):
    for each in sections:
        if each["sid"] == str(sid):
            return json.dumps(each), status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

######### ORDERS #########
@app.route('/orders', methods=['GET', 'PUT', 'POST'])
def viewOrCreateOrders():
    if request.method == 'GET':
        if ('start_date' in request.args) & ('end_date' in request.args):
            # Should regex check values
            start = list(request.args.get('start_date'))
            sdate = str(start)[0:3]+"-"+str(start)[4:6]+"-"+str(start)[6:8]
            end = list(request.args.get('end_date'))
            edate = str(end)[0:3]+"-"+str(end)[4:6]+"-"+str(end)[6:8]
            resp = []
            for each in orders:
                if sdate < each["date_ordered"] < edate:
                    resp.append(each)
            return resp, status.HTTP_200_OK
        return orders, status.HTTP_200_OK
    if request.method == 'POST':
        global oid
        #global tid
        #global cid
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
                        resp["wid"] = each["wid"]
                        resp["show_info"] = each["show_info"]
                        for section in each["seating_info"]:
                            if section["sid"] == dictpayload["sid"]:
                                price = section["price"]
                for i in range(quantity):
                    resptickets.append(createTicket(price, dictpayload["sid"], dictpayload["seats"][i]["cid"],
                                                    "oid"+str(oid), dictpayload["wid"], dictpayload["patron_info"],
                                                    resp["show_info"]))
                # TO DO : Build order in dictpayload, build response in resp, manage ticket creation
                dateordered = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                dictpayload["date_ordered"] = dateordered
                dictpayload["order_amount"] = quantity*int(price)
                dictpayload["number_of_tickets"] = quantity
                dictpayload.pop("seats", None)
                dictpayload.pop("sid", None)
                resp["oid"] = "oid"+str(oid)
                dictpayload = {**dictpayload, **resp}
                orders.append(dictpayload)
                resp["date_ordered"] = dateordered
                resp["tickets"] = resptickets
                resp["order_amount"] = quantity*int(price)
                return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return status.HTTP_400_BAD_REQUEST

@app.route('/orders/<oid>', methods=['GET', 'PUT', 'DELETE'])
def editOrders(oid):
    if request.method == 'GET':
        temptick = []
        for each in orders:
            if each["oid"] == str(oid):
                for ticket in tickets:
                    if ticket["oid"] == str(oid):
                        temptick.append({"tid": ticket["tid"], "status": ticket["status"]})
                each["tickets"] = temptick
                return json.dumps(each), status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND


######### TICKETS #########
@app.route('/tickets')
def viewAllTickets():
    return "Not implemented"

@app.route('/tickets/donations', methods=['POST'])
def donateTickets():
    if request.method == 'POST':
        if 'tickets' in request.args:
            # Header stuff
            for each in request.args.get("tickets"):
                for order in orders:
                    if {"tid": each, "status": "open"} in order["tickets"]:
                        order["tickets"].pop({"tid": each, "status": "open"})
                        order["number_of_tickets"] -= 1
                    for donation in donations:
                        if donation["wid"] == order["wid"]:
                            donation["tickets"].append(each)
                            if len(donation["tickets"]) == donation["count"]:
                                donation["status"] = "assigned"
                                # Create order ? Hmmm
                            return status.HTTP_201_CREATED
                    donated.append(each)
                    return status.HTTP_201_CREATED
        return status.HTTP_400_BAD_REQUEST

@app.route('/tickets/<tid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viewOrEditTickets(tid):
    if request.method == 'GET':
        global oid
        global cid
        resp = {}
        for each in tickets:
            if each["tid"] == tid:
                resp = each
        if resp == {}:
            return status.HTTP_404_NOT_FOUND
        for each in sections:
            if each["sid"] == resp["sid"]:
                resp["section_name"] = each["section_name"]
                for row in each["seating"]:
                    for seat in row["seats"]:
                        if not seat["cid"] == resp["cid"]:
                            row.pop(seat)
                        else:
                            seat.pop(status)
                    if len(row["seats"]) == 0:
                        each.pop(row)
                    else:
                        resp["seating"] = row
        resp.pop(oid)
        resp.pop(cid)
        return json.dumps(resp), status.HTTP_200_OK
    if request.method == 'POST':
        if ("tid" in request.args) & ("status" in request.args):
            for each in tickets:
                if each["tid"] == tid:
                    each["status"] = "used"
            return json.dumps({"tid": tid, "status": "used"}), status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

######### REPORTS #########
@app.route('/reports')
def viewAllReports():
    resp = []
    for each in reports:
        resp.append({"mrid": each["mrid"], "name": each["name"]})
    return json.dumps(resp), status.HTTP_200_OK

@app.route('/reports/<mrid>')
def viewReport(mrid):
    if "show" in request.args:
        wid = request.args.get("show")
        report = {}
        for each in reports:
            if each["mrid"] == str(mrid):
                report = each
        if report == {}:
            return status.HTTP_404_NOT_FOUND
        for show in report["shows"]:
            if not show["wid"] == wid:
                report["shows"].pop(show)
        if len(report["shows"]) == 0:
            return status.HTTP_404_NOT_FOUND
        return json.dumps(report), status.HTTP_200_OK
    elif ('start_date' in request.args) & ('end_date' in request.args):
        report = {}
        start = list(request.args.get('start_date'))
        sdate = str(start)[0:3] + "-" + str(start)[4:6] + "-" + str(start)[6:8]
        end = list(request.args.get('end_date'))
        edate = str(end)[0:3] + "-" + str(end)[4:6] + "-" + str(end)[6:8]
        for each in reports:
            if each["mrid"] == str(mrid):
                report = each
        if report == {}:
            return status.HTTP_404_NOT_FOUND
        for show in report["shows"]:
            if not sdate < show["show_info"]["date"] < edate:
                report["shows"].pop(show)
        if len(report["shows"]) == 0:
            return status.HTTP_404_NOT_FOUND
        return json.dumps(report), status.HTTP_200_OK
    else:
        for each in reports:
            if each["mrid"] == str(mrid):
                return json.dumps(each), status.HTTP_200_OK

######### SEARCH #########
@app.route('/search')
def search():
    if ("topic" in request.args) & ("key" in request.args):
        resp = {}
        results = []
        if not (request.args.get("topic") == "show") | (request.args.get("topic") == "order"):
            return status.HTTP_400_BAD_REQUEST

        if request.args.get("topic") == "show":
            for each in shows:
                for key in each:
                    for value in each[key]:
                        if (request.args.get("key") in value) & (not each in results):
                            results.append(each)
            resp["shows"] = results
        elif request.args.get("topic") == "order":
            for each in orders:
                for key in each:
                    for value in each[key]:
                        if (request.args.get("key") in value) & (not each in results):
                            results.append(each)
            resp["orders"] = results
        return json.dumps(results), status.HTTP_200_OK


######### METHODS #########
def checkSeat(seats, number):
    for each in seats:
        if (each["seat"] == str(number)) & (each["status"] == "available"):
            return True
    return False

def createTicket(price, sid, cid, oid, wid, patron_info, show_info):
    global tid
    tid += 1
    tickdict = {"tid": str(tid), "price": price, "status": "open", "oid": str(oid),
                "sid": str(sid), "cid": str(cid), "wid": str(wid), "patron_info": patron_info,
                "show_info": show_info}
    tickets.append(tickdict)
    return tid

def init():
    print('init')
    global sid
    #seating
    file = open("project-test-theatre-seating.json", "r")
    dic = json.loads(file.read())
    print(dic)
    for each in dic:
        sid += 1
        temp = {"sid": "sid"+str(sid)}
        temp = {**temp, **each}
        sections.append(temp)
        print("sid is :" + str(sid))

if __name__ == "__main__":
    init()
    app.run(debug=True)
