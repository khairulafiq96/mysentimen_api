from cmath import e
from urllib import response
from flask import Flask
import json
import psycopg2

app = Flask(__name__)

def initilizeConnection():
    print("Initializing connection")
    connection = psycopg2.connect("dbname=postgres user=postgres password=admin")
    cursor = connection.cursor()
    return connection, cursor


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

    except(e):
        return e
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Commection is closed")
            

if __name__ == '__main__':
    app.run


