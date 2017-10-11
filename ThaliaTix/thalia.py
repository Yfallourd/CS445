from flask import Flask, request, status
import json

app = Flask(__name__)
#Replace by "database", maybe a conf file
shows = []
sections = []
#Replace by reading a conf file
wid = 0
sid = 0
mrid = 0
oid = 0

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
                shows.remove(dict)
                payload = request.get_json(force=True)
                if checkData(payload, 'POSTshow'):
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
    
@app.route('/shows/<wid>/sections/<sid>', methods=['GET'])
def viewSections(wid, sid):
    showdict = {}
    for dict in shows:
        if dict["wid"] == str(wid):
            showdict = dict
    for dict in sections:
        if dict["section"] == str(sid): #Possible mistake
            if not showdict == {}:
                return {**showdict, **dict}, status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

######### SEATING #########
@app.route('/seating', methods=['POST'])
def createSection():


@app.route('/seating/<sid>', methods=['GET', 'PUT', 'DELETE'])
def editOrRequestSections(sid):
    if request.method == 'GET':
        if(request.args.get('show')):


######### ORDERS #########
@app.route('/orders', methods=['GET', 'PUT')
def viewOrCreateOrders():

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

