import os
import io
import csv
import json
import time
import uuid
import base64
import socket
from datetime import datetime
import qrcode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EMPLOYEES_FILE = os.path.join(DATA_DIR, 'employees.json')
LOG_FILE = os.path.join(DATA_DIR, 'attendance_log.csv')

token_store = {"code": str(uuid.uuid4()), "expires": time.time() + 60}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def init_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Employee ID', 'Name', 'Action'])


def load_employees():
    if not os.path.exists(EMPLOYEES_FILE):
        return {}
    with open(EMPLOYEES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_valid_token(ttl_seconds=60):
    if time.time() > token_store["expires"]:
        token_store["code"] = str(uuid.uuid4())
        token_store["expires"] = time.time() + ttl_seconds
    return token_store["code"]


def is_token_valid(token):
    return bool(token) and token == token_store["code"] and time.time() <= token_store["expires"]


def generate_qr_base64(url):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def log_attendance(emp_id, name, action):
    init_storage()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([now, emp_id, name, action])
    return now


def read_attendance_logs():
    init_storage()
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))
