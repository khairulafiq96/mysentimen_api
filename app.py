from urllib import response
from flask import Flask, request
import json
import psycopg2
import calendar
import os

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def initilizeConnection():
    print("Initializing connection")
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()
    return connection, cursor

#https://stackoverflow.com/questions/5067218/get-utc-timestamp-in-python-with-datetime
def convertUTC(dt):
    return calendar.timegm(dt.utctimetuple())

def convertSentimen(sentimen):
    score = round((float(sentimen) *100), 3 )
    'print(type(sentimen))'
    return score

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
        #print(data)
        cursor.execute("""select * from public.users where id = '%s' """ % data['id'])
        response = cursor.fetchall()
        #print(type(response))

        if response:
            print("User account has been created")
        else:
            print("Creating new account")
            cursor.execute("insert into public.users(id, name, email) values ('%s', '%s', '%s')"%(data['id'], data['name'], data['email']))
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

        #print("Politicians ID")
        #print(data['politicianid'])
        #print(data)
        cursor.execute("""select * from public.votes where politicianid = '%s' order by timestamp desc""" % data['politicianid'])
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

@app.route('/postVotes', methods=['POST'])
def func_postVotes():
    try :
        connection, cursor  = initilizeConnection()
        data = request.get_json()
        #print(data)
        #print("insert into mysentimen.votes(comments, politicianid, userid, sentimen) values ('%s', '%s', '%s', '%s')"%(data['comments'], data['politicianid'], data['userid'], data['sentimen']))
        cursor.execute("insert into public.votes(comments, politicianid, userid, sentimen) values ('%s', '%s', '%s', %s)"%(data['comments'], data['politicianid'], data['userid'], data['sentimen']))
        connection.commit()

        cursor.execute("select * from public.votes where comments = '%s' and userid = '%s' and politicianid= '%s'"%(data['comments'],data['userid'],data['politicianid']) )
        #print("select * from mysentimen.votes where comments = '%s' and userid = '%s' and politicianid= '%s'"%(data['comments'],data['userid'],data['politicianid']))
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
        postgreSQL_select_Query = "select * from public.politicians ORDER BY sentimen DESC"
        print("Excecuting Query")
        cursor.execute(postgreSQL_select_Query)
        response = cursor.fetchall()

        finalResp = {}
        rank=0

        for row in response:

            rank += 1

            finalResp[row[0]]={}
            finalResp[row[0]]['rank'] = rank
            finalResp[row[0]]['name'] = row[1]
            finalResp[row[0]]['category'] = row[2]
            finalResp[row[0]]['position'] = row[3]
            finalResp[row[0]]['party'] = row[4]
            finalResp[row[0]]['imgpath'] = row[5]
            finalResp[row[0]]['sentimen'] = convertSentimen(row[6])

            #print (finalResp)
            
        
        return json.dumps(finalResp)

    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")


@app.route('/getLeaderboardDetails')
def func_leaderboardDetails():
    try :
        connection, cursor  = initilizeConnection()
        postgreSQL_select_Query = "select * from public.politicians"
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
            finalResp[row[0]]['sentimen'] = row[6]

            #print (finalResp)
            
        
        return json.dumps(finalResp)

    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")




@app.route('/politicianScorebyDay', methods=['GET', 'POST'])
def func_calcPoliticianScorebyDay():
    try :
        connection, cursor  = initilizeConnection()
        data = request.get_json()
        #print(data['politicianid'])
        cursor.execute("""SELECT
                            (((SELECT count(*) from public.votes WHERE 
                                    sentimen = true AND timestamp >= NOW() - '1 day'::INTERVAL AND politicianid = '%s')*1.00)-
                               (SELECT count(*) from public.votes WHERE 
                                    sentimen = false AND timestamp >= NOW() - '1 day'::INTERVAL AND politicianid = '%s')) / 
                            (NULLIF((SELECT count(*) from public.votes WHERE timestamp >= NOW() - '1 hour'::INTERVAL AND politicianid = '%s'), 0)) 
                                as Sentimen """%(data['politicianid'], data['politicianid'],data['politicianid']))
        response = cursor.fetchall()

        finalResp = {}

        for row in response:
            #print(row[0])
            #Checking if the SQL server return (None,)
            if(row[0]):
                score = round((row[0] *100), 3 )
                finalResp[data['politicianid']]={}
                finalResp[data['politicianid']]['sentimen'] = str(score)
            else :
                finalResp[data['politicianid']]={}
                finalResp[data['politicianid']]['sentimen'] = 'null'
                
        
        #print(finalResp)

        return json.dumps(finalResp)
        
    except Exception as e:
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")


@app.route('/politicianUpdateSentimen', methods=['GET', 'POST'])
def func_calcPoliticianDetail():
    try :
        connection, cursor  = initilizeConnection()
        data = request.get_json()
        #print(data['politicianid'])
        cursor.execute("""SELECT
                            (((SELECT count(*) from public.votes WHERE 
                                    sentimen = true AND politicianid = '%s')*1.00)-
                               (SELECT count(*) from public.votes WHERE 
                                    sentimen = false AND politicianid = '%s')) / 
                            (NULLIF((SELECT count(*) from public.votes WHERE politicianid = '%s'), 0)) 
                                as Sentimen """%(data['politicianid'], data['politicianid'],data['politicianid']))
        response = cursor.fetchall()

        finalResp = {}

        for row in response:
            #print(row[0])
            #Checking if the SQL server return (None,)
            if(row[0]):
                score = round((row[0] *100), 3 )
                finalResp[data['politicianid']]={}
                finalResp[data['politicianid']]['sentimen'] = str(score)
            else :
                finalResp[data['politicianid']]={}
                finalResp[data['politicianid']]['sentimen'] = 'null'
                
        
        print(finalResp)

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


