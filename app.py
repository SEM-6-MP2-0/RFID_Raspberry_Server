from flask import Flask,request,jsonify
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()
app = Flask(__name__)
Unique_roll_no = set()


@app.route('/')
def index():
    return "Hello"

@app.route('/take',methods=['GET','POST'])
def take_attendance():
    if request.method == 'POST':
        return "GET Attendance"
    try:
        print("API HIT Take Attendance")
        t_end = time.time()+20*1
        while t_end > time.time():
            print("")
            id, text = reader.read()
            #print(id)
            Unique_roll_no.add(text.replace('!','').replace('(','').replace(')','').replace('$','').strip())
            print(text)
        if '' in Unique_roll_no: Unique_roll_no.remove('')
        print("All Attendance",Unique_roll_no)
        GPIO.cleanup()
        return jsonify(data=list(Unique_roll_no))

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    app.run(debug=True)
