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
        tubelight_state_1 = request.form['toggle']
        print tubelight_state_1
        create_machine_state_table() 
        if tubelight_state_1 == 'on':
            print "turning light on"
            save_tubelight_state() #this function is still to be added in the to get the information of state of tubelight and save it in the mysql database

        else :
            print "turning light off"
        return tubelight_state_1

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
        coffeem_state_1 = request.form['coffeem_state']
        print coffeem_state_1
        if coffeem_state_1 == 'on':
            print "turning coffee machine on"
        else :
            print "turning coffee machine off"
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
                  last_name  CHAR(20),
                  email_id VARCHAR(30),   
                  contact_number VARCHAR(15),
                  merchant_id int(11) NOT NULL AUTO_INCREMENT,
                  tbubelight VARCHAR(15),
                  fanstate VARCHAR(15),
                  switch1state VARCHAR(15),
                  coffeemachinestate VARCHAR(15),
                  PRIMARY KEY (`merchant_id`) )""" 
        cursor.execute(query)
 
        conn.commit()

    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")
     

if __name__ == "__main__":
    application.run(host='0.0.0.0')
