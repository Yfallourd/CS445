from flask import Flask, request
import json

app = Flask(__name__)
#Replace by "database", maybe a conf file
shows = []
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
    else:
        payload = request.get_json(force=True)
        if checkData(payload, 'POSTshow'):
            wid +=1
            dictpayload = json.loads(payload)
            dictpayload["wid"] = str(wid)
            shows.append(dictpayload)
            return json.dumps({'wid': str(wid)})


@app.route('/shows/<wid>', methods=['GET', 'PUT', 'DELETE'])
def editShow(wid):

@app.route('/shows/<wid>/sections', methods=['GET'])
def viewSections(wid):


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

