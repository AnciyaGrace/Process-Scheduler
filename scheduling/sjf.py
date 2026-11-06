def run_sjf(processes):
    """
    Shortest Job First (SJF) Non-Preemptive Scheduling Algorithm
    Input: list of dicts with keys: id, arrival_time, burst_time
    Output: dict with gantt, metrics, averages
    """
    remaining = [p.copy() for p in processes]
    gantt = []
    metrics = []
    current_time = 0
    completed = []

    while remaining:
        # Get all processes that have arrived by current_time
        available = [p for p in remaining if p['arrival_time'] <= current_time]

        if not available:
            # CPU idle — jump to next process arrival
            current_time = min(p['arrival_time'] for p in remaining)
            continue

        # Pick shortest burst time (tie-break: earliest arrival)
        selected = min(available, key=lambda x: (x['burst_time'], x['arrival_time']))
        remaining.remove(selected)

        start = current_time
        end = current_time + selected['burst_time']

        waiting_time = start - selected['arrival_time']
        turnaround_time = end - selected['arrival_time']

        gantt.append({
            "id": selected['id'],
            "start": start,
            "end": end
        })

        metrics.append({
            "id": selected['id'],
            "arrival_time": selected['arrival_time'],
            "burst_time": selected['burst_time'],
            "completion_time": end,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })

        current_time = end

    avg_waiting = round(sum(m['waiting_time'] for m in metrics) / len(metrics), 2)
    avg_turnaround = round(sum(m['turnaround_time'] for m in metrics) / len(metrics), 2)

    return {
        "algorithm": "SJF",
        "gantt": gantt,
        "metrics": metrics,
        "averages": {
            "avg_waiting_time": avg_waiting,
            "avg_turnaround_time": avg_turnaround
        }
    }
