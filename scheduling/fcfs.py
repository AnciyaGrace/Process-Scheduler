def run_fcfs(processes):
    """
    First Come First Serve (FCFS) Scheduling Algorithm
    Input: list of dicts with keys: id, arrival_time, burst_time
    Output: dict with gantt, metrics, averages
    """
    # Sort by arrival time
    sorted_procs = sorted(processes, key=lambda x: (x['arrival_time'], x['id']))

    gantt = []
    metrics = []
    current_time = 0

    for p in sorted_procs:
        # If CPU is idle, jump to process arrival
        if current_time < p['arrival_time']:
            current_time = p['arrival_time']

        start = current_time
        end = current_time + p['burst_time']

        waiting_time = start - p['arrival_time']
        turnaround_time = end - p['arrival_time']

        gantt.append({
            "id": p['id'],
            "start": start,
            "end": end
        })

        metrics.append({
            "id": p['id'],
            "arrival_time": p['arrival_time'],
            "burst_time": p['burst_time'],
            "completion_time": end,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })

        current_time = end

    avg_waiting = round(sum(m['waiting_time'] for m in metrics) / len(metrics), 2)
    avg_turnaround = round(sum(m['turnaround_time'] for m in metrics) / len(metrics), 2)

    return {
        "algorithm": "FCFS",
        "gantt": gantt,
        "metrics": metrics,
        "averages": {
            "avg_waiting_time": avg_waiting,
            "avg_turnaround_time": avg_turnaround
        }
    }
