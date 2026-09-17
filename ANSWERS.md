# 1. When did the problem start? Include the timestamp and the evidence you used.
> Problem started at the following date and time: **2026-07-02 14:32:40.073**.
> By parsing both the logs, this is the exact timestamp of the first status=202 request in web.log that failed to find a job completed match in worker.log with the same request_id.

# 2. Which endpoint is affected? Support your answer with evidence from the logs.
> The `/checkout` endpoint is specifically affected. Every dropped request_id isolated by the script originated from a POST method request to the `/checkout` route.

# 3. What do the failing requests have in common? Identify the pattern and support it with numbers.
> Every failing request is a POST request mapped to the path=`/checkout` endpoint. Other jobs such as `/login` or `/orders` are successfully completing in the worker logs.
> The terminal output shows that the 100% of the **2385** missing requests identified share the exact same POST method and path of `/checkout`.

# 4. How many distinct users were affected?
> **2335** distinct users were affected as per the terminal output.

# Bonus: Is there anything in the logs that suggests the root cause?
> The background worker is actually running perfectly fine for other tasks. The problem is specifically happening inside the code that handles the `/checkout` route. While there are `AnalyticsUploadTimeout` errors in the worker log, they do not have request_ids and dont match up with failed orders. Since the checkout jobs disappears from the logs without an error message, the checkout function is probably crashing silently or failing before it can print a status.

# Investigation Process:
1. > Reviewed the log structure to understand the relationship between web.log and worker.log, realised the common key request_id.
2. > Noticed the core behavior, successful asynchronous tasks log a status=202 in web.log and a job completed event with a matching request_id in worker.log.
3. > Approached the issue as a set difference problem to isolate the missing data. Every single log minus the successful logs leaves us with failed logs.
4. > Wrote a Python script using hash map and sets to parse both files, storing all 202 requests from the web log, and filtering out any request_id that appeared as completed in the worker log.
5. > Analysed the resulting pattern of requests and observed they all belonged to the `/checkout` path.
6. > Investigated the AnalyticsUploadTimeout errors in the worker log but realised they were unrelated to our problem because the error log does not carries any `request_id` with it meaning this error is not attached to any specific user or any specific order.