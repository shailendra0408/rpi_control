from flask import Flask , render_template, request
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("control_page.html")

@application.route('/tubelightstate',methods = ['GET','POST'])
def tubelightstate():
    if request.method == 'POST': 
        tubelight_state_1 = request.form['toggle']
        print tubelight_state_1
        if tubelight_state_1 == 'on':
            print "turning light on"
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
        switch1_state_1 = request.form['swicth1_state']
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
    return None 
          
     

if __name__ == "__main__":
    application.run(host='0.0.0.0')
