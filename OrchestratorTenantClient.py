from typing import List, Dict, Optional
import requests
import datetime

class OrchestratorTenantClient:
    """
    A client for interacting with the Orchestrator API to fetch data.
    This does not allow for manipulating any data in Orchestrator.
    """
    ### Private Functions Start ###
    def __init__(self, organisation: str, tenant: str, client_id: str, refresh_token: str):
        self.organisation = organisation
        self.tenant = tenant
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.base_url = f"https://cloud.uipath.com/{organisation}/{tenant}/orchestrator_/"
        self.access_token = self._authenticate()

        self.folders = self._get_folders()
        self.queue_defs = self._get_queue_defs()

    def _authenticate(self) -> Optional[str]:
        auth_url = "https://account.uipath.com/oauth/token"
        headers = {
            "Content-Type": "application/json",
            "X-UIPATH-TenantName": self.tenant
        }

        body = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token
        }

        response = requests.post(auth_url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        print(f"Failed to Authenticate: {response.text}")
        return None
        

    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _get_queue_defs(self) -> Optional[List[Dict]]:
        try:
            request_url = self.base_url + f"odata/QueueDefinitions"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()["value"]
            return data
        except Exception as e:
            print("An error occurred in _get_queue_defs():", str(e))
            return None
        

    def _get_folders(self) -> Optional[List[Dict]]:
        try:
            request_url = self.base_url + f"odata/Folders"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()["value"]
            return data
        except Exception as e:
            print("An error occurred in _get_folders():", str(e))
            return None
    ### Private Functions End ###


    ### Queue Functions Start ###
    def get_queue_details_table(
        self, 
        time_frame_minutes: int = 1440, 
        pageNo: int = 1, 
        pageSize: int = 1000, 
        orderBy: str = "queueName", 
        direction: str = "asc"
    ) -> Optional[List[Dict]]:
        """
        Fetch queue details from Orchestrator.

        :param time_frame_minutes: The timeframe in minutes to fetch the queue data (default is 1440 or 24 hours).
        :param pageNo: The page number for pagination (default is 1).
        :param pageSize: The number of items per page (default is 1000).
        :param orderBy: The field to order the data by (default is 'queueName').
        :param direction: The order direction, either 'asc' or 'desc' (default is 'asc').
        :return: A list of dictionaries with the queue details or None if an error occurs.
        """
        try:
            request_url = self.base_url + f"monitoring/QueuesMonitoring/GetQueuesTable?timeFrameMinutes={time_frame_minutes}&pageNo={pageNo}&pageSize={pageSize}&orderBy={orderBy}&direction={direction}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()["data"]
            return data
        except Exception as e:
            print("An error occurred in get_queue_details_table():", str(e))
            return None


    def get_queue_processing_records(self, days: int = 1) -> Optional[List[List[Dict]]]:
        try:
            datalist = []
            for queue in self.queue_defs:
                request_url = self.base_url + f"odata/QueueProcessingRecords/UiPathODataSvc.RetrieveLastDaysProcessingRecords(daysNo={1},queueDefinitionId={queue['Id']})"
                headers = self._get_headers()
                response = requests.get(request_url, headers=headers)
                records = response.json()["value"]

                # insert the name of the queue into the response for downstream filtering
                for record in records:
                    record["Name"] = queue["Name"]

                datalist.append(records)
            return datalist
        except Exception as e:
            print("An error occurred in get_queue_processing_records():", str(e))
            return None
        

    def get_unprocessed_items(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/QueuesMonitoring/GetUnprocessedItemsCounts?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_unprocessed_items():", str(e))
            return None


    def get_transactions_overview(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/QueuesMonitoring/GetProcessedItemsCounts?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_transactions_overview():", str(e))
            return None
        

    def get_transactions_timeline(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/QueuesMonitoring/GetProcessedItemsEvolution?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_transactions_timeline():", str(e))
            return None

    ### Queue Functions End ###    
    

    ### Job/Process Functions Start ###
    def get_completed_jobs_timeline(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/JobsMonitoring/GetFinishedJobsEvolution?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_completed_jobs_timeline():", str(e))
            return None
        

    def get_triggered_job_states(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/JobsMonitoring/GetJobsCounts?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_triggered_job_states():", str(e))
            return None
        

    def get_completed_jobs_overview(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/JobsMonitoring/GetFinishedJobsCounts?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_completed_jobs_overview():", str(e))
            return None
        

    def get_completed_jobs_timeframe(self, time_frame_minutes: int = 1440):
        try:
            request_url = self.base_url + f"monitoring/JobsMonitoring/GetRunningJobsEvolution?timeFrameMinutes={time_frame_minutes}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_completed_jobs_timeframe():", str(e))
            return None
        

    def get_job_stats(self):
        try:
            request_url = self.base_url + f"api/Stats/GetJobsStats"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            print("An error occurred in get_job_stats():", str(e))
            return None
        

    def get_process_details_table(
        self, 
        time_frame_minutes: int = 1440, 
        pageNo: int = 1, 
        pageSize: int = 1000, 
        orderBy: str = "processId", 
        direction: str = "asc"
    ) -> Optional[List[Dict]]:
        """
        Fetch process details from Orchestrator.

        :param time_frame_minutes: The timeframe in minutes to fetch the process data (default is 1440 or 24 hours).
        :param pageNo: The page number for pagination (default is 1).
        :param pageSize: The number of items per page (default is 1000).
        :param orderBy: The field to order the data by (default is 'processId').
        :param direction: The order direction, either 'asc' or 'desc' (default is 'asc').
        :return: A list of dictionaries with the process details or None if an error occurs.
        """
        try:
            request_url = self.base_url + f"monitoring/JobsMonitoring/GetProcessesTable?timeFrameMinutes={time_frame_minutes}&pageNo={pageNo}&pageSize={pageSize}&orderBy={orderBy}&direction={direction}"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()["data"]
            return data
        except Exception as e:
            print("An error occurred in get_process_details_table():", str(e))
            return None
    ### Job/Process Functions End ###

    def get_maintenance_mode_status(self):
        try:
            request_url = self.base_url + f"odata/Sessions/UiPath.Server.Configuration.OData.GetMachineSessionRuntimes?runtimeType=Unattended"
            headers = self._get_headers()
            response = requests.get(request_url, headers=headers)
            data = response.json()["value"]
            return data
        except Exception as e:
            print("An error occurred in get_maintenance_mode_status():", str(e))
            return None

    
    
    def get_faulted_jobs(self):
        try:
            current_time = datetime.datetime.now()
            creation_time = current_time - datetime.timedelta(days=6)
            
            # Format the time to the required UTC format (ISO 8601)
            creation_time_str = creation_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

            # Construct the URL
            query_params = f"?$top=100&$filter=((CreationTime ge {creation_time_str}) and (State eq '4') and (ProcessType eq 'Process'))"
            expand_params = "&$expand=Robot,Machine,Release&$orderby=StartTime desc"
            
            # Combine everything to form the final URL
            full_url = self.base_url +"odata/Jobs"+ query_params + expand_params
            
            
            headers = self._get_headers()

            faulted_jobs = []
            for folder in self.folders:
                try:
                    folder_id = folder["Id"]
                    folder_name = folder["DisplayName"]

                    headers["X-UIPATH-OrganizationUnitId"] = str(folder_id)
                    response = requests.get(full_url, headers=headers).json()
                    
                    for faulted_job in response["value"]:

                        job = {"Process_name":faulted_job["ReleaseName"],
                            "Organization" : faulted_job["OrganizationUnitFullyQualifiedName"],
                            "Folder" : folder_name,
                            "Machine" : faulted_job["HostMachineName"],
                            "Started":faulted_job["StartTime"],
                            "Ended":faulted_job["EndTime"],
                            "Reason":self.get_fault_reason(faulted_job["Key"],folder_id=folder_id)}
                        
                        faulted_jobs.append(job)

                except Exception as e:
                    print(e)
                    continue

            return faulted_jobs

        except Exception as e:
            print("An error occurred in get_faulted_jobs:", str(e))
            return None
        
        
    def get_fault_reason(self,key,folder_id):
        request_url = self.base_url + f"odata/Jobs/UiPath.Server.Configuration.OData.GetByKey(identifier={key})?$expand=Robot,Release,Machine"
        headers = self._get_headers()
        headers["X-UIPATH-OrganizationUnitId"] = str(folder_id)

        response = requests.get(request_url, headers=headers)
        reason = response.json()["Info"]
        return reason[:200]+"..."

    def get_disabled_triggers(self):
        # Base API URL for retrieving Process Schedules with filters
        query_params = "?$top=100&$filter=((Enabled eq false) and (QueueDefinitionId eq null))&$orderby=Name asc"
        full_url = self.base_url + "odata/ProcessSchedules" + query_params
        
        headers = self._get_headers()

        process_schedules = []
        for folder in self.folders:
            try:
                folder_id = folder["Id"]
                folder_name = folder["DisplayName"]

                # Include the folder in the request headers
                headers["X-UIPATH-OrganizationUnitId"] = str(folder_id)

                # Make the API request for each folder
                response = requests.get(full_url, headers=headers).json()

                # If no schedules found, skip to the next folder
                if int(response["@odata.count"]) == 0:
                    continue
                
                # Loop through the schedules and extract relevant data
                for schedule in response["value"]:
                    process_schedule = {
                        "Name": schedule["Name"],
                        "Enabled": schedule["Enabled"],
                        "NextStart": schedule.get("NextStart", "N/A"),
                        "Folder": folder_name
                    }
                    process_schedules.append(process_schedule)
            except:
                continue
        return process_schedules


    def get_queue_data(self):
        # Construct the URL for retrieving queue definitions
        query_params = "?$top=20&$orderby=QueueDefinitionName%20asc"
        full_url = self.base_url + "odata/QueueDefinitions/UiPath.Server.Configuration.OData.ListQueues" + query_params
        
        headers = self._get_headers()

        # Dictionary to track queue definitions by QueueDefinitionName
        queue_data_dict = {}

        for folder in self.folders:
            try:
                folder_id = folder["Id"]
                folder_name = folder["DisplayName"]

                # Add the folder ID to the headers
                headers["X-UIPATH-OrganizationUnitId"] = str(folder_id)
                
                # Make the GET request
                response = requests.get(full_url, headers=headers).json()
                
                
                # Check if there are any queues in the response
                if int(response["@odata.count"]) == 0:
                    continue

                # Iterate over the queue definitions in the "value" list
                for queue_definition in response["value"]:
                    queue_name = queue_definition["QueueDefinitionName"]
                    
                    # If the queue already exists, concatenate the folder names
                    if queue_name in queue_data_dict:
                        queue_data_dict[queue_name]["Folder"] += f"/{folder_name}"
                    else:
                        queue_data_dict[queue_name] = {
                            "QueueDefinitionName": queue_name,
                            "Organization": self.organisation,
                            "Folder": folder_name,
                            "SuccessfulTransactionsNo": queue_definition["SuccessfulTransactionsNo"],
                            "ApplicationExceptionsNo": queue_definition["ApplicationExceptionsNo"],
                            "BusinessExceptionsNo": queue_definition["BusinessExceptionsNo"]
                        }
            
            except Exception as e:
                print(f"Error processing folder {folder_name}: {e}")
                continue

        # Convert the dictionary values to a list before returning
        return list(queue_data_dict.values())
