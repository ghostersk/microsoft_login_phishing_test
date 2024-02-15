import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
# pip install flask-cors
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
CORS(app) 


CSV_FILENAME = 'data.csv'  # Adjust the filename as needed

def get_uk_timestamp():
    # Get the current time in the UK timezone
    uk_timezone = timezone(timedelta(hours=0))
    uk_time = datetime.now(uk_timezone)
    return uk_time.strftime('%Y-%m-%d %H:%M:%S')

def write_to_csv(data):
    data['timestamp'] = get_uk_timestamp()  # Add timestamp to the data
    with open(CSV_FILENAME, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'email', 'password_length', 
            'has_upper_case', 'has_lower_case', 'has_number', 'has_special_char']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty and write header if needed
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write data to CSV file
        writer.writerow(data)

@app.route('/mscheck', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    # Access the data
    email = data.get('email')
    password_length = data.get('passwordLength')
    has_upper_case = data.get('hasUpperCase')
    has_lower_case = data.get('hasLowerCase')
    has_number = data.get('hasNumber')
    has_special_char = data.get('hasSpecialChar')

    # Write data to CSV file
    write_to_csv({
        'email': email,
        'password_length': password_length,
        'has_upper_case': has_upper_case,
        'has_lower_case': has_lower_case,
        'has_number': has_number,
        'has_special_char': has_special_char
    })
    # Return a response
    return jsonify({"message": 200})

if __name__ == '__main__':
    app.run(debug=True)