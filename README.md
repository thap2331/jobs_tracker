# What is jobs_tracker

### What is the repo about?

- Assume you want to apply for jobs to specific companies that you care about. In addition, assume, you only want the notifications to specific category of jobs, example, data analyst or, economist.
- We want to create a repo that will allow you to quickly do it and gives you the flexibility the extend it.

### Benefits

- Given the size of the database you need, you can easily store everything in your local box.
- Set up your email and cron job. Then, you are done. (Well, thats the plan.)
- Add companies you want. If the companies are not listed, extend it yourself and contribute to this project.

### Supported OS system

- Linux: Easy support in Linux boxes for now.
- MacOS: To be tested
- Windows: Get (git) bash on windows.


# Set up for a developer

### First time use
  - `git clone [repo]`
  - Copy .env.example and create .env.dev file. 
    - `cp .env.example .env.dev`
    - Fill out `.env.dev` file as needed. Fill `run_mode=test`.
  - Ensure you can run docker as a user. Check [post-install](https://docs.docker.com/engine/install/linux-postinstall/) for linux.

##### Setup

- Set up your environment `source setenv.sh test`
- Run `docker compose up` . Wait till all services are up.
- Now, run `setup/test_setup.sh` to create tables in your test database.
  This will also add a few sample rows.
  - Now go to [localhost:5000](http://localhost:5000/). You should see a page.

### Start crawling
- Run crawl
  - `docker exec -it setup_box bash -c "python scraping/crawl.py"`

### Shut down
- Run `remove_container_images.sh` to remove all images, containers, volumes, and network.
  - NOTE: It will delete all your data as it will take down all the volumes.


# Other

### Supported Organizations

- texastribune
- onx

### Things to do next (order by priority)

- ~~Pull settings from database for crawler~~
- ~~Url join~~
- ~~Front-end~~
- ~~Add do not follow these links such as .pdf~~
- ~~Add email method~~
- ~~request to add your email and one pass~~
- ~~add render in config~~
- ~~allow ability to recrawl without restarting~~
- ~~title with dash~~
- ~~add a db for supported websites - not sure what I was thinking~~
- ~~Allow email if not notified yet~~
- Add to crawl logs when crawl runs, columns: jl, last_attempted_crawl,
- Add cron job
  - To run crawl
  - To send emails
- keep things in docker
  - ~~initialize test db~~
  - ~~allow crawl for test~~
  - ~~allow prod for frontend~~
  - ~~allow crawl for prod~~
  - allow ability to run dead container and set up from there
- Frontend
  - when trying to update we see: `This url already appears in another entry. Please enter a unique url.`
  - convert db connect in flask app to sqlalchmy
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
  - ~~allow render for job posting pages as well~~
- ~~add capability to be less verbose sqlite/~~
- Tests
  - Unit tests

- Bug
-- progress bar has % sign at the end

- Annoying things
-- ~~sqlite verbose~~
-- Add progress bar for pages scraped

# Planned feature extension

- ~~Allow Postgres and SQLite option (or more as needed)~~
- ~~Add front end functionality to add job websites to database~~
- ~~Use containerized services~~
- Use scrapy and handle data pipeline through scrapy pipeline
- Create a table with a organization's website, its name, jobs website, ats if exists.

### Personal motivation

- In addition to the above annoyance about checking jobs everyday, I wanted to use bash as much as possible in this project (just for learning purposes). I am not against other language ideas.

### Scraping strategy

- check for settings, see if title in link, page title, and then in page
- if no settings keep strategy of going through all three strategy

### Tests need to be added

- validate url
- url normalizer
-


### Email config
- https://realpython.com/python-send-email/
- https://stackoverflow.com/questions/73026671/how-do-i-now-since-june-2022-send-an-email-via-gmail-using-a-python-script
- https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
