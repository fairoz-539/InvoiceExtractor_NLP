import uuid
from flask import Flask, request, jsonify, render_template
import os
import base64
import json
import re
import google.generativeai as genai
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import uuid
import numpy as np

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fairozAhmed'
GEMINI_API_KEY = "AIzaSyAMi-TzsRC3JgZHid2ApRGGMi8lbf79my8"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
UPLOAD_FOLDER = "uploads"
INVOICES_EXCEL_FOLDER = "invoices_excel"
EXCEL_FILE = os.path.join(INVOICES_EXCEL_FOLDER, "invoices.xlsx")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INVOICES_EXCEL_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def extract_info_from_image(image_path):
    image_base64 = encode_image_to_base64(image_path)
    if not image_base64:
        print("Failed to encode image to base64")
        return None

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    Analyze this invoice image and extract all information into a structured JSON object. 
    Include any fields present without enforcing a strict schema. Format numeric values as numbers (not strings). 
    If information is not present, omit the field. Handle multi-line addresses appropriately.
    Return the result as a clean, valid JSON object without surrounding text or markdown.
    """
    try:
        print("Calling Gemini API...")
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_base64}
        ])
        extracted_text = response.text.strip()
        print(f"Gemini API response: {extracted_text[:100]}...")
        parsed_json = parse_response_to_json(extracted_text)
        if parsed_json:
            parsed_json["processed_at"] = datetime.now().isoformat()
            parsed_json["invoice_id"] = str(uuid.uuid4())
            print("Successfully parsed JSON")
        else:
            print("Failed to parse JSON from response")
        return parsed_json
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def parse_response_to_json(response_text):
    try:
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
        if json_match:
            json_str = json_match.group(1).strip()
            return json.loads(json_str)
        cleaned_text = response_text.strip()
        if cleaned_text.startswith('{') and cleaned_text.endswith('}'):
            return json.loads(cleaned_text)
        start_idx = cleaned_text.find('{')
        end_idx = cleaned_text.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = cleaned_text[start_idx:end_idx+1]
            return json.loads(json_content)
        raise ValueError("Could not extract valid JSON from response")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)

def save_to_excel(data):
    if not data:
        print("No data to save to Excel")
        return False

    invoice_data = {k: v for k, v in data.items() if k != 'items'}
    flat_data = flatten_dict(invoice_data)
    invoice_df = pd.DataFrame([flat_data])

    items = data.get('items', []) or []
    items_df = pd.DataFrame(items) if items else pd.DataFrame()
    if not items_df.empty:
        items_df['invoice_id'] = data['invoice_id']

    if os.path.exists(EXCEL_FILE):
        with pd.ExcelFile(EXCEL_FILE) as xls:
            existing_invoices = pd.read_excel(xls, sheet_name='Invoice_Details')
            existing_items = pd.read_excel(xls, sheet_name='Items') if 'Items' in xls.sheet_names else pd.DataFrame()
        
        updated_invoices = pd.concat([existing_invoices, invoice_df], ignore_index=True)
        updated_items = pd.concat([existing_items, items_df], ignore_index=True) if not items_df.empty else existing_items
    else:
        updated_invoices = invoice_df
        updated_items = items_df

    try:
        with pd.ExcelWriter(EXCEL_FILE) as writer:
            updated_invoices.to_excel(writer, sheet_name='Invoice_Details', index=False)
            if not updated_items.empty:
                updated_items.to_excel(writer, sheet_name='Items', index=False)
        print(f"Data appended to: {EXCEL_FILE}")
        return True
    except Exception as e:
        print(f"Error saving to Excel: {str(e)}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(f"Saving uploaded file to: {file_path}")
            file.save(file_path)
            
            extracted_data = extract_info_from_image(file_path)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed temporary file: {file_path}")
                
            if not extracted_data:
                return jsonify({"error": "Failed to extract structured data from the image"}), 500
            
            if not save_to_excel(extracted_data):
                return jsonify({"error": "Failed to save to Excel"}), 500
                
            return jsonify(extracted_data), 200
        except Exception as e:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            print(f"Unexpected error: {str(e)}")
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid file type. Allowed types: jpg, jpeg, png, pdf"}), 400

@app.route('/invoices', methods=['GET'])
def get_invoices():
    try:
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE, sheet_name='Invoice_Details')
            items_df = pd.read_excel(EXCEL_FILE, sheet_name='Items') if 'Items' in pd.ExcelFile(EXCEL_FILE).sheet_names else pd.DataFrame()
            # Replace NaN with None (null in JSON)
            invoices = df.replace({np.nan: None}).to_dict(orient='records')
            items = items_df.replace({np.nan: None}).to_dict(orient='records')
            return jsonify({"invoices": invoices, "items": items}), 200
        return jsonify({"invoices": [], "items": []}), 200
    except Exception as e:
        print(f"Error reading invoices: {str(e)}")
        return jsonify({"error": f"Error reading invoices: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)