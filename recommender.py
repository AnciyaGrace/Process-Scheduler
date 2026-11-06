def recommend_algorithm(processes):
    """
    Recommends the best scheduling algorithm based on process characteristics.
    Logic:
      - If all processes arrive at time 0 and burst times are similar → FCFS (simple, fair)
      - If burst times vary significantly → SJF (minimizes waiting time)
      - If many processes with varied arrival times → SJF
    """
    burst_times   = [p['burst_time'] for p in processes]
    arrival_times = [p['arrival_time'] for p in processes]

    avg_burst  = sum(burst_times) / len(burst_times)
    max_burst  = max(burst_times)
    min_burst  = min(burst_times)
    variance   = max_burst - min_burst

    all_arrive_at_zero = all(a == 0 for a in arrival_times)

    if all_arrive_at_zero and variance <= 2:
        recommendation = "FCFS"
        reason = (
            "All processes arrive at the same time and burst times are similar. "
            "FCFS is simple and fair in this scenario."
        )
    elif variance >= 4:
        recommendation = "SJF"
        reason = (
            f"Burst times vary significantly (min={min_burst}, max={max_burst}). "
            "SJF minimizes average waiting time by executing shorter jobs first."
        )
    elif not all_arrive_at_zero:
        recommendation = "SJF"
        reason = (
            "Processes have varied arrival times. "
            "SJF handles this efficiently by always picking the shortest available job."
        )
    else:
        recommendation = "FCFS"
        reason = "Workload is balanced. FCFS provides a simple and predictable execution order."

    return {
        "recommended_algorithm": recommendation,
        "reason": reason,
        "analysis": {
            "total_processes": len(processes),
            "avg_burst_time": round(avg_burst, 2),
            "min_burst_time": min_burst,
            "max_burst_time": max_burst,
            "burst_variance": variance,
            "all_arrive_at_zero": all_arrive_at_zero
        }
    }
