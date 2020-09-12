# Heritage at Risk RESTful API Server

## Introduction

Heritage at Risk RESTful API server is a server application that allows heritage lovers to submit reports about heritage at risks. A report is composed of information that describes an heritage at risk, and a series of photos of this heritage at risk taken by the user. The server application gathers all the reports and makes them publicly available to inform the international community and to encourage corrective action.

## What the project does

Develop the Heritage at Risk RESTful API server application to handle thousands of daily reports from all over the world. This API server supports for 4 main endpoints:

- POST `/account/session`: Support Sign-Up Sign-In for the HTTP method POST: </br>

  The HTTP method POST to the endpoint /account/session performs two actions:

  - Create an account for the user (sign-up), if the email address passed along the HTTP request is not already registered.
  - Create a login session for the user (sign-in), if none already active for this account.

  Returns a JSON expression containing the following attributes:.

  - account_id: Identification of the account of a user
  - expiration_time: Date and time when this report has been expired to the server platform.
  - session_id: Identification of the session as registered in the server platform.

- POST `/report`: Support Create a report for the HTTP method POST </br>

  Returns a JSON expression containing the following attributes:.

  - Creation_time: Date and time when this report has been registered to the server platform.
  - Report_id: Identification of the report as registered in the server platform.

- POST `/report/<uuid:report_id>/photo`: Support Add report photo for the HTTP method POST

  `report_id` (a UUID string) representing the identification of the report to add the photo to.

  Returns a JSON expression containing the following attributes:

  - creation_time: Date and time when this photo has been registered to the server platform.
  - photo_id: Identification of the photo as registered in the server platform.
  - report_id: Identification of the report as registered in the server platform.

- DELETE `/report/<uuid:report_id>'`: Support Delete a report for the HTTP method DELETE
  `report_id` (a UUID string) representing the identification of the report to delete the photo to.

  Returns a JSON expression containing the following attributes:

  - creation_time: Date and time when this photo has been registered to the server platform.
  - photo_id: Identification of the photo as registered in the server platform.
  - report_id: Identification of the report as registered in the server platform.

## Usage Information

### Prerequisites

- Python `3.6+` is required.
- PostgreSQL `10.12+`. Extension `Postgis`

### Usage

- Clone the repository:
  ```
  git clone https://github.com/intek-training-jsc/har-restful-api-server-hoaithu1.git
  ```
- Setup a directory to install
  ```
  $ mkdir ~/Documents/username/har-restful-api-server-hoaithu1
  $ cd ~/Documents/username/har-restful-api-server-hoaithu1
  ```
- Install our Flickr mirroring utility `pipenv install` to install virtual environment.
- Run a Python virtual environment: `$ pipenv shell`
- Get help our Bash script
  `$ mirror_flickr --help`
- Check local variables environment. Below is my default setting:

  ```
  # Define the connection we need to connect to database
  DATABASE_TYPE = 'postgresql'
  DATABASE_CONNECTOR = 'psycopg2'
  USERNAME = 'postgres'
  PASSWORD = 'postgres'
  HOST = '127.0.0.1'
  PORT = '5432'
  DATABASE_NAME = 'heritage'
  UPLOADED_FOLDER = '~/var/lib/har/photo'
  ```

  _Note_:

  - As my default config, you need to create a database `postgresql` with name `heritage`
  - You can set your own variables environment at file with path `./har_restapi/config.py`

* Demonstration:

  - Firstly you need to r`egister your application`:

    ```bash
    (har-restful-api-server-hoaithu1) ltthoai@IEPC0041:~/Documents/hoai/har-restful-api-server-hoaithu1$ python3
    Python 3.7.4 (default, Sep  2 2019, 20:47:34)
    [GCC 7.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from har_restapi import create_app
    >>> from har_restapi.models import Application, db
    >>>
    >>> app = create_app()
    >>> ctx = app.app_context()
    >>> ctx.push()
    >>> db.create_all()
    >>> application = Application("Heritage at Risk Mobile Application")
    >>> db.session.add(application)
    >>> db.session.commit()
    ```

  - Executive example: `$ ./run.py` </br>

    ```
    (har-restful-api-server-hoaithu1) ltthoai@IEPC0041:~/Documents/hoai/har-restful-api-server-hoaithu1$ ./run.py
    * Serving Flask app "har_restapi" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: on
    18:23:01.415 INFO _internal-_log:  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    18:23:01.416 INFO _internal-_log:  * Restarting with stat
    18:23:01.704 WARNING _internal-_log:  * Debugger is active!
    18:23:01.709 INFO _internal-_log:  * Debugger PIN: 172-276-153

    ```

  - Call API (As Client Side):

    - Connect to the database

      ```
      (har-restful-api-server-hoaithu1) ltthoai@IEPC0041:~/Documents/hoai/har-restful-api-server-hoaithu1$ psql -U postgres heritage
      psql (10.12 (Ubuntu 10.12-0ubuntu0.18.04.1))
      Type "help" for help.

      heritage=# \d
                    List of relations
      Schema |       Name        | Type  |  Owner
      --------+-------------------+-------+----------
      public | account           | table | postgres
      public | application       | table | postgres
      public | geography_columns | view  | postgres
      public | geometry_columns  | view  | postgres
      public | photo             | table | postgres
      public | raster_columns    | view  | postgres
      public | raster_overviews  | view  | postgres
      public | report            | table | postgres
      public | session           | table | postgres
      public | spatial_ref_sys   | table | postgres
      (10 rows)

      heritage=# select * from application;
      heritage=#
      ```

    - Get the `Consumer_Key` of the application.

      ```
      heritage=# select * from application;

      ```

      Here I get `Consumer_Key`: `60b0f3eb210748a3997e56fec9613858`

    - Create a Session:

      ```bash
      $ curl -X POST http://127.0.0.1:5000/account/session \
          content-type: application/json
          -H 'Content-Type: application/json' \
          -H 'X-API-Key: 60b0f3eb210748a3997e56fec9613858' \
          -H 'X-API-Sig: 4bad796430ee17bce569f94571e94d62c2511d8b' \
          -d '{"email_address": "daniel.caune@intek.edu.vn", "password": "7Dj3VEE8Z9j4E4Jv"}'
      ```

      _Note_: You may not get the responses `error: 400` as below.

      ```
      {
          "error": 400,
          "message": "Invalid Request Signature"
        }
      ```

      The reason here is that your `X-API-Sig` does not correct. To get the the access, take a look at the console and find the `X-API-Sig` which is logged. In this case, here is our `X-API-Sig`: `f65a67fcacf34c32cf1d76d9a61b6d2ae9fd5551`

      ```bash
      (har-restful-api-server-hoaithu1) ltthoai@IEPC0041:~/Documents/hoai/har-restful-api-server-hoaithu1$ ./run.py
      * Serving Flask app "har_restapi" (lazy loading)
      * Environment: production
        WARNING: This is a development server. Do not use it in a production deployment.
        Use a production WSGI server instead.
      * Debug mode: on
      21:05:44.437 INFO _internal-_log:  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      21:05:44.437 INFO _internal-_log:  * Restarting with stat
      21:05:44.717 WARNING _internal-_log:  * Debugger is active!
      21:05:44.723 INFO _internal-_log:  * Debugger PIN: 172-276-153
      21:05:48.641 INFO models-authenticate_application: expected_consumer_secret f65a67fcacf34c32cf1d76d9a61b6d2ae9fd5551
      21:05:48.643 INFO _internal-_log: 127.0.0.1 - - [16/Jun/2020 21:05:48] "POST /account/session HTTP/1.1" 200 -

      ```

      - Re-Create the session:

      ```bash
      $ curl -X POST http://127.0.0.1:5000/account/session \
          content-type: application/json
          -H 'Content-Type: application/json' \
          -H 'X-API-Key: 60b0f3eb210748a3997e56fec9613858' \
          -H 'X-API-Sig: f65a67fcacf34c32cf1d76d9a61b6d2ae9fd5551' \
          -d '{"email_address": "daniel.caune@intek.edu.vn", "password": "7Dj3VEE8Z9j4E4Jv"}'
      ```

      We got the responses:

      ```
        {
          "account_id": "e81922fe-7f1a-43ef-a812-0a9d8cfff44c",
          "expiration_time": "Thu, 16 Jul 2020 07:05:44 GMT",
          "session_id": "c56cc442-37a3-434f-88aa-534cbb62c917"
        }
      ```

## Contact Information

- If you have any problems using this library, please use the contact below.
  `Email: hoai.le@f4.intek.edu.vn`
