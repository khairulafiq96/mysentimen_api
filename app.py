from urllib import response
from flask import Flask, request
import json
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
    if(request.method == 'GET' or request.method == 'OPTIONS' or request.method == 'POST'):
        print("OK")
        #response = flask.Response()
        response.headers["Status Code"] = "200 OK"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Content-Type"] = "application/json"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"     
        response.headers["Access-Control-Allow-Origin"] = "*"

        return response

@app.route('/myHello')
def hello():
    return 'Hello World'

@app.route('/verifyUserDB', methods=['GET', 'POST'])
def func_verifyUserDB():
    try :
        connection, cursor  = initilizeConnection()
        data = request.get_json()
        print(data)
        cursor.execute("""select * from mysentimen.users where id = '%s' """ % data['id'])
        response = cursor.fetchall()
        #print(type(response))

        if response:
            print("User account has been created")
        else:
            print("Creating new account")
            cursor.execute("insert into mysentimen.users(id, name, email) values ('%s', '%s', '%s')"%(data['id'], data['name'], data['email']))
            connection.commit()

            #return json.dumps("New User account has been created in the DB")

        return json.dumps({'mysentimendb' :  'true'})
        
    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")

@app.route('/liveVotes', methods=['GET', 'POST'])
def liveComment():
    try :
       
        connection, cursor  = initilizeConnection()
        #get data from body
        #data = request.get_json()

        #get all headers
        data = request.headers

        print("Politicians ID")
        #print(data['politicianid'])
        print(data)
        cursor.execute("""select * from mysentimen.votes where politicianid = '%s' """ % data['politicianid'])
        response = cursor.fetchall()

        finalResp = {}

        for row in response:

            finalResp[row[0]]={}
            finalResp[row[0]]['comments'] = row[1]
            finalResp[row[0]]['timestamp'] = convertUTC(row[2])
            finalResp[row[0]]['politicianid'] = row[3]
            finalResp[row[0]]['userid'] = row[4]
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


