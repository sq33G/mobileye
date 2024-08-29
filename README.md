# mobileye
## Take-home assignment

To set up, use pipenv to prepare local virtual environment

    pipenv install
    pipenv shell

To run, start the django server from the `pipe_dream` folder

    python manage.py runserver

Use the REST API to define jobs to run.
Once you have jobs defined to run, you can start the scheduler.
For the current exercise, the assumption is that this command will be
run as a cron job.

    python tasks.py

Once the job has been run, it will not run again for 24 hours. To overcome
this for easy testing, you can use the django admin interface to reset the last
scheduler run time.
