# CloudSQL Latency Tester

This Python script measures the connection latency between your application and multiple CloudSQL instances using the nc (netcat) command for simple TCP connectivity checks.


## Requirements
* Python 3.x
* nc (netcat) installed on your system (used to test TCP connection)
* Python packages listed in requirements.txt

## Installation

1. Clone the repository or download the files.
2. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file in the project root and add your environment variables:
    ```bash
    CLOUDSQL_1_DBNAME="database_name_1"
    CLOUDSQL_1_HOST="instance_1_ip"
    CLOUDSQL_1_PROJECT="project_id_1"

    CLOUDSQL_2_DBNAME="database_name_2"
    CLOUDSQL_2_HOST="instance_2_ip"
    CLOUDSQL_2_PROJECT="project_id_2"

    ```

Add additional entries as needed for other instances.

## Usage
1. Ensure that nc (netcat) is installed on your system.
2. Run the script to measure latency across the configured CloudSQL instances:
    ```
    python3 cloudsql-check-latency.py
    ```
3. The script will:
    * Load connection settings from the .env file.
    * Perform 50 connection attempts to each CloudSQL instance.
    * Measure the average connection latency in milliseconds.
    * Output a summary of the results to the terminal in JSON format.


## How It Works

* The script retrieves environment variables for multiple CloudSQL instances from a .env file.
* For each CloudSQL instance, it runs a series of TCP connection attempts using the nc command to measure the time it takes to establish a connection.
* It calculates the average connection latency over 50 attempts per instance.
* A final report is printed as a JSON structure, showing the status and average latency for each database.

## Output
The script provides a summary in JSON format that includes:
* Total number of database connections tested.
* Number of successful and failed connection attempts.
* Average latency (in milliseconds) per CloudSQL instance.

## Notes
* The default number of connection attempts is set to 50 but can be adjusted in the script by changing the NUM_ATTEMPTS variable.
* Ensure that your CloudSQL instances allow incoming connections from the machine where the script is being run.