# Cableway Inspection Report Generator

## Overview
The Cableway Inspection Report Generator is a Python-based GUI application designed to help users generate detailed inspection reports for cableway stations. Users can input inspection data, upload inspection images, and generate a comprehensive PDF report.

## Features
- User-friendly GUI built with Tkinter.
- Scrollable form for entering inspection data.
- Drag and drop interface for uploading images.
- Manual file upload option for images.
- Automated PDF report generation with input data and images.
- Customizable report filename based on station name, number, and date of inspection.

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cableway-inspection-report-generator.git
   cd cableway-inspection-report-generator
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows, use `env\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the application:**
   ```bash
   python cableway_inspection.py
   ```

2. **Fill out the inspection form:**
    - Enter details such as Station Name, Station Number, Inspector Name, and more.
    - Scroll through the form to complete all fields.

3. **Upload images:**
    - Drag and drop images into the designated area.
    - Or click "Browse" to select images manually.

4. **Generate the PDF report:**
    - Click the "Generate Report" button.
    - The report will be saved as a PDF file with a name based on the station name, number, and date.

## Dependencies
- Python 3.x
- tkinter
- tkinterdnd2
- Pillow
- fpdf
- datetime
