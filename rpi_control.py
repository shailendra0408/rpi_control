from flask import Flask , render_template, request
import mysql.connector
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from mysql.connector import errorcode



application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("control_page.html")

@application.route('/tubelightstate',methods = ['GET','POST'])
def tubelightstate():
    if request.method == 'POST': 
        global tubelight_state
        global first_name 
        first_name = "Shailendra"
        tubelight_state = request.form['toggle']
        print tubelight_state
        create_machine_state_table() 
        if tubelight_state == 'on':
            print "turning light on"
            save_tubelight_state(tubelight_state, first_name)
            print "after saving on in the DB" 

        else :
            print "turning light off"
            save_tubelight_state(tubelight_state, first_name) 
            print "after saving off in the DB" 
        return tubelight_state

@application.route('/fanstate',methods = ['GET','POST'])
def fanstate():
    if request.method == 'POST': 
        fan_state_1 = request.form['toggle1']
        print fan_state_1
        if fan_state_1 == 'on':
            print "turning fan on"
        else :
            print "turning fan off"
        return fan_state_1

@application.route('/switch1state',methods = ['GET','POST'])
def switch1state():
    if request.method == 'POST': 
        switch1_state_1 = request.form['switch1_state']
        print switch1_state_1
        if switch1_state_1 == 'on':
            print "turning Switch1 on"
        else :
            print "turning switch1 off"
        return switch1_state_1

@application.route('/coffeemachine',methods = ['GET','POST'])
def coffeemachine():
    if request.method == 'POST':
        first_name = "Shailendra" 
        coffeem_state_1 = request.form['coffeem_state']
        print coffeem_state_1
        if coffeem_state_1 == 'on':
            print "turning coffee machine on"
            save_coffeem_state(first_name, coffeem_state_1)
        else :
            print "turning coffee machine off"
            save_coffeem_state(first_name, coffeem_state_1)
    return coffeem_state_1 
          
def create_machine_state_table():        
    try:
        db_config = read_db_config()
        print db_config
        print db_config['database']
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

        cursor = conn.cursor()
        query ="""CREATE TABLE IF NOT EXISTS home_control (
                  first_name CHAR(20) NOT NULL,
                  tubelight_state VARCHAR(20),
                  fan_state_1 VARCHAR(20),
                  switch1_state_1 VARCHAR(20),
                  coffeem_state_1 VARCHAR(20) )""" 
        cursor.execute(query)
 
        conn.commit()

    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")
     

def save_tubelight_state(tubelight_state, first_name):
    print first_name, tubelight_state
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET tubelight_state=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (tubelight_state,first_name))
        

        conn.commit()
        print "after commit"
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")
  

 

if __name__ == "__main__":
    application.run(host='0.0.0.0')
