# QR Code Office Attendance System

A lightweight, modular QR attendance system designed for local PC testing and Raspberry Pi 3 Model B+ deployment.

## Folder Structure
- `app.py`: Main Flask web application and routes.
- `utils.py`: Helper functions for network IP detection, QR generation, and CSV logging.
- `templates/`: Separate HTML templates for the Kiosk screen, Employee Check-In, and Admin Dashboard.
- `static/style.css`: Shared styling for all screens.
- `data/employees.json`: Employee ID and name directory.
- `data/attendance_log.csv`: Automatically generated attendance records.

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser.
# attendance_raspberry
