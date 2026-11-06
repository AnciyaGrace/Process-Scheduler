def run_bankers(data):
    """
    Banker's Algorithm for Deadlock Detection
    Input:
      - processes: list of process IDs e.g. ["P0", "P1", "P2"]
      - allocation: 2D list — allocated resources per process
      - maximum: 2D list — max resources each process may need
      - available: list — currently available resources
    Output:
      - safe: bool
      - safe_sequence: list (if safe)
      - need_matrix: 2D list
      - message: explanation string
    """
    processes  = data['processes']
    allocation = data['allocation']
    maximum    = data['maximum']
    available  = data['available']

    n = len(processes)       # number of processes
    m = len(available)       # number of resource types

    # Calculate Need matrix: Need = Maximum - Allocation
    need = [
        [maximum[i][j] - allocation[i][j] for j in range(m)]
        for i in range(n)
    ]

    work      = available[:]
    finish    = [False] * n
    safe_seq  = []

    # Safety Algorithm
    while len(safe_seq) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                # Process i can finish — release its resources
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                safe_seq.append(processes[i])
                found = True

        if not found:
            break  # No progress → deadlock

    if all(finish):
        return {
            "safe": True,
            "safe_sequence": safe_seq,
            "need_matrix": need,
            "message": f"System is in a SAFE state. Safe sequence: {' → '.join(safe_seq)}"
        }
    else:
        # Find which processes are deadlocked
        deadlocked = [processes[i] for i in range(n) if not finish[i]]
        return {
            "safe": False,
            "safe_sequence": [],
            "need_matrix": need,
            "deadlocked_processes": deadlocked,
            "message": f"System is in an UNSAFE state. Deadlock risk detected in: {', '.join(deadlocked)}"
        }
