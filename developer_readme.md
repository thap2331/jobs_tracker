
# Set up for a developer

### First time use
- Get [Docker](https://docs.docker.com/get-docker/)
    - Ensure you can run docker as a user. Check [post-install](https://docs.docker.com/engine/install/linux-postinstall/) for linux.
- Clone repo `git clone [repo]`
- Go to jobs tracker, i.e. cd into it.
- Copy `.env.example` and create `.env.dev` file.
    - Run command: `cp .env.example .env.dev`
    - Fill out rest of `.env.dev` file as needed
        - Fill `run_mode=test`. For prod, no need to fill this.
        - Fill your email.
        - Fill your `onePasswordEmail` if you want to send email from yourself. 
          - To be done: In future let's remove this and allow to email from your container box. Need to build send email feature from device/container.

### One time Setup (only once to set database tables)

- Go to jobs tracker, i.e. cd into it.
- Add absolute path on `.env.dev` file. 
  - To find current work directoyr and save in `.env.dev` file run below on bash 
    - `printf "\nabsolute_path=$(pwd)" >> .env.dev`
    - `echo "$(sort .env.dev | uniq)" > .env.dev`
  - or just copy paste your absolute path as `absolute_path=abs_path_of_directory`

- Set up your test environment `source setenv.sh test`
- Run `docker compose up test_entrypoint test_database -d`.   
    -   Wait till all services are up. Use `-d` to run in a detached mode.
- Now, run `bash setup/test_setup.sh` to create tables in your test database.
  This will also add a few sample rows.
  - Now go to [localhost:5000](http://localhost:5000/). You should see a page with more data. 
- To see more data, ensure that you have [psql (link for linux)](https://www.postgresql.org/download/linux/) and use [these commands](/setup/command_line_cmds.sh) as you line.

### Start crawling
- Run crawl
    - For test entry container, test db, frontend, run `docker compose up test_entrypoint test_database frontend -d`
  - Wait for it to be done. Then run `docker exec -it test_box bash -c "python scraping/crawl.py -f all"`. See [argparse](/scraping/crawl.py) for more options.

### Shut down
- Run `docker compose down` to stop containers.
- CAREFUL: Run `bash remove_container_images.sh` to remove all images, containers, volumes, and network.
  - NOTE: It will delete all your data because it will take down all the volumes.

### Setup cron jobs
- Use frontend to generate command line code for cron jobs
    - Run `docker compose up test_database frontend -d`
    - Go to `localhost:5000`
    - Go to tab `Cron Jobs Generator`. Select `Add New Cronjob Entry`.
    - Rows to fill
        - Absolute Path
            - Check your `.env.dev` file. Here you can add `absolute_path=` if it is not there yet.
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
    

# Other

### Supported Organizations on test env

- texastribune
- onx

### Things to do next (order by priority)

- Add cron job
  - Use .env file to find absolute path. `echo "$(sort .env.dev | uniq)" > .env.dev`
  - To run crawl in prod mode (for this work delete the repo and make readme as you set up for a prod.)
  - How to use relative links for a cron job
- keep things in docker
  - use frontend for adding cron jobs
  - research on orphan docker containers
  - Do not allow test container to spin up if the run mode is prod
- Frontend
  - when trying to update we see: `This url already appears in another entry. Please enter a unique url.`
  - convert db connect in flask app to sqlalchmy
  - cron job
    - crawl cron job
      - we need (1) full path of the folder
      - everything else is default (run crawl job, time it runs - every hour, linux)
      - once submitted, 
        - add cron job in your box
        - store in a database (seperate by space); do not allow to add more unless deleted
    - email cron job
      - we need (1) full path of the folder
      - everything else is default (run email job, time it runs - every hour, linux)
      - once submitted, store in a database (seperate by space); do not allow to add more unless deleted
  - delete db configs file and use file from outside

- Fill out test env including dummy data for all tables
- Crawling
  - Add option to crawl all job listings or few selected job listings
  - Allow crawling to select a few job listings
  - Allow crawling if not crawled in last 24 hours
  - Allow crawl logs to have when a website was crawled
  - allow crawl for all by catching exception and logging them
  - for add job listing, allow capability to add job posting or view job listing to be added, check for duplicates
  - crawl logs with capability to say how many new jobs found
  - Optimize crawers
    - Optimze the crawlers
- Crawling strategy
  - think about pagination - pagination in url param + pagination in
  - see if title is in the headings
  - allow ability to load jobs from past and skip seen jobs
  - Tighten render: always render and return markup. First, request html and then selenium render.

- Tests
  - Unit tests
- Keep tracker dirctory inside database folder

- Bug
-- progress bar has % sign at the end

- Annoying things
  - Add progress bar for pages scraped

- Database work
  - A column of cronjobs is written as `last_attempted_crawl`. Change this to `last_attempted` and then update it wherever it get impacted.
  - work with database from one place only, i.e., interact with it using one class
- Email work
  - Allow email from a given box without requiring from one's email.


# Planned feature extension

- Use scrapy and handle data pipeline through scrapy pipeline
- Create a table with a organization's website, its name, jobs website, ats if exists.


### Scraping strategy


### Tests need to be added

- validate url
- url normalizer