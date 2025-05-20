# parking_lot_Analyser

A web application that analyzes parking lot images to determine total parking spaces, occupied spaces, and available spaces.

**Live Demo:** https://parking-lot-analyzer.onrender.com

## Working screenshot:
![Parking Lot](Screenshot%202025-05-20%20at%2011.59.13%E2%80%AFPM.png)

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features

- 📷 **Simple Image Upload:** Drag and drop or click to upload parking lot images
- 🔢 **Automatic Analysis:** Provides counts of total, occupied, and available parking spaces
- 📊 **CSV Export:** Download results as CSV files for further analysis
- 📱 **Responsive Design:** Works on desktop and mobile devices
- 🚗 **Quick Results:** Process images and receive results within seconds

## How It Works

The Parking Lot Analyzer uses a combination of computer vision techniques and predefined parameters to:

1. Accept an uploaded parking lot image
2. Process the image to determine the total number of parking spaces
3. Estimate which spaces are occupied vs. available
4. Generate a CSV file with the analysis results
5. Display statistics to the user

## Project Structure

```
parking-lot-analyzer/
├── app.py                 # Flask application - main entry point
├── parking_detection.py   # Core detection logic
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
├── uploads/               # Temporary storage for uploaded images
├── results/               # Storage for generated CSV files
└── templates/             
    └── index.html         # Web interface template
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/parking-lot-analyzer.git
   cd parking-lot-analyzer
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create required directories:
   ```bash
   mkdir -p uploads results
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. **Upload Image:**
   - Click on the drop zone or drag and drop a parking lot image
   - The image will appear in the preview area

2. **Analyze:**
   - Click the "Analyze Parking Lot" button
   - The application will process the image

3. **View Results:**
   - See total, occupied, and available parking space counts
   - Results are displayed in color-coded cards

4. **Export Data:**
   - Click the "Download CSV Results" button to save the data
   - The CSV file contains total, occupied, and available counts

5. **Analyze Another Image:**
   - Click "Analyze Another Image" to start over

## Code Explanation

### app.py

The main Flask application that:
- Handles HTTP routes and requests
- Processes uploaded images
- Calls the parking detection algorithms
- Generates and serves CSV files

Key functions:
- `index()`: Renders the main page
- `analyze()`: Processes uploaded images and returns results
- `uploaded_file()` and `result_file()`: Serve static files

### parking_detection.py

Contains the core logic for parking space detection:
- `manual_count_based_on_image()`: Analyzes the image to count spaces
- `export_results_to_csv()`: Creates CSV files with parking data

### index.html

The frontend interface featuring:
- Responsive Bootstrap layout
- Drag and drop file upload
- Interactive results display
- Dynamic statistics cards

## Deployment

The application is deployed on Render. You can access it here:

**Live Demo:** https://parking-lot-analyzer.onrender.com

### Deployment Environment

- **Platform:** Render Web Service
- **Runtime:** Python 3.10
- **Framework:** Flask
- **Web Server:** Gunicorn

## Future Improvements

- Implement real-time camera feed analysis
- Add historical data tracking and trending
- Integrate mapping services to locate available parking
- Implement user authentication for private lots
- Add multi-lot management capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


Created by Mekala Jaya nanda prabhas 
