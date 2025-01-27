import os
import subprocess
import json
import time
from dotenv import load_dotenv
from datetime import datetime

# Number of connection attempts to make per server
NUM_ATTEMPTS = 50

# Load environment variables
def load_env():
    load_dotenv()
    return [
        {
            "name": os.getenv(f"CLOUDSQL_{i}_DBNAME"),
            "host": os.getenv(f"CLOUDSQL_{i}_HOST"),  # Direct host IP of Cloud SQL
            "port": "5432",  # PostgreSQL default port
            "project": os.getenv(f"CLOUDSQL_{i}_PROJECT")  # Google Cloud Project
        }
        for i in range(1, 100) if os.getenv(f"CLOUDSQL_{i}_HOST")
    ]

# Run the nc command multiple times to test TCP connection and measure latency
def run_nc_test(server):
    latencies = []
    
    for attempt in range(NUM_ATTEMPTS):
        start_time = datetime.now().isoformat()
        try:
            # Measure the start time in seconds (as a float)
            start = time.time()

            # Run nc command and measure the time with subprocess
            result = subprocess.run(
                ['nc', '-zv', server['host'], server['port']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Measure the end time and calculate total connection time in milliseconds
            end = time.time()
            total_time_ms = (end - start) * 1000  # Convert to milliseconds
            latencies.append(total_time_ms)

        except Exception as e:
            latencies.append(None)

    # Filter out None values in case of failures and calculate average latency
    valid_latencies = [latency for latency in latencies if latency is not None]
    if valid_latencies:
        avg_latency_ms = sum(valid_latencies) / len(valid_latencies)
    else:
        avg_latency_ms = None

    return {
        "status": "success" if valid_latencies else "error",
        "project": server['project'],
        "host": server['host'],
        "database": server['name'],
        "latencies": valid_latencies,
        "average_latency_ms": avg_latency_ms,  # Average latency
        "attempts": NUM_ATTEMPTS,
        "start_time": start_time,
        "end_time": datetime.now().isoformat()
    }

# Test all Cloud SQL connections
def test_cloudsql_connections(servers):
    results = []
    for server in servers:
        # Run the nc command for each server
        results.append(run_nc_test(server))
    return results

# Output results in a Datadog-friendly format or general JSON structure
def output_results(results):
    summary = {"total_tests": len(results), "successful_tests": 0, "failed_tests": 0, "databases": []}
    for result in results:
        summary["databases"].append({
            "database": result["database"],
            "project": result["project"],
            "status": result["status"],
            "host": result["host"],
            "average_latency_ms": result.get("average_latency_ms", "N/A"),
            "attempts": result["attempts"]
        })
        if result["status"] == "success":
            summary["successful_tests"] += 1
        else:
            summary["failed_tests"] += 1

    # Create a JSON report with summary only (no detailed results)
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary
    }
    
    # Print and return the full report
    json_output = json.dumps(report, indent=4)
    print(json_output)
    return json_output

# Load environment and run tests
def main():
    servers = load_env()
    if not servers:
        print("No servers loaded. Please check your environment variables.")
    else:
        results = test_cloudsql_connections(servers)
        output_results(results)

# Run the program
if __name__ == "__main__":
    main()