# Cableway Inspection Report App

## Overview
The **Cableway Inspection Report App** is a Python-based application that provides a graphical user interface (GUI) for generating cableway inspection reports. The app allows users to input inspection details, upload images, and generate a formatted PDF report.

## Features
- **GUI built with Tkinter**: An interface used for entering inspection data.
- **Drag and Drop Image Upload**: Supports dropping image files directly into the application.
- **Manual Image Selection**: Browse and select images from your file system.
- **Dynamic Form Input**: Users can enter details about general inspection and cable-specific data.
- **Automated PDF Generation**: Creates a structured, professional report including the entered data and images.
- **Scrollable Input Form**: Easily navigate through all required fields.

## Installation

### Prerequisites
Ensure you have Python installed on your system. The required dependencies can be installed using the provided `requirements.txt` file.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/JustinSRao/Cableway-Inspection-Report-App.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Cableway-Inspection-Report-App
   ```
3. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the application using the following command:
```sh
python cableway_inspection.py
```

### Steps to Generate a Report
1. Open the application.
2. Fill in the **General Data** and **Cable Data** sections.
3. Upload images by dragging and dropping or clicking **Browse**.
4. Click **Generate Report** to create and save a PDF file.


## Dependencies
This project uses the following Python libraries:
- `tkinter` – GUI development
- `tkinterdnd2` – Drag and drop functionality
- `PIL` (Pillow) – Image processing
- `fpdf` – PDF generation
- `datetime` – Timestamp management

Install all dependencies using:
```sh
pip install -r requirements.txt
```