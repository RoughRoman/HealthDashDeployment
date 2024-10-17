from OrchestratorTenantClient import OrchestratorTenantClient
from OrchestratorDataInserter import OrchestratorDataInserter
import os
import time
import schedule


def timeseriesdata(host, user, password):

    client = OrchestratorTenantClient(
        organisation=os.getenv('ORGANISATION'),
        tenant=os.getenv('TENANT'),
        client_id=os.getenv('CLIENT_ID'),
        refresh_token=os.getenv('REFRESH_TOKEN')
    )

    # Determine database name
    db_name = os.getenv("SCHEMA_NAME", client.organisation)

    # Initialize OrchestratorDataInserter
    inserter = OrchestratorDataInserter(client=client, db_user=user, db_pass=password, db_host=host, db_name=db_name)

    # Insert records
    try:
        inserter.insert_queue_processing_records()
        inserter.insert_transactions_timeline()
        inserter.insert_completed_jobs_timeline()
        inserter.insert_completed_jobs_timeframe()
        
    except Exception as e:
        print(f"Error in majordata: {e}")

def realtimestats(host, user, password):

    client = OrchestratorTenantClient(
        organisation=os.getenv('ORGANISATION'),
        tenant=os.getenv('TENANT'),
        client_id=os.getenv('CLIENT_ID'),
        refresh_token=os.getenv('REFRESH_TOKEN')
    )


    # Determine database name
    db_name = os.getenv("SCHEMA_NAME", client.organisation)

    # Initialize OrchestratorDataInserter
    inserter = OrchestratorDataInserter(client=client, db_user=user, db_pass=password, db_host=host, db_name=db_name)

    # Insert records
    try:
        inserter.insert_transactions_overview()
        inserter.insert_completed_jobs_overview()
        inserter.insert_unprocessed_items()
        inserter.insert_triggered_job_states()
        inserter.insert_process_details_table()
        inserter.insert_queue_details_table()
        inserter.insert_queue_data()
        inserter.insert_maintenance_mode_status()
        inserter.insert_disabled_triggers()
        inserter.insert_job_stats()
        inserter.insert_faulted_jobs()
               
    except Exception as e:
        print(f"Error in realtimestats: {e}")



def main():
    # Read database connection details from environment variables
    host = os.getenv('DB_HOST', '')  # Default to localhost if not set
    user = os.getenv('DB_USER', '')       # Default to 'root' if not set
    password = os.getenv('DB_PASSWORD','')   # No default password

    # Read intervals from environment variables or use defaults
    timeseries_interval = int(os.getenv('TIMESERIES_INTERVAL', 21600))   # Default is 6 hours
    realtimestats_interval = int(os.getenv('REALTIME_INTERVAL', 600))   # Default is 1 hour

    # Schedule the timeseries data function
    schedule.every(timeseries_interval).seconds.do(timeseriesdata, host, user, password)

    # Schedule the real-time stats function
    schedule.every(realtimestats_interval).seconds.do(realtimestats, host, user, password)

    # Keep the scheduling running
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting

if __name__ == "__main__":
    main()
