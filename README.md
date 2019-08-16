How to run:
1. Clone the repo
2. Make sure you have docker and docker-compose
3. Navigate to project directory (where the docker-compose file is present)
4. Add the `.env` file sent through the mail in the root of the project directory.
```bash
docker-compose up
```
That's it.



Tech Stack:
 - Django
 - Django Rest Framework
 - Postgres
 - Amazon S3 (uploaded files are stored here)
 - Redis (Used as message broker for celery)
 - Celery
 - Flower: Celery monitoring tool (localhost:5555)


#### Endpoints

1. Create a user.
```bash
curl "localhost:8000/auth/users/" --data "username=bhavesh&email=bhaveshpraveen10@gmail.com&password=12ab34cd"
```
Enter user_name, email and password of your choice. Email is optional. 
  
2. Create Token
```bash
curl "localhost:8000/token/" --data "username=bhavesh&&password=12ab34cd"
# sample response
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU2NjA0OTQ5MiwianRpIjoiYmJhMDIzZTEyZWY5NGNkODhhNDYyYjVmM2U4ODQ2ZjciLCJ1c2VyX2lkIjoxfQ.dlE5dqGSOrgp4UntI7GEgOkKa4-Z1VEwk482mx0Oq1A",
"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY1OTY0ODkyLCJqdGkiOiIwZjU3MmFkM2EyNDU0MThhOGQyMTdmZDQ1NDQyMGJhZiIsInVzZXJfaWQiOjF9.Be4rxvTm6NfzrQ02LkCXZORskx1xw4HqBMa6taFaC-M"}
```

If the token expires, just hit this endpoint again to get new access and refresh token.
(You can also use the refresh token to get the acesss token token (`token/refresh/`))
  
3. To upload the file (Endpoint: 1 in the task document)
```bash
curl -F 'file=@/path/to/project/atlan_task/upload-files/100000-Sales-Records.csv' http://localhost:8000/collect/baseline/ -H "Authorization: Bearer {access token}"
```
Replace `path/to/project` with the path where you cloned the repo. In my case this was `@/Users/bhavesh/PycharmProjects/atlan-task/atlan_task/upload-files/100000-Sales-Records.csv`.  
Please use the files already provided(I've hardcoded the datetime format and other small details)
Replace `{access_token}` with the access token that you received in step2

The response should be something like this
```bash
{"id":1,"file":"https://atlan-task-assets.s3.amazonaws.com/file/100000-Sales-Records.csv"}%
```
The uploaded file has not been uploaded to Amazon s3.

Now if you check the console, you can see the data being imported into the db by the background celery worker.

A background celery worker downloads the uploaded file from S3 and starts importing the data into db. You can check the console.

If you try to upload another file during this process you get the following error message

`{
    "detail": "You do not have permission to perform this action."
}`

You can check all the files uploaded by the user by running the following command
```bash
curl -X GET "localhost:8000/collect/baseline/" -H "Authorization: Bearer {access_token}"
```

Replace `{access_token}` with a valid access token

You should get a response like the following
```bash
{
   "count":1,
   "next":null,
   "previous":null,
   "results":[
      {
         "id":1,
         "file":"https://atlan-task-assets.s3.amazonaws.com/file/100000-Sales-Records.csv"
      }
   ]
}
```

The list is paginated.

To delete the data associated with the uploaded file
```bash
curl -X "DELETE" localhost:8000/collect/baseline/{id}/ -H "Authorization: Bearer {access_token}"
```

Replace `{access_token` with a valid access token  
Replace `{id}` with the id of the uploaded file. You can find the `id` in the the previous response (the response that you get after uploading the file).  

If the data is still being imported to the database in the back-ground. It does not let you cancel the task. (as specified in the task document). You can delete the data (use the endpoint specified above) after the data has been imported to the database.  

4. Example 2 endpoint in the task  

Send a GET request with proper JWT Token in the format specied above.

Endpoint: `localhost:8000/collect/data/?from=2015-08-01`

The response are paginated.

```bash
curl "localhost:8000/collect/data/?from=2015-08-01" -H "Authorization: Bearer {access_token}"
```

5. Example 3 endpoint in the task

You can use Flower to check the status of the tasks.  

``` bash
curl -F 'file=@/path/to/project/atlan_task/upload-files/team_data.csv' http://localhost:8000/collect/team/ -H "Authorization: Bearer {access_token}"
```

The response would be something like this

```bash
{
   "id":1,
   "file":"https://atlan-task-assets.s3.amazonaws.com/file/team_data_zIkb5K3.csv"
}
```

A celery background worker downloads the file from s3 and starts creating the teams.

Now to cancel this process (to stop the celery worker from creating teams and deleting all the teams created up until now from the uploaded file, `revoking` the task )   

Now check flower(localhost:5555), the task would have been revoked.  


```bash
curl -X "DELETE" localhost:8000/collect/team/{id}/ -H "Authorization: Bearer {access_token}"
```

Replace `{access_token}` with a valid access token  
Replace `{id}` with the id of the uploaded file. You can find the `id` in the the previous response (the response that you get after uploading the file)

