from flask import Flask, render_template, request
from utils import (
    get_local_ip,
    init_storage,
    load_employees,
    get_valid_token,
    is_token_valid,
    generate_qr_base64,
    log_attendance,
    read_attendance_logs,
)

app = Flask(__name__)
LOCAL_IP = get_local_ip()
PORT = 5050

init_storage()


@app.route('/')
def kiosk():
    token = get_valid_token(ttl_seconds=60)
    checkin_url = f"http://{LOCAL_IP}:{PORT}/checkin?token={token}"
    qr_b64 = generate_qr_base64(checkin_url)
    return render_template('kiosk.html', qr_b64=qr_b64, checkin_url=checkin_url)


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    token = request.args.get('token')
    if not is_token_valid(token):
        return render_template(
            'checkin.html',
            expired=True,
            error=None,
            success=None
        )

    if request.method == 'POST':
        emp_id = request.form.get('emp_id', '').strip().upper()
        action = request.form.get('action', '').strip().upper()
        employees = load_employees()

        if emp_id not in employees:
            return render_template(
                'checkin.html',
                expired=False,
                error=f"Invalid Employee ID: {emp_id}",
                success=None
            )

        if action not in ('IN', 'OUT'):
            return render_template(
                'checkin.html',
                expired=False,
                error="Invalid action selected.",
                success=None
            )

        name = employees[emp_id]
        timestamp = log_attendance(emp_id, name, action)
        return render_template(
            'checkin.html',
            expired=False,
            error=None,
            success={"name": name, "emp_id": emp_id, "action": action, "timestamp": timestamp}
        )

    return render_template('checkin.html', expired=False, error=None, success=None)


@app.route('/admin')
def admin():
    rows = read_attendance_logs()
    headers = rows[0] if rows else []
    records = list(reversed(rows[1:])) if len(rows) > 1 else []
    return render_template('admin.html', headers=headers, records=records)


if __name__ == '__main__':
    print("\n--- QR Attendance System Running ---")
    print(f"Kiosk Screen : http://localhost:{PORT}")
    print(f"Network URL  : http://{LOCAL_IP}:{PORT}")
    print(f"Admin Logs   : http://localhost:{PORT}/admin\n")
    app.run(host='0.0.0.0', port=PORT, debug=True)
