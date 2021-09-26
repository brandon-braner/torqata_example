# Torqata Coding Example

## Rerequirements
* Create API/API documentation.
  * Rows of data with search, filter, sorting, and pagination
  * Aggregated summary data
  * Modify data in the database
* use flask/fastapi python for any back-end code if necessary
* push data into a database of your choice
* Check in the code to your personal GitHub account.
* Deploy the application in Google Cloud (Use free tier with new account setup)
** Preferably you can use managed services (App Engine, Cloud Run, CloudSQL,
etc.)
  
**EXTRA POINTS**
* Unit Testing implemented
* Continuous Integration/Continuous Deployment features set up (CI/CD)
* E.g. CircleCI, Travis, GCP Cloud Build, Github Actions, etc.
* Authentication implemented so that only authenticated users are capable of accessing
the API.
  

## Solution

* Implement api using FastAPI
* Authentication handled via FastAPI builtin methods
  * Authentication provider will be our own postgres database
  * middleware used to check authentication header or cookie for on requests
  * use starlette authentication middleware which will store the authorized user in the request context  
  * Authentication documentation in Notion [https://timberln.notion.site/Authentication-932f3b71f1f1447d8b67e4ecd2aedbe1](here)
    * This is the documentation of how it works in my side project referencing using aws cognito but everything else is the same
