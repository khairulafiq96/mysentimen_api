from urllib import response
from flask import Flask, request
import json
import flask
import psycopg2
import calendar

app = Flask(__name__)

def initilizeConnection():
    print("Initializing connection")
    connection = psycopg2.connect("dbname=postgres user=postgres password=admin")
    cursor = connection.cursor()
    return connection, cursor

#https://stackoverflow.com/questions/5067218/get-utc-timestamp-in-python-with-datetime
def convertUTC(dt):
    return calendar.timegm(dt.utctimetuple())

@app.after_request
def handlerCORS(response):
    if(request.method == 'GET' or request.method == 'OPTIONS'):
        print("OK")
        #response = flask.Response()
        response.headers["Status Code"] = "200 OK"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Content-Type"] = "application/json"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "*"     
        response.headers["Access-Control-Allow-Origin"] = "*"

        return response

@app.route('/myHello')
def hello():
    return 'Hello World'

@app.route('/conn')
def initializeConn():
    try:
        print("Initializing connection")
        connection = psycopg2.connect("dbname=postgres user=postgres password=admin")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from mysentimen.politicians"
        cursor.execute(postgreSQL_select_Query)
        
        response = cursor.fetchall()



        return json.dumps(response)

    except(e):
        return e
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/liveVotes', methods=['GET'])
def liveComment():
    try :
       
        connection, cursor  = initilizeConnection()
        data = request.get_json()
        cursor.execute("""select * from mysentimen.votes where politicianid = '%s' """ % data['politicianid'])
        response = cursor.fetchall()

        finalResp = {}

        for row in response:

            finalResp[row[0]]={}
            finalResp[row[0]]['comments'] = row[1]
            finalResp[row[0]]['timestamp'] = convertUTC(row[2])
            finalResp[row[0]]['politicianid'] = row[3]
            finalResp[row[0]]['userid'] = row[4]

            #print (finalResp)
            
        
        return json.dumps(finalResp)

    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")


@app.route('/liveVotes2')
def liveComment2():
    try :
        connection, cursor  = initilizeConnection()
        postgreSQL_select_Query = "select * from mysentimen.votes"
        print("Excecuting Query")
        cursor.execute(postgreSQL_select_Query)
        response = cursor.fetchall()

        finalResp = {}

        for row in response:

            finalResp[row[0]]={}
            finalResp[row[0]]['comments'] = row[1]
            finalResp[row[0]]['timestamp'] = convertUTC(row[2])
            finalResp[row[0]]['politicianid'] = row[3]
            finalResp[row[0]]['userid'] = row[4]

            #print (finalResp)
            
        
        return json.dumps(finalResp)

    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")


@app.route('/getLeaderboard')
def leaderboard():
    try :
        connection, cursor  = initilizeConnection()
        postgreSQL_select_Query = "select * from mysentimen.politicians"
        print("Excecuting Query")
        cursor.execute(postgreSQL_select_Query)
        response = cursor.fetchall()

        finalResp = {}

        for row in response:

            finalResp[row[0]]={}
            finalResp[row[0]]['name'] = row[1]
            finalResp[row[0]]['category'] = row[2]
            finalResp[row[0]]['position'] = row[3]
            finalResp[row[0]]['party'] = row[4]
            finalResp[row[0]]['imgpath'] = row[5]
            finalResp[row[0]]['sentimen'] = row[5]

            #print (finalResp)
            
        
        return json.dumps(finalResp)

    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")
            

if __name__ == '__main__':
    app.run


