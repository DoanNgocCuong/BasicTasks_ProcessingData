# FILE NÀY DÙNG ĐỂ Đóng gói file larkbaseOperations_ClassNoASYNC.py và confi.py thành 1 API ENDPOINT

from flask import Flask, jsonify  # Import Flask and jsonify
from config import APP_DOANNGOCCUONG_ID, APP_DOANNGOCCUONG_SECRET, APP_BASE_TOKEN, BASE_TABLE_ID

app = Flask(__name__)  # Create a Flask app

@app.route('/api/data', methods=['GET'])  # Define an API endpoint
def get_data():
    # Here you can add logic to fetch or process data
    data = {
        "config": {
            "id": APP_DOANNGOCCUONG_ID,
            "secret": APP_DOANNGOCCUONG_SECRET,
            "token": APP_BASE_TOKEN,
            "table_id": BASE_TABLE_ID
        },
        "records": [
            {
                "fields": {
                    "user_name": "Example Text 1",
                    "stt_question": 1
                }
            },
            {
                "fields": {
                    "user_name": "Example Text 2",
                    "stt_question": 2
                }
            }
        ]
    }
    return jsonify(data)  # Return data as JSON

if __name__ == '__main__':
    app.run(debug=True)  # Run the app