from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduling.fcfs import run_fcfs
from scheduling.sjf import run_sjf
from deadlock.bankers import run_bankers
from recommender import recommend_algorithm

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API


# ─────────────────────────────────────────────
# Helper: Validate process input
# ─────────────────────────────────────────────
def validate_processes(processes):
    if not processes or not isinstance(processes, list):
        return False, "No processes provided."
    for p in processes:
        if 'id' not in p or 'arrival_time' not in p or 'burst_time' not in p:
            return False, f"Process missing required fields (id, arrival_time, burst_time): {p}"
        if p['burst_time'] <= 0:
            return False, f"Burst time must be greater than 0 for process {p['id']}."
        if p['arrival_time'] < 0:
            return False, f"Arrival time cannot be negative for process {p['id']}."
    return True, ""


# ─────────────────────────────────────────────
# Route: Home / Health Check
# ─────────────────────────────────────────────
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "message": "Process Scheduling & Resource Allocation Manager API",
        "endpoints": [
            "POST /api/fcfs",
            "POST /api/sjf",
            "POST /api/compare",
            "POST /api/bankers",
            "POST /api/recommend"
        ]
    })


# ─────────────────────────────────────────────
# Route: FCFS Scheduling
# ─────────────────────────────────────────────
@app.route('/api/fcfs', methods=['POST'])
def fcfs():
    data = request.get_json()
    processes = data.get('processes', [])

    valid, error = validate_processes(processes)
    if not valid:
        return jsonify({"error": error}), 400

    try:
        result = run_fcfs(processes)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# Route: SJF Scheduling
# ─────────────────────────────────────────────
@app.route('/api/sjf', methods=['POST'])
def sjf():
    data = request.get_json()
    processes = data.get('processes', [])

    valid, error = validate_processes(processes)
    if not valid:
        return jsonify({"error": error}), 400

    try:
        result = run_sjf(processes)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# Route: Compare FCFS vs SJF side by side
# ─────────────────────────────────────────────
@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    processes = data.get('processes', [])

    valid, error = validate_processes(processes)
    if not valid:
        return jsonify({"error": error}), 400

    try:
        fcfs_result = run_fcfs(processes)
        sjf_result  = run_sjf(processes)

        return jsonify({
            "fcfs": fcfs_result,
            "sjf": sjf_result,
            "comparison": {
                "better_waiting_time": (
                    "FCFS" if fcfs_result['averages']['avg_waiting_time'] <= sjf_result['averages']['avg_waiting_time']
                    else "SJF"
                ),
                "better_turnaround_time": (
                    "FCFS" if fcfs_result['averages']['avg_turnaround_time'] <= sjf_result['averages']['avg_turnaround_time']
                    else "SJF"
                )
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# Route: Banker's Algorithm (Deadlock Detection)
# ─────────────────────────────────────────────
@app.route('/api/bankers', methods=['POST'])
def bankers():
    data = request.get_json()

    required_keys = ['processes', 'allocation', 'maximum', 'available']
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required field: {key}"}), 400

    try:
        result = run_bankers(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# Route: Algorithm Recommendation
# ─────────────────────────────────────────────
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    processes = data.get('processes', [])

    valid, error = validate_processes(processes)
    if not valid:
        return jsonify({"error": error}), 400

    try:
        result = recommend_algorithm(processes)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# Run Server
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
