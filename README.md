# Criminal Face Recognition System

A web-based application that uses computer vision and face detection to identify known criminals from uploaded images.

## Features

- **Face Detection**: Automatically detects faces in uploaded images using OpenCV
- **Criminal Database**: Maintain a database of known criminals with their photos and crime details
- **Real-time Recognition**: Compare detected faces against the criminal database
- **Modern UI**: Responsive web interface with drag-and-drop functionality
- **Secure File Handling**: Safe file uploads with validation

## Screenshots

- **Main Interface**: Clean, modern design with intuitive controls
- **Face Recognition**: Real-time analysis with visual results
- **Criminal Management**: Add, view, and delete criminal records
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project files**

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv env
   
   # On Windows:
   env\Scripts\activate
   
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### Face Recognition

1. **Upload Image**: Drag and drop an image or click to browse
2. **Analyze**: Click "Analyze Image" to process the photo
3. **View Results**: See detected faces and criminal matches

### Managing Criminal Database

1. **Add Criminal**:
   - Enter name and crime details
   - Upload a clear photo of the person
   - Click "Add Criminal"

2. **View Database**: See all criminals in the database
3. **Delete Records**: Remove criminals using the delete button

## How It Works

1. **Face Detection**: Uses OpenCV's Haar Cascade classifier to detect faces
2. **Image Processing**: Extracts face regions and normalizes them
3. **Comparison**: Compares detected faces against the criminal database
4. **Results**: Provides similarity scores and criminal information

## Technical Details

- **Backend**: Flask web framework
- **Computer Vision**: OpenCV for face detection
- **Image Processing**: PIL/Pillow for image manipulation
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Storage**: JSON-based file storage (can be upgraded to database)

## File Structure

```
criminal-face-recognition/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main web interface
├── uploads/              # Temporary uploaded images
├── criminal_database/    # Criminal images and database
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Considerations

- File type validation for uploads
- Secure filename handling
- Maximum file size limits
- Input sanitization

## Limitations

- **Basic Face Recognition**: Currently uses simple pixel comparison
- **Accuracy**: May have false positives/negatives
- **Database**: JSON-based storage (not suitable for production)

## Future Improvements

- **Advanced AI Models**: Integrate with face_recognition or insightface libraries
- **Database**: Use PostgreSQL or MongoDB for better performance
- **API**: RESTful API for mobile applications
- **Real-time**: WebSocket support for live video feeds
- **Authentication**: User login and role-based access
- **Logging**: Comprehensive audit trails

## Troubleshooting

### Common Issues

1. **"No module named 'cv2'"**:
   ```bash
   pip install opencv-python
   ```

2. **Port already in use**:
   ```bash
   # Change port in app.py or kill existing process
   python app.py --port 5001
   ```

3. **Permission errors**:
   - Ensure write permissions for upload directories
   - Run with appropriate user privileges

### Performance Tips

- Use smaller images for faster processing
- Optimize criminal database images
- Consider using GPU acceleration for OpenCV

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the code comments
- Open an issue on the repository

---

**Note**: This is a demonstration system. For production use, implement proper security measures, use advanced face recognition models, and consider legal and privacy implications. 