from flask import Flask, render_template, request, jsonify
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Keep legacy .html routes working if directly typed
@app.route('/<page>.html')
def html_pages(page):
    try:
        return render_template(f'{page}.html')
    except:
        return "Page not found", 404

# API route for handling the booking form submissions
@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    print(f"New Booking Inquiry Received: {data}")
    
    name = data.get('name')
    phone = data.get('phone')
    service = data.get('service')
    message = data.get('message')
    
    if not all([name, phone, service, message]):
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400
        
    try:
        if os.path.exists('credentials.json'):
            scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                     "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
            
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            client = gspread.authorize(creds)
            
            # Replace 'Shubhotsav Forms' with the EXACT name of your Google Sheet
            sheet = client.open("Shubhotsav Forms").sheet1
            
            # Append the row
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [timestamp_str, name, phone, service, message]
            sheet.append_row(row_data)
            print(f"Successfully pushed {name}'s inquiry to Google Sheets.")
        else:
            print("Error: credentials.json not found! Unable to save submission.")
            return jsonify({
                "success": False,
                "message": "Server configuration error. Please try again later."
            }), 500
            
    except Exception as e:
        print(f"Google Sheets API error: {e}")
        return jsonify({
            "success": False,
            "message": "An error occurred while saving your request. Please try again later."
        }), 500
    
    return jsonify({
        "success": True, 
        "message": "Thank you for reaching out! We have received your inquiry and will get back to you shortly."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
