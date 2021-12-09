# Appointment Scheduler

This is a basic appointment booking system with get and create capability. Each user can book at most one appointment per day at any time on the hour or half hour.

## How to Run
From the base folder of the project and with docker started run:
1. `sudo docker build --tag appointment-scheduler .`
2. `sudo docker run --name appointment-scheduler -p 5000:5000 appointment-scheduler`

Commands can then be run in the Docker CLI that can be accessed from the **Containers** section of the Docker dashboard.

## Commands

### Creating Appointments
Appointments are created with a POST request with a JSON input.

It supports JSON input in the following format:
```
{
    "user_id": int // Any positive integer
    "datetime": int // A unix timestamp
}
```

Example query: `curl -i -X POST -H 'Content-Type: application/json' -d '{"user_id": 345, "datetime": 1638736207}' http://127.0.0.1:5000/create`

### Getting Appointments
Appointments can be fetched for any particular user with a GET request. The `user_id` can be any positive integer and is passed in as a query parameter.

Example query : `curl -i -X GET http://localhost:5000/appointments?user_id=345`

## Future To-Do's

With more time, I'd add some unit tests for this HTTP server to check the happy path as well as potential edge cases.