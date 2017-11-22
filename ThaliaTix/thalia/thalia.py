from flask import request
from flask_api import FlaskAPI, status
import json
from time import strftime, gmtime
from threading import Lock
from ast import literal_eval

app = FlaskAPI(__name__)

lock = Lock()

# Replace by "database", maybe a conf file
shows = []
sections = []
seats = []
donations = []
orders = []
tickets = []
reports = []

# Replace by reading a conf file
wid = 0  # Shows
sid = 0  # Sections
did = 0  # Donations
mrid = 0  # Reports
oid = 0  # Orders
tid = 0  # Tickets
cid = 0  # Seats


def checkData(payload, expected):
    return True
    # This is where we'd check input
    # Rest of the checking will be regex matching


######### SHOWS #########
@app.route('/thalia/shows', methods=['GET', 'POST'])
def viewOrCreateShow():
    global wid
    if request.method == 'GET':
        resp = []
        for each in shows:
            resp.append({"wid": each["wid"], "show_info": each["show_info"]})
        return json.dumps(resp), status.HTTP_200_OK
    if request.method == 'POST':
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):
            wid += 1
            dictpayload = payload
            dictpayload["wid"] = str(wid)
            shows.append(dictpayload)
            return json.dumps({'wid': str(wid)}), status.HTTP_201_CREATED


@app.route('/thalia/shows/<wid>', methods=['GET', 'PUT', 'DELETE'])
def editShow(wid):
    if request.method == 'GET':
        for dict in shows:
            if dict["wid"] == str(wid):
                return json.dumps(dict), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        for dic in shows:
            if dic["wid"] == str(wid):
                payload = request.get_json(force=True)
                if checkData(payload, 'POSTshow'):
                    shows.remove(dic)
                    dictpayload = payload
                    dictpayload["wid"] = str(wid)
                    shows.append(dictpayload)
                    return json.dumps(''), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        for dic in shows:
            if dic["wid"] == str(wid):
                shows.remove(dic)
        return json.dumps(''), status.HTTP_200_OK


@app.route('/thalia/shows/<wid>/sections', methods=['GET'])
def viewAllSectionsForShow(wid):
    resp = []
    show = {}
    for each in shows:
        if each["wid"] == wid:
            show = each.copy()
    for section in sections:
        for each in show["seating_info"]:
            if section["sid"] == each["sid"]:
                resp.append(section)
    if not resp:
        return json.dumps(''), status.HTTP_404_NOT_FOUND
    return json.dumps(resp), status.HTTP_200_OK


@app.route('/thalia/shows/<wid>/sections/<sid>', methods=['GET'])
def viewSections(wid, sid):
    showdict = {}
    tempdic = {}
    for dic in shows:
        if dic["wid"] == str(wid):
            showdict = dic.copy()
    for each in showdict["seating_info"]:
        if each["sid"] == str(sid):
            showdict["price"] = each["price"]
    showdict.pop("seating_info")
    for dic in sections:
        if dic["sid"] == str(sid):  # Gotta add the seating when done
            if not showdict == {}:
                tempdic = dic.copy()
                for seating in tempdic["seating"]:
                    templist = []
                    for seat in seats:
                        if (seat["sid"] == str(sid)) & (seat["row"] == seating["row"]):
                            tempseat = {"seat": seat["seat"], "status": seat["status"], "cid": seat["cid"]}
                            templist.append(tempseat)
                    seating["seats"] = templist
                return json.dumps({**showdict, **tempdic}), status.HTTP_200_OK
    return json.dumps(''), status.HTTP_404_NOT_FOUND


@app.route('/thalia/shows/<wid>/donations', methods=['POST'])
def subscribeToDonations(wid):
    if request.method == 'POST':
        global did
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg ofc
            did += 1
            dictpayload = payload
            dictpayload["did"] = str(did)
            dictpayload["status"] = "pending"
            dictpayload["tickets"] = []
            donations.append(dictpayload)
            resp = {"did": str(did)}
            return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return json.dumps(''), status.HTTP_400_BAD_REQUEST


@app.route('/thalia/shows/<wid>/donations/<did>', methods=['GET'])
def viewDonationRequests(wid, did):
    for each in donations:
        if (each["wid"] == str(wid)) & (each["did"] == str(did)):
            return json.dumps(each), status.HTTP_200_OK
    return json.dumps(''), status.HTTP_404_NOT_FOUND


######### SEATING #########
@app.route('/thalia/seating', methods=['POST', 'GET'])
def createSection():
    if request.method == 'GET':
        if "show" in request.args:
            seating = []
            count = 0
            startingseat = 1
            freeseats = []
            resp = []
            rownumber = 0
            respdict = {}
            foundall = False
            noseats = False
            for each in shows:
                if each["wid"] == request.args["show"]:
                    seatinginfo = each["seating_info"]
                    for section in sections:
                        if section["sid"] == str(request.args["section"]):
                            seating = section["seating"]
                            respdict = {**section.copy(), **respdict}
                    if 'starting_seat_id' in request.args:  # A refaire lol
                        for seat in seats:
                            if seat["cid"] == request.args["starting_seat_id"]:
                                for x in seating:
                                    if x["row"] == seat["row"]:
                                        tlist = []
                                        for el in x["seats"]:
                                            tlist.append(el["seat"])
                                        startingseat = tlist.index(seat["seat"])+1
                                    else:
                                        seating.remove(x)
                    else:
                        startingseat = 1
                    for row in seating:
                        foundall = False
                        freeseats.clear()
                        count = 0
                        i = int(startingseat)
                        while checkSeat(row, i, request.args["section"]):
                            freeseats.append(str(row["seats"][i-1]["seat"])+"-"+row["row"])
                            count += 1
                            i += 1
                            if count >= int(request.args["count"]):
                                foundall = True
                                break
                    if not foundall:
                        noseats = True
                    for freeseat in freeseats:
                        data = freeseat.split("-")
                        for seat in seats:
                            if (seat["sid"] == request.args["section"])\
                                    & (seat["seat"] == data[0])\
                                    & (seat["row"] == data[1]):
                                tempd = {"cid": seat["cid"], "status": seat["status"], "seat": seat["seat"]}
                                resp.append(tempd)
                                rownumber = seat["row"]
                    respdict = {**each.copy(), **respdict}
                    if "seating_info" in respdict:
                        respdict.pop("seating_info")
                    if noseats:
                        respdict["status"] = "Error: "+str(request.args["count"])+" contiguous seats not available"
                        respdict["starting_seat_id"] = "1"
                        respdict["seating"] = []
                        return json.dumps(respdict), status.HTTP_200_OK
                    else:
                        respdict["seating"] = [{"row": rownumber, "seats": resp}]
                        respdict["starting_seat_id"] = resp[0]["cid"]
                        respdict["status"] = "ok"
                    for info in seatinginfo:
                        if info["sid"] == request.args["section"]:
                            respdict["total_amount"] = int(info["price"])*count
                    print(respdict)
                    return json.dumps(respdict), status.HTTP_200_OK
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        else:
            resp = []
            for each in sections:
                temp = {}
                temp["sid"] = each["sid"]
                temp["section_name"] = each["section_name"]
                resp.append(temp)
            return json.dumps(resp), status.HTTP_200_OK

    if request.method == 'POST':
        global sid
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg
            with lock:
                sid += 1
                dictpayload = payload
                dictpayload["sid"] = str(sid)
                sections.append(dictpayload)
                resp = {}
                resp["sid"] = str(sid)
                return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return json.dumps(''), status.HTTP_400_BAD_REQUEST


@app.route('/thalia/seating/<sid>', methods=['GET', 'PUT', 'DELETE'])
def editOrRequestSections(sid):
    if request.method == 'GET':
        for each in sections:
            if each["sid"] == str(sid):
                return json.dumps(each), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        for each in sections:
            if each["sid"] == str(sid):
                payload = request.get_json(force=True)
                if checkData(payload, 'POSTshow'):  # Not the right arg
                    sections.remove(each)
                    dictpayload = payload
                    dictpayload["sid"] = str(sid)
                    sections.append(dictpayload)
                    return json.dumps(''), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        for each in sections:
            if each["sid"] == str(sid):
                sections.remove(each)
                return json.dumps(''), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND


@app.route('/thalia/sections')
def viewAllSections():
    resp = []
    for each in sections:
        temp = {}
        temp["sid"] = each["sid"]
        temp["section_name"] = each["section_name"]
        resp.append(temp)
    return json.dumps(resp), status.HTTP_200_OK


@app.route('/thalia/sections/<sid>')
def viewSection(sid):
    for each in sections:
        if each["sid"] == str(sid):
            return json.dumps(each), status.HTTP_200_OK
    return json.dumps(''), status.HTTP_404_NOT_FOUND


######### ORDERS #########
@app.route('/thalia/orders', methods=['GET', 'PUT', 'POST'])
def viewOrCreateOrders():
    if request.method == 'GET':
        if ('start_date' in request.args) & ('end_date' in request.args):
            start = request.args.get('start_date')
            sdate = str(start)[0:4] + "-" + str(start)[4:6] + "-" + str(start)[6:8]
            end = request.args.get('end_date')
            edate = str(end)[0:4] + "-" + str(end)[4:6] + "-" + str(end)[6:8]
            resp = []
            for each in orders:
                if sdate <= each["date_ordered"][0:10] <= edate:
                    resp.append(each)
            return json.dumps(resp), status.HTTP_200_OK
        return json.dumps(orders), status.HTTP_200_OK
    if request.method == 'POST':
        global oid
        # global tid
        # global cid
        price = 0
        resptickets = []
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):  # Not the right arg
            with lock:
                oid += 1
                resp = {}
                dictpayload = payload
                quantity = len(dictpayload["seats"])
                for seat in dictpayload["seats"]:
                    sellSeat(seat["cid"])
                for each in shows:
                    if each["wid"] == dictpayload["wid"]:
                        resp["wid"] = each["wid"]
                        resp["show_info"] = each["show_info"]
                        for section in each["seating_info"]:
                            if section["sid"] == dictpayload["sid"]:
                                price = section["price"]
                for i in range(quantity):
                    resptickets.append(createTicket(price, dictpayload["sid"], dictpayload["seats"][i]["cid"],
                                                    str(oid), dictpayload["wid"], dictpayload["patron_info"],
                                                    resp["show_info"]))

                dateordered = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                dictpayload["date_ordered"] = dateordered
                dictpayload["order_amount"] = quantity * int(price)
                dictpayload["number_of_tickets"] = quantity
                dictpayload.pop("seats", None)
                dictpayload.pop("sid", None)
                resp["oid"] = str(oid)
                dictpayload = {**dictpayload, **resp}
                orders.append(dictpayload)
                resp["date_ordered"] = dateordered
                resp["tickets"] = resptickets
                resp["order_amount"] = quantity * int(price)
                return json.dumps(resp), status.HTTP_201_CREATED
        else:
            return json.dumps(''), status.HTTP_400_BAD_REQUEST


@app.route('/thalia/orders/<oid>', methods=['GET', 'PUT', 'DELETE'])
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
        return json.dumps(''), status.HTTP_404_NOT_FOUND


######### TICKETS #########
@app.route('/thalia/tickets')
def viewAllTickets():
    return json.dumps(tickets), status.HTTP_200_OK


@app.route('/thalia/tickets/donations', methods=['POST'])
def donateTickets():
    if request.method == 'POST':
        temptick = []
        tempdict = {}
        payload = request.get_json(force=True)
        dictpayload = payload
        # Header stuff
        for each in dictpayload["tickets"]:
            isdonated = False
            for order in orders:
                tempdict = order.copy()
                for ticket in tickets:
                    if ticket["oid"] == tempdict["oid"]:
                        temptick.append({"tid": ticket["tid"], "status": ticket["status"]})
                tempdict["tickets"] = temptick
                for ticket in tempdict["tickets"]:
                    if (ticket["tid"] == each) & (ticket["status"] == "open"):
                        for t in tickets:
                            if t["tid"] == each:
                                t["status"] = "donated"
                for donation in donations:
                    if (donation["wid"] == tempdict["wid"])\
                            & (len(donation["tickets"]) < donation["count"])\
                            & (not isdonated):
                        donation["tickets"].append(each)
                        donation["status"] = "assigned"
                        isdonated = True

                            # Create order ? Hmmm
        return json.dumps(''), status.HTTP_201_CREATED


@app.route('/thalia/tickets/<tid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def viewOrEditTickets(tid):
    if request.method == 'GET':
        global oid
        global cid
        resp = {}
        for each in tickets:
            if each["tid"] == tid:
                resp = each.copy()
        if resp == {}:
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        seatingdict = {}
        for seat in seats:
            if seat["cid"] == resp["cid"]:
                seatingdict["row"] = seat["row"]
                tempdict = {"cid": seat["cid"], "seat": seat["seat"]}
                seatingdict["seats"] = [tempdict]
        resp["seating"] = seatingdict
        resp.pop("oid")
        resp.pop("cid")
        return json.dumps(resp), status.HTTP_200_OK
    if request.method == 'POST':
        payload = request.get_json(force=True)
        if ("tid" in payload) & ("status" in payload):
            for each in tickets:
                if each["tid"] == tid:
                    each["status"] = "used"
            return json.dumps({"tid": tid, "status": "used"}), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_400_BAD_REQUEST


######### REPORTS #########
@app.route('/thalia/reports')
def viewAllReports():
    resp = []
    for each in reports:
        resp.append({"mrid": each["mrid"], "name": each["name"]})
    return json.dumps(resp), status.HTTP_200_OK


@app.route('/thalia/reports/<mrid>')
def viewReport(mrid):
    if "show" in request.args:
        wid = request.args.get("show")
        report = {}
        for each in reports:
            if each["mrid"] == str(mrid):
                report = each.copy()
        if report == {}:
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        for show in report["shows"]:
            if not show["wid"] == wid:
                report["shows"].pop(show)
        if len(report["shows"]) == 0:
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        return json.dumps(report), status.HTTP_200_OK
    elif ('start_date' in request.args) & ('end_date' in request.args):
        report = {}
        start = list(request.args.get('start_date'))
        sdate = str(start)[0:3] + "-" + str(start)[4:6] + "-" + str(start)[6:8]
        end = list(request.args.get('end_date'))
        edate = str(end)[0:3] + "-" + str(end)[4:6] + "-" + str(end)[6:8]
        for each in reports:
            if each["mrid"] == str(mrid):
                report = each.copy()
        if report == {}:
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        for show in report["shows"]:
            if not sdate < show["show_info"]["date"] < edate:
                report["shows"].pop(show)
        if len(report["shows"]) == 0:
            return json.dumps(''), status.HTTP_404_NOT_FOUND
        return json.dumps(report), status.HTTP_200_OK
    else:
        for each in reports:
            if each["mrid"] == str(mrid):
                return json.dumps(each), status.HTTP_200_OK
        return json.dumps(''), status.HTTP_404_NOT_FOUND


######### SEARCH #########
@app.route('/thalia/search')
def search():
    if ("topic" in request.args) & ("key" in request.args):
        resp = {}
        results = []
        if not (request.args["topic"] == "show") | (request.args["topic"] == "order"):
            return json.dumps(''), status.HTTP_400_BAD_REQUEST

        if request.args["topic"] == "show":
            for each in shows:
                for value in each.values():
                    if (request.args["key"] in str(value)) & (str(value) not in results):
                        results.append(each)
            resp["shows"] = results
        elif request.args["topic"] == "order":
            for each in orders:
                for value in each.values():
                    if (request.args["key"] in str(value)) & (str(value) not in results):
                        results.append(each)
            resp["orders"] = results
        return json.dumps(results), status.HTTP_200_OK


######### METHODS #########
def checkSeat(seatlist, number, sid):
    try:
        for seat in seats:
            if (seat["sid"] == str(sid)) \
                    & (seat["row"] == seatlist["row"]) \
                    & (seatlist["seats"][number-1]["seat"] == seat["seat"]):
                if seat["status"] == "available":
                    return True
        return False
    except IndexError:
        return False

def sellSeat(cid):
    for seat in seats:
        if seat["cid"] == cid:
            seat["status"] = "sold"

def createTicket(price, sid, cid, oid, wid, patron_info, show_info):
    global tid
    tid += 1
    tickdict = {"tid": str(tid), "price": price, "status": "open", "oid": str(oid),
                "sid": str(sid), "cid": str(cid), "wid": str(wid), "patron_info": patron_info,
                "show_info": show_info}
    tickets.append(tickdict)
    return tid


def init(filename):
    global sid
    global cid
    # seating
    file = open(filename, "r")
    dic = json.loads(file.read())
    file.close()
    for each in dic:
        sid += 1
        temp = {"sid": str(sid)}
        temp = {**temp, **each}
        sections.append(temp)
    # From seating init seats
    for each in sections:
        for seating in each["seating"]:
            for seat in seating["seats"]:
                cid += 1
                seats.append(
                    {"sid": each["sid"], "row": seating["row"], "cid": str(cid), "status": "available", "seat": seat})

@app.route('/thalia/reset')
def reset():
    global wid, sid, did, mrid, oid, tid, cid
    shows.clear()
    orders.clear()
    donations.clear()
    seats.clear()
    sections.clear()
    tickets.clear()
    reports.clear()
    wid = 0  # Shows
    sid = 0  # Sections
    did = 0  # Donations
    mrid = 0  # Reports
    oid = 0  # Orders
    tid = 0  # Tickets
    cid = 0  # Seats
    return json.dumps(''), status.HTTP_200_OK

if __name__ == "__main__":
    init("JSON_files/project-test-theatre-seating.json")
    app.run(port=8080, debug=True)
