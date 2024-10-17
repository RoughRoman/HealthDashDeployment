import pandas as pd
from OrchestratorTenantClient import OrchestratorTenantClient
from utils import write_df_to_mysql, now
import pymysql

class OrchestratorDataInserter:
    def __init__(self, client: OrchestratorTenantClient, db_user: str, db_pass: str, db_host: str, db_name: str):
        self.client = client
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_name = db_name
        self.create_mysql_schema()

    def create_mysql_schema(self):
        # Create a connection to MySQL server
        connection = pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_pass
        )

        try:
            with connection.cursor() as cursor:
                # Check if the schema already exists
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}`;")
                print(f"Schema '{self.db_name}' has been created or already exists.")
        except pymysql.MySQLError as e:
            print(f"Error creating schema: {e}")
        finally:
            connection.close()

    def insert_queue_processing_records(self):
        try:
            records = self.client.get_queue_processing_records(days=1)
            record_dfs = [pd.json_normalize(record) for record in records]
            
            for record_df in record_dfs:
                record_df.drop(columns=["ReportType", "QueueDefinitionId", "TenantId", "Id"], inplace=True)
                write_df_to_mysql(record_df, "queue_processing_records", self.db_user, self.db_pass, self.db_host, self.db_name)
        except Exception as e:
            print(f"An error occurred in insert_queue_processing_records() : {str(e)}")

    def insert_queue_details_table(self):
        try:
            records = self.client.get_queue_details_table()
            date_queried = now()
            record_dfs_list = [pd.json_normalize(record).fillna("N/A") for record in records]
            for record in records:
                record["date_queried"] = date_queried
                
            record_dfs = pd.concat(record_dfs_list, axis=0)
            write_df_to_mysql(record_dfs, "queue_details_table", self.db_user, self.db_pass, self.db_host, self.db_name, trunc=True)
        except Exception as e:
            print(f"An error occurred in insert_queue_details_table() : {str(e)}")

    def insert_unprocessed_items(self):
        try:
            record = self.client.get_unprocessed_items()
            record["date_queried"] = now()
            record_df = pd.json_normalize(record)
            write_df_to_mysql(record_df, "unprocessed_items", self.db_user, self.db_pass, self.db_host, self.db_name, trunc=True)
        except Exception as e:
            print(f"An error occurred in insert_unprocessed_items() : {str(e)}")

    def insert_transactions_timeline(self):
        try:
            records = self.client.get_transactions_timeline()
            for record in records:
                write_df_to_mysql(pd.json_normalize(record), "transactions_timeline", self.db_user, self.db_pass, self.db_host, self.db_name)
        except Exception as e:
            print(f"An error occurred in insert_transactions_timeline() : {str(e)}")

    def insert_transactions_overview(self):
        try:
            record = self.client.get_transactions_overview()
            record["date_queried"] = now()

            new_record_df = pd.json_normalize(record)

            try:
                old_record_df = pd.read_csv("transactions_overview_old.csv")

                columns_to_sum = ["countSuccessful", "countBusinessExceptions", "countApplicationExceptions"]

                old_total = old_record_df[columns_to_sum].sum(axis=1).values[0]
                new_total = new_record_df[columns_to_sum].sum(axis=1).values[0]

                if old_total == new_total:
                    return
                record_df = pd.concat([new_record_df, old_record_df])
            except:
                record_df = new_record_df
                
            write_df_to_mysql(record_df, "transactions_overview", self.db_user, self.db_pass, self.db_host, self.db_name,trunc=True)
            
            new_record_df.to_csv("transactions_overview_old.csv",index=False, mode="w")

        except Exception as e:
            print(f"An error occurred in insert_transactions_overview() : {str(e)}")



    def insert_completed_jobs_overview(self):
        try:
            record = self.client.get_completed_jobs_overview()
            record["date_queried"] = now()
            new_record_df = pd.json_normalize(record)

            try:
                old_record_df = pd.read_csv("jobs_overview_old.csv")

                columns_to_sum = ["countSuccessful", "countErrors", "countStopped"]

                old_total = old_record_df[columns_to_sum].sum(axis=1).values[0]
                new_total = new_record_df[columns_to_sum].sum(axis=1).values[0]

                if old_total == new_total:
                    return
                record_df = pd.concat([new_record_df, old_record_df])
            except:
                record_df = new_record_df
                
            write_df_to_mysql(record_df, "completed_jobs_overview", self.db_user, self.db_pass, self.db_host, self.db_name,trunc=True)
            
            new_record_df.to_csv("jobs_overview_old.csv",index=False, mode="w")

        except Exception as e:
            print(f"An error occurred in insert_completed_jobs_overview() : {str(e)}")


    def insert_completed_jobs_timeline(self):
        try:
            records = self.client.get_completed_jobs_timeline()
            for record in records:
                write_df_to_mysql(pd.json_normalize(record), "completed_jobs_timeline", self.db_user, self.db_pass, self.db_host, self.db_name)
        except Exception as e:
            print(f"An error occurred in insert_completed_jobs_timeline() : {str(e)}")

    def insert_completed_jobs_timeframe(self):
        try:
            records = self.client.get_completed_jobs_timeframe()
            for record in records:
                write_df_to_mysql(pd.json_normalize(record), "completed_jobs_timeframe", self.db_user, self.db_pass, self.db_host, self.db_name)
        except Exception as e:
            print(f"An error occurred in insert_completed_jobs_timeframe() : {str(e)}")

    def insert_process_details_table(self):
        try:
            records = self.client.get_process_details_table(time_frame_minutes=10080)
            date_queried = now()
            record_dfs_list = [pd.json_normalize(record).fillna("N/A") for record in records]
            for record in records:
                record["date_queried"] = date_queried
                
            record_dfs = pd.concat(record_dfs_list, axis=0)
            write_df_to_mysql(record_dfs, "process_details_table", self.db_user, self.db_pass, self.db_host, self.db_name, trunc=True)
        except Exception as e:
            print(f"An error occurred in insert_process_details_table() : {str(e)}")

    def insert_job_stats(self):
        try:
            records = self.client.get_job_stats()
            new_record = {record["title"]: record["count"] for record in records}
            new_record["date_queried"] = now()
            record_df = pd.json_normalize(new_record)
            write_df_to_mysql(record_df, "job_stats", self.db_user, self.db_pass, self.db_host, self.db_name, trunc=True)
        except Exception as e:
            print(f"An error occurred in insert_job_stats() : {str(e)}")

    
    def insert_triggered_job_states (self):
        try:
            record = self.client.get_triggered_job_states()
            record["date_queried"] = now()
            record_df = pd.json_normalize(record)
            write_df_to_mysql(record_df,
                            "triggered_job_states",
                            self.db_user,
                            self.db_pass,
                            self.db_host,
                            self.db_name,
                            trunc=True)

        except Exception as e:
            print(f"An error occured in insert_triggered_job_states() : {str(e)}")


    def insert_queue_data(self):
        try:

            queue_data = self.client.get_queue_data()
                
            record_dfs = pd.json_normalize(queue_data)



            # Write the DataFrame to the MySQL database
            write_df_to_mysql(record_dfs,
                "queue_data",  # Table name where queue data will be inserted
                self.db_user,
                self.db_pass,
                self.db_host,
                self.db_name,
                trunc=True)  # Set to True if you want to truncate the table before inserting

        except Exception as e:
            print(f"An error occurred in insert_queue_data(): {str(e)}")

    def insert_maintenance_mode_status(self):
        try:
            # Get maintenance mode status from the client

            current_machine_df = pd.json_normalize(self.client.get_maintenance_mode_status())

            write_df_to_mysql(current_machine_df,
                "maintenance_mode_states",
                self.db_user,
                self.db_pass,
                self.db_host,
                self.db_name,
                trunc=True)
            
        except Exception as e:
            print(f"An error occured in insert_maintenance_mode_status() : {str(e)}")


    def insert_disabled_triggers(self):
        try:

            # Retrieve schedules from the client and normalize them into a DataFrame
            record_dfs = pd.json_normalize(self.client.get_disabled_triggers())

            # Write the DataFrame to the database table
            write_df_to_mysql(record_dfs,
                            "disabled_triggers",  # Replace with your table name
                            self.db_user,
                            self.db_pass,
                            self.db_host,
                            self.db_name,
                            trunc=True)  # Optional: set trunc=True if you want to truncate the table before insert
            
        except Exception as e:
            print(f"An error occurred in insert_disabled_triggers(): {str(e)}")


    def insert_faulted_jobs (self):
        
        try:
            record_df = pd.json_normalize(self.client.get_faulted_jobs())

            write_df_to_mysql(record_df,
                    "faulted_jobs",
                    self.db_user,
                    self.db_pass,
                    self.db_host,
                    self.db_name,
                    trunc=False)
            
        except Exception as e:
            print(f"An error occured in insert_faulted_jobs() : {str(e)}")