from flask import Flask, render_template, request, jsonify
import os
import requests
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
    email = data.get('email')
    phone = data.get('phone')
    service = data.get('service')
    message = data.get('message')
    
    if not all([name, email, phone, service, message]):
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400
        
    try:
        # -------------------------------------------------------------------
        # Google Form Submission Details
        # -------------------------------------------------------------------
        GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdGThPjhw8ajy6VI4rtEhqBLyZRAOcqw8jXL95oxVQhvgGwZg/formResponse"
        
        # Form field 'name' attributes (the "entry.XXXXX" IDs)
        form_data = {
            "emailAddress": email,         # User's actual email
            "entry.1357029353": name,      # Name
            "entry.566394827": phone,     # Phone
            "entry.1012819661": service,   # Service
            "entry.1883359612": message    # Message
        }
        
        if GOOGLE_FORM_URL == "YOUR_GOOGLE_FORM_URL_HERE":
            print("Notice: Google Form URL not configured yet. Saving entry locally to console.")
            print(f"Submission Data: {name}, {phone}, {service}, {message}")
        else:
            response = requests.post(GOOGLE_FORM_URL, data=form_data)
            if response.status_code == 200:
                print(f"Successfully pushed {name}'s inquiry to Google Forms.")
            else:
                print(f"Warning: Google Forms returned status code {response.status_code}")
                
    except Exception as e:
        print(f"Google Forms API error: {e}")
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
