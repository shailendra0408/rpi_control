from flask import Flask , render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from mysql.connector import errorcode



application = Flask(__name__)

@application.route("/")
def hello():
    first_name="Shailendra"
    home_appliance_state = get_appliance_state(first_name)
    return render_template("control_page.html", user = home_appliance_state)

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
        return redirect(url_for('hello'))

@application.route('/fanstate',methods = ['GET','POST'])
def fanstate():
    if request.method == 'POST':
        global fan_state_1
        first_name="Shailendra"
        fan_state_1 = request.form['toggle1']
        print fan_state_1
        if fan_state_1 == 'on':
            print "turning fan on"
            save_fan_state(fan_state_1,first_name)
        else :
            print "turning fan off"
            save_fan_state(fan_state_1,first_name)
        return fan_state_1

@application.route('/switch1state',methods = ['GET','POST'])
def switch1state():
    if request.method == 'POST':
        global switch1_state_1
        first_name = "Shailendra" 
        switch1_state_1 = request.form['switch1_state']
        print switch1_state_1
        if switch1_state_1 == 'on':
            print "turning Switch1 on"
            save_switch1_state(switch1_state_1,first_name)
        else :
            print "turning switch1 off"
            save_switch1_state(switch1_state_1,first_name)
        return switch1_state_1

@application.route('/coffeemachine',methods = ['GET','POST'])
def coffeemachine():
    if request.method == 'POST':
        first_name = "Shailendra"
        global coffeem_state_1
        coffeem_state_1 = request.form['coffeem_state']
        print coffeem_state_1
        if coffeem_state_1 == 'on':
            print "turning coffee machine on"
            save_coffeem_state(coffeem_state_1,first_name)
        else :
            print "turning coffee machine off"
            save_coffeem_state(coffeem_state_1,first_name)
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

def save_fan_state(fan_state_1, first_name):
    print first_name, fan_state_1
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET fan_state_1=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (fan_state_1,first_name))
        

        conn.commit()
        print "after commit"
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")
  

def save_coffeem_state(coffeem_state_1, first_name):
    print first_name, coffeem_state_1
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET coffeem_state_1=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (coffeem_state_1,first_name))
        

        conn.commit()
        print "after commit"
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.")

def save_switch1_state(switch1_state_1, first_name):
    print first_name, switch1_state_1
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor()
        query ="""UPDATE home_control SET switch1_state_1=%s WHERE first_name=%s"""
        print query 
        cursor.execute(query, (switch1_state_1,first_name))
        

        conn.commit()
        print "after commit"
    except Error as error:
        print(error)
        
    finally:
        cursor.close()
        conn.close()
        print ("connection closed.") 

def get_appliance_state(first_name):
    print "in get_appliance_state function"
    Name = 0
    tubelightstate = 0
    fanstate = 0
    switch1state = 0
    coffeemstate = 0
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        print ('Trying')
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        
        cursor = conn.cursor(buffered=True) 
        query ="""SELECT * FROM home_control WHERE first_name = %s"""
        cursor.execute(query, (first_name,))  
        rows_count = cursor.rowcount
        print rows_count
        if rows_count > 0:
            result_set = cursor.fetchall()
            print result_set
            for row in result_set:
                Name = row[0]
                tubelightstate=row[1]
                fanstate=row[2]
                switch1state=row[3]
                coffeemstate=row[4]
                print Name
                print tubelightstate
                print fanstate
                print switch1state 
                print coffeemstate 
                home_appliance_data = {'Tubelight_state':tubelightstate,'Fan_state':fanstate,'Switch1_state':switch1state,'coffeem_state':coffeemstate                }
                print "dictionay "
                print home_appliance_data 
                return home_appliance_data
                
        else:
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

if __name__ == "__main__":
    application.run(host='0.0.0.0')
