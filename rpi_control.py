import mysql.connector
import json
import sys 
import os
import logging
 
from mysql.connector import MySQLConnection, Error
from flask import Flask , render_template, request, redirect, url_for, escape, session, make_response, request, jsonify  
from python_mysql_dbconfig import read_db_config
from mysql.connector import errorcode
from mqttpubsub.mqttpublish import my_mqtt_publish

#logging configuration
#@todo - need to move it to a configuration file
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('/home/shailendra/test.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

application = Flask(__name__)

#@todo - generate a radom secrete key everytime this application is run 
application.secret_key = "###########################################"

#landing page is this
@application.route("/")
def landing():
    if 'email_id' in session:
        Phone_number = 0
        email_id = session['email_id']
        password = session['password']
        merchant_exist_session = if_merchant_exist(email_id, Phone_number)
        if merchant_exist_session == 1:
            user_validation = verify_user(email_id,password)
            if user_validation == 1:
                return redirect(url_for('hello'))
    else:
        logger.debug("No user in this session")
        error_msg_1 = "No user in this session, please login"
        error = {'error':error_msg_1}
        return render_template("index.html", user = error )
        #return response

#@application.route("/index")
#def index():
#    return render_template('index.html')

#login function here, user will be asked to enter his details 
@application.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_id = 0
        password = 0
        mechant_exist_login = 0
        contact_number = 0
        logger.debug("inside login") 
        session['email_id'] = request.form['email_id']
        session['password'] = request.form['password']
        email_id = request.form['email_id']
        password = request.form['password']
        logger.debug('email id is %s and Password is %s',email_id, password)
        merchant_exist_login = if_merchant_exist(email_id, contact_number)
        if merchant_exist_login == 1:
            user_verification = verify_user(email_id,password)
            if user_verification == 1:
                return redirect(url_for('hello'))
            else:
                
                error_msg = "Login and password didn't macthed, please try again"
                user = {'error':error_msg}
                return render_template('index.html',user = user)
    else:
        print "No user data in session"
        response = make_response(redirect('/index'))
        return response
          

@application.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template ("index.html", user="")



#route need to be changed here
@application.route("/controlpage")
def hello():
    first_name="Shailendra"
    home_appliance_state = get_appliance_state(first_name) 
    return render_template("control_page.html" ,user = json.dumps(home_appliance_state))

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
            logger.info("turning light ON")
            save_tubelight_state(tubelight_state, first_name)
            logger.info("After saving ON in the DB")
            my_mqtt_publish("appliance/state","tubelight:ON")
        else :
            logger.info("turning light off")
            save_tubelight_state(tubelight_state, first_name) 
            logger.info("After saving OFF in the DB")
            my_mqtt_publish("appliance/state","tubelight:OFF")
 
        return redirect(url_for('hello'))

@application.route('/fanstate',methods = ['GET','POST'])
def fanstate():
    if request.method == 'POST':
        global fan_state_1
        first_name="Shailendra"
        fan_state_1 = request.form['toggle1']
        print fan_state_1
        if fan_state_1 == 'on':
            logger.info("Turning FAN ON")
            save_fan_state(fan_state_1,first_name)
            my_mqtt_publish("appliance/state","fan:ON") 
        else :
            logger.info("Turning FAN OFF")
            save_fan_state(fan_state_1,first_name)
            my_mqtt_publish("appliance/state","fan:OFF") 
        return redirect(url_for('hello'))

@application.route('/switch1state',methods = ['GET','POST'])
def switch1state():
    if request.method == 'POST':
        global switch1_state_1
        first_name = "Shailendra" 
        switch1_state_1 = request.form['switch1_state']
        print switch1_state_1
        if switch1_state_1 == 'on':
            logger.info("Turning Switch1 ON")
            save_switch1_state(switch1_state_1,first_name)
            my_mqtt_publish("appliance/state","switch1:ON") 
        else :
            logger.info("turning Switch1 OFF")
            save_switch1_state(switch1_state_1,first_name)
            my_mqtt_publish("appliance/state","switch:OFF") 
        return redirect(url_for('hello'))

@application.route('/coffeemachine',methods = ['GET','POST'])
def coffeemachine():
    if request.method == 'POST':
        first_name = "Shailendra"
        global coffeem_state_1
        coffeem_state_1 = request.form['coffeem_state']
        print coffeem_state_1
        if coffeem_state_1 == 'on':
            logger.info("turning coffee machine ON")
            save_coffeem_state(coffeem_state_1,first_name)
            my_mqtt_publish("appliance/state","coffeem:ON") 
        else :
            logger.info("turning coffee machine ON")
            save_coffeem_state(coffeem_state_1,first_name)
            my_mqtt_publish("appliance/state","coffeem:OFF") 
    return  redirect(url_for('hello'))
          
def create_machine_state_table():        
    try:
        db_config = read_db_config()
        print db_config
        print db_config['database']
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.info("Inside create machine state table fuction, connection established")
        else:
            logger.info("Connection failed")

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
    logger.info("Inside  save_tubellight_state function")
    logger.info("First_name : %s and Tubelight_state : %s",first_name, tubelight_state)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.debug('connection established.')
        else:
            logger.info("connection failed")
            print('connection failed.')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET tubelight_state=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (tubelight_state,first_name))
        

        conn.commit()
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        logger.info("connection closed for save_tubloght_state_function")

def save_fan_state(fan_state_1, first_name):
    logger.info("Inside  save_fan_state function")
    logger.info("First_name : %s and fan_state_1 : %s",first_name, fan_state_1)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.debug('connection established.')
        else:
            logger.debug('connection failed')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET fan_state_1=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (fan_state_1,first_name))
        

        conn.commit()
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        logger.info("Connection closed for save_fan_state function")
        print ("connection closed.")
  

def save_coffeem_state(coffeem_state_1, first_name):
    logger.info("Inside  save_coffem_state function")
    logger.info("First_name : %s and coffem_state_1 : %s",first_name, coffeem_state_1)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.debug('connection established.')
        else:
            logger.debug('connection failed')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET coffeem_state_1=%s WHERE first_name=%s"""
        #print query 
        cursor.execute(query, (coffeem_state_1,first_name))
        

        conn.commit()
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        loggger.info("Connection closed for save_coffeem_state function")

def save_switch1_state(switch1_state_1, first_name):
    logger.info("Inside  save_switch1_state function")
    logger.info("First_name : %s and Switch1_state_1 : %s",first_name, switch1_state_1)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.debug('connection established.')
        else:
            logger.debug('connection failed')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET switch1_state_1=%s WHERE first_name=%s"""
        #print query 
        cursor.execute(query, (switch1_state_1,first_name))
        

        conn.commit()
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        logger.info("Connection closed for save_switch1_state function")

#@todo - need to create a admin page, where you can cretae user, as this is only admin controlled app.
def get_appliance_state(first_name):
    logger.debug("in get_appliance_state function") 
    #print "in get_appliance_state function"
    Name = 0
    tubelightstate = 0
    fanstate = 0
    switch1state = 0
    coffeemstate = 0
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        logger.debug("trying inside get_appliance_state function")
        print ('Trying')
        if conn.is_connected():
            logger.debug('connection established.')
        else:
            logger.debug('connection failed')
        
        cursor = conn.cursor(buffered=True) 
        query ="""SELECT * FROM home_control WHERE first_name = %s"""
        cursor.execute(query, (first_name,))  
        rows_count = cursor.rowcount
        #print rows_count
        if rows_count > 0:
            result_set = cursor.fetchall()
            #print result_set
            for row in result_set:
                Name = row[0]
                tubelightstate=row[1]
                fanstate=row[2]
                switch1state=row[3]
                coffeemstate=row[4]
                logger.debug("Name : %s , tubelightstate :%s , fanstate : %s, switch1state :%s , coffeemstate : %s", Name, tubelightstate,fanstate,switch1state,coffeemstate)
                home_appliance_data = {"Tubelight_state":tubelightstate,"Fan_state":fanstate,"Switch1_state":switch1state,"coffeem_state":coffeemstate                }
                logger.debug("Printing dictionary : %s", home_appliance_data)
                return home_appliance_data
                
        else:
            logger.debug("No rows in get_home_appluinace_state_data")
            print "no rows"
            return 0
        
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
            conn.commit()

    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.") 


def if_merchant_exist(email_id, contact_number):
    logger.info("Email Id {0} and contact_number is {1}".format(email_id, contact_number))
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            logger.info("connection established with DB")
        else:
            logger.info("connection fialed with DB")
        
        cursor = conn.cursor(buffered=True)
        query ="""SELECT * FROM merchant_registration_table WHERE email_id = %s OR contact_number = %s""" 
        cursor.execute(query, (email_id,contact_number))
        rows_count = cursor.rowcount
        #print rows_count
        if rows_count > 0:
            result_set = cursor.fetchall()
            logger.debug('user matched')
            logger.debug("result_set is : %s",result_set)
            #print result_set
            return 1
            
        else:
            logger.debug("user not found")
            return 0

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
            conn.commit()

    except Error as error:
        logger.error(error)
        
    finally:
        cursor.close()
        conn.close()
        logger.info("connection closed")
         
def verify_user(email_id, password):
    logger.info("in verify user function")
    logger.info("Email id is: %s and password is : %s", email_id, password)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        #print ('Trying')
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor(buffered=True)
        query ="""SELECT * FROM merchant_registration_table WHERE email_id = %s""" 
        cursor.execute(query, (email_id,))
        rows_count = cursor.rowcount
        #print "printing rows count"
        #print rows_count
        if rows_count > 0:
            logger.info("There are rows in the table - not empty")
            result_set = cursor.fetchall()
            for row in result_set:
                entered_password = row[3]
                logger.debug('entered password is : %s',password)
                if str(entered_password) == password:
                    logger.debug("password matched")
                    return 1
                else:
                    logger.debug("password didn't matched")
                    return 0
        else:
            return 0
            logger.error("There are no rows in the table")

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
            conn.commit()

    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")    


if __name__ == "__main__":
    application.run(host='0.0.0.0')
