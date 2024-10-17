Queue Success Rate alert query
This shows how to chain queries, each resulting row in the table is going to be evaluated against the threshold set.
We also provide a field in the resuling table with a meaningful label for the db we are querying which can be referenced in alert payloads

An example of how to reference the db_name label: "Grafana alert for {{ index $labels "db_name" }}"

(SELECT 
    'Aspenhealthcare' AS db_name,
    (countSuccessful * 1.0 / (countSuccessful + countBusinessExceptions + countApplicationExceptions) * 100) AS success_rate_percentage
FROM 
    aspenhealthcare_DB.transactions_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Italtile' AS db_name,
    (countSuccessful * 1.0 / (countSuccessful + countBusinessExceptions + countApplicationExceptions) * 100) AS success_rate_percentage
FROM 
    italtile_DB.transactions_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Afgri Prod' AS db_name,
    (countSuccessful * 1.0 / (countSuccessful + countBusinessExceptions + countApplicationExceptions) * 100) AS success_rate_percentage
FROM 
    afgriprod_DB.transactions_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Intellicomms' AS db_name,
    (countSuccessful * 1.0 / (countSuccessful + countBusinessExceptions + countApplicationExceptions) * 100) AS success_rate_percentage
FROM 
    plpljaakhz_DB.transactions_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Tangent Production' AS db_name,
    (countSuccessful * 1.0 / (countSuccessful + countBusinessExceptions + countApplicationExceptions) * 100) AS success_rate_percentage
FROM 
    tangentsolutionsproduction_DB.transactions_overview
ORDER BY date_queried DESC
LIMIT 1 );

######################################################################################################################


Job alert queries

(SELECT 
    'Italtile' AS db_name,
    ((countSuccessful * 1.0) / (countSuccessful + countStopped + countErrors) * 100) AS success_rate_percentage
FROM 
    italtile_DB.completed_jobs_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT  
    'Aspenhealthcare' AS db_name,
    ((countSuccessful * 1.0) / (countSuccessful + countStopped + countErrors) * 100) AS success_rate_percentage
FROM 
    aspenhealthcare_DB.completed_jobs_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Afgri Prod' AS db_name,
    ((countSuccessful * 1.0) / (countSuccessful + countStopped + countErrors) * 100) AS success_rate_percentage
FROM 
    afgriprod_DB.completed_jobs_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Intellicomms' AS db_name,
    ((countSuccessful * 1.0) / (countSuccessful + countStopped + countErrors) * 100) AS success_rate_percentage
FROM 
    plpljaakhz_DB.completed_jobs_overview
ORDER BY date_queried DESC
LIMIT 1 )

UNION

(SELECT 
    'Tangent Production' AS db_name,
    ((countSuccessful * 1.0) / (countSuccessful + countStopped + countErrors) * 100) AS success_rate_percentage
FROM 
    tangentsolutionsproduction_DB.completed_jobs_overview
ORDER BY date_queried DESC
LIMIT 1 );
