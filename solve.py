# solve.py
def analyze_logs():
    # store web log in map: request_id -> log line
    promised_jobs = {}
    with open("web.log", "r") as web_file:
        for line in web_file:
            if "status=202" in line:
                req_id = line.strip().split("request_id=")[-1]
                promised_jobs[req_id] = line.strip()

    # jobs finished
    completed_jobs = set()
    with open("worker.log", "r") as worker_file:
        for line in worker_file:
            if "job completed" in line:
                req_id = line.strip().split("request_id=")[-1].split(" ")[0]
                completed_jobs.add(req_id)

    # failed requests : map - finished
    failed_requests = []
    for req_id, log_line in promised_jobs.items():
        if req_id not in completed_jobs:
            failed_requests.append(log_line)

    print(f"Total failed/missing orders found: {len(failed_requests)}\n")
    print("--- Failed Log Lines ---")
    for failure in failed_requests:
        print(failure)

    if not failed_requests:
        print("No failed requests found.")
        return

    first_failure = failed_requests[0]
    print(f"Start Time: {first_failure.split(' ')[0]} {first_failure.split(' ')[1]}")
    users = set([line.split("user_id=")[1].split(" ")[0] for line in failed_requests])
    print(f"Distinct Users: {len(users)}")

    print(f"Failed Requests: {len(failed_requests)}")


if __name__ == "__main__":
    analyze_logs()
