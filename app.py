from flask import Flask, render_template, request, jsonify, session
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import io
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('criminal_database', exist_ok=True)

# Criminal database (in production, use a proper database)
CRIMINAL_DB_FILE = 'criminal_database/criminals.json'

def load_criminal_database():
    """Load criminal database from JSON file"""
    if os.path.exists(CRIMINAL_DB_FILE):
        with open(CRIMINAL_DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_criminal_database(criminals):
    """Save criminal database to JSON file"""
    with open(CRIMINAL_DB_FILE, 'w') as f:
        json.dump(criminals, f, indent=2)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def detect_faces(image_path):
    """Detect faces in image using OpenCV"""
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        face_data = []
        for (x, y, w, h) in faces:
            face_data.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'confidence': 0.9  # Placeholder confidence
            })
        
        return face_data
    except Exception as e:
        print(f"Error detecting faces: {e}")
        return []

def compare_faces(face1_path, face2_path):
    """Simple face comparison (placeholder - replace with actual face recognition)"""
    # This is a placeholder. In production, use proper face recognition models
    # like face_recognition library or insightface
    try:
        img1 = cv2.imread(face1_path)
        img2 = cv2.imread(face2_path)
        
        if img1 is None or img2 is None:
            return 0.0
        
        # Resize images to same size for comparison
        img1 = cv2.resize(img1, (100, 100))
        img2 = cv2.resize(img2, (100, 100))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate similarity (simple pixel difference)
        diff = cv2.absdiff(gray1, gray2)
        similarity = 1 - (np.mean(diff) / 255.0)
        
        return similarity
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return 0.0

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and face detection"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if file and allowed_file(file.filename):
            # Save uploaded image
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Detect faces
            faces = detect_faces(filepath)
            
            if not faces:
                return jsonify({
                    'success': True,
                    'message': 'No faces detected in the image',
                    'faces': [],
                    'image_path': filepath
                })
            
            # Check against criminal database
            criminals = load_criminal_database()
            results = []
            
            for face in faces:
                # Extract face region
                img = cv2.imread(filepath)
                x, y, w, h = face['x'], face['y'], face['width'], face['height']
                face_img = img[y:y+h, x:x+w]
                
                # Save face image
                face_filename = f"face_{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
                face_path = os.path.join(app.config['UPLOAD_FOLDER'], face_filename)
                cv2.imwrite(face_path, face_img)
                
                # Compare with criminal database
                best_match = None
                best_similarity = 0.0
                
                for criminal in criminals:
                    similarity = compare_faces(face_path, criminal['image_path'])
                    if similarity > best_similarity and similarity > 0.7:  # Threshold
                        best_similarity = similarity
                        best_match = criminal
                
                face_result = {
                    'bbox': face,
                    'face_path': face_path,
                    'is_criminal': best_match is not None,
                    'criminal_info': best_match,
                    'similarity': best_similarity
                }
                results.append(face_result)
            
            return jsonify({
                'success': True,
                'message': f'Detected {len(faces)} face(s)',
                'faces': results,
                'image_path': filepath
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_criminal', methods=['POST'])
def add_criminal():
    """Add a new criminal to the database"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        name = request.form.get('name', 'Unknown')
        crime = request.form.get('crime', 'Unknown')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"criminal_{timestamp}_{uuid.uuid4().hex[:8]}_{filename}"
            filepath = os.path.join('criminal_database', unique_filename)
            file.save(filepath)
            
            # Detect faces in criminal image
            faces = detect_faces(filepath)
            
            if not faces:
                return jsonify({'error': 'No faces detected in criminal image'}), 400
            
            # Add to database
            criminals = load_criminal_database()
            criminal_data = {
                'id': str(uuid.uuid4()),
                'name': name,
                'crime': crime,
                'image_path': filepath,
                'added_date': datetime.now().isoformat(),
                'face_count': len(faces)
            }
            
            criminals.append(criminal_data)
            save_criminal_database(criminals)
            
            return jsonify({
                'success': True,
                'message': f'Criminal {name} added successfully',
                'criminal': criminal_data
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/criminals')
def list_criminals():
    """List all criminals in database"""
    criminals = load_criminal_database()
    return jsonify(criminals)

@app.route('/delete_criminal/<criminal_id>', methods=['DELETE'])
def delete_criminal(criminal_id):
    """Delete a criminal from database"""
    try:
        criminals = load_criminal_database()
        criminal = next((c for c in criminals if c['id'] == criminal_id), None)
        
        if criminal:
            # Remove image file
            if os.path.exists(criminal['image_path']):
                os.remove(criminal['image_path'])
            
            # Remove from database
            criminals = [c for c in criminals if c['id'] != criminal_id]
            save_criminal_database(criminals)
            
            return jsonify({'success': True, 'message': 'Criminal deleted successfully'})
        
        return jsonify({'error': 'Criminal not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 