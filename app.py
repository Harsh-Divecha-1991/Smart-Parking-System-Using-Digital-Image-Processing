from flask import Flask, flash, render_template, request, jsonify, Response
import sqlite3
import os

# db connection 
ROOT = os.getcwd()
DB_FILE_PATH = os.path.join(ROOT, "Parking.db")

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/callParkingData', methods=['POST'])
def callParkingData():

    if request.method == 'POST':
        
        # db connection 
        connection = sqlite3.connect(DB_FILE_PATH)
        cursor = connection.cursor()
        
        cursor.execute(f'''SELECT * FROM ParkingCount; ''')
        connection.commit()
        result_ParkingCount = cursor.fetchall()
        print('result_ParkingCount : ', result_ParkingCount)

        cursor.execute(f'''SELECT * FROM NumberPlates; ''')
        connection.commit()
        result_NumberPlates = cursor.fetchall()
        print('result_NumberPlates : ', result_NumberPlates)

    return render_template('index.html', ParkingCount=result_ParkingCount, NumberPlates=result_NumberPlates)




if __name__ == '__main__':
    app.run(debug=True) #debug=True