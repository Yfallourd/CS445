from flask import Flask, request

app = Flask(__name__)

######### SHOWS #########
@app.route('/shows', methods=['GET', 'POST'])
def viewOrCreateShow():
    if request.method == 'GET':

    else:


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

