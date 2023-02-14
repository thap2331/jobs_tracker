# What is jobs_tracker

### What is the repo about?

- Assume you want to apply for jobs to specific companies that you care about. In addition, assume, you only want the notifications to specific category of jobs, example, data engineer, data analyst, or economist.
- The idea of this repo is to allow you to quickly do it and give you the flexibility the extend it.

### Benefits

- Given the size of the database you need, you can easily store everything in your local box.
- Set up once. Add the companies, job titles, your email and cron job. Then, you are done. (Well, thats the plan.)
- Add companies you want. If the companies are not listed, extend it yourself and contribute to this project.

## Setup

-   For developer's see this [developer's readme.](/developer_readme.md)

### First time use
- Get [Docker](https://docs.docker.com/get-docker/)
    - Ensure you can run docker as a user. Check [post-install](https://docs.docker.com/engine/install/linux-postinstall/) for linux.
- Clone repo `git clone [repo]`
- Go to jobs tracker directory, i.e. use command line and cd into it.
- Copy `.env.example` and create `.env` file. 
    - Run command: `cp .env.example .env`
    - Fill out rest of `.env` file as needed
        - Fill your `email` and `onePasswordEmail` if you want to send email from yourself.

### One time Setup (only once to set database tables)
- Go to jobs tracker directory, i.e. use command line and cd into it.
- To find current work directory and save in `.env` file, do below:
    - Find full path for this cloned repository. Use `pwd` in bash/zsh. Copy and paste it in `.env` file as `absolute_path=paste_path_here`.
- Now, run `bash setup/one_time_setup.sh` to start containers and create tables in your database.
  This will also add a few sample rows.
  - Now go to [localhost:5000](http://localhost:5000/). You should see a page with more data. 
- To see more data, ensure that you have [psql (link for linux)](https://www.postgresql.org/download/linux/) and use [these commands](/setup/command_line_cmds.sh) as you like.

### Start crawling
- Run crawl
    - For entry container and frontend, run `docker compose up prod_entrypoint frontend -d`
  - Wait for it to be done. Then run `docker exec -it prod_box bash -c "python scraping/crawl.py -f all"`. See [argparse](/scraping/crawl.py) for more options.


### Setup cron jobs
- Use frontend to generate command line code for cron jobs
    - Run `docker compose up prod_database frontend -d`
    - Go to `localhost:5000`
    - Go to tab `Cron Jobs Generator`.  Select `Add New Cronjob Entry`.
    - Rows to fill
        - Absolute Path
            - Check your `.env` file. Here you can add `absolute_path=` if it is not there yet.
            - Alternatively, you can manually find the repo path and add it there.
        - Job type
            - Default crawl. You can also add email option.
        - Cron Job
            - Go to https://crontab.guru/ and copy paste.
        - Box Type
            - Default is linux. Others are yet to be tested. Godspeed.
    - Hit submit. If you have absolute path in your env file, you can just hit submit if are ok with default options.
- Copy `Fullcronjob` command and paste it in your bash command line. Use `crontab -l` to see all cron jobs.
- Remove a cron jon. Copy `Remove cronjob` command and paste it in your bash command line. Use `crontab -l` to see all cron jobs.
    


### Supported OS system

- Linux: Easy support in Linux boxes for now.
- MacOS: To be tested
- Windows: Get (git) bash on windows. To be tested.


### Email config
- https://realpython.com/python-send-email/
- https://stackoverflow.com/questions/73026671/how-do-i-now-since-june-2022-send-an-email-via-gmail-using-a-python-script
- https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j

### Developer's readme
For developer's see this [developer's readme.](/developer_readme.md)