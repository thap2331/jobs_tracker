# What is jobs_tracker

# How to use

- First time use
-- git clone repo
-- bash shell_scripts/start_clean_slate.sh

- You can do below to add job listing page
-- Add a job listing
  `python3 tracker/add_job_listing.py -u https://www.onxmaps.com/join-our-team -jt "backend engineer"`
-- You can do below to crawl
  `pythonr scraping/crawl.py`

### What is the repo about?

- Assume you want to apply for jobs to specific companies that you care about. In addition, assume, you only want the notifications to specific category of jobs, example, data analyst or, economist.
- We want to create a repo that will allow you to quickly do it and gives you the flexibility the extend it.

### Benefits

- Given the size of the database you need, you can easily store everything in your local box.
- Set up your email and cron job. Then, you are done. (Well, thats the plan.)
- Add companies you want. If the companies are not listed, extend it yourself and contribute to this project.

### Supported OS system

- In Linux boxes only for now.

### Supported Organizations

- texastribune
- onx

### Things to do next (order by priority)

- ~~Pull settings from database for crawler~~
- ~~Url join~~
- ~~Front-end~~
- ~~Add do not follow these links such as .pdf~~
- Allow email if not notified yet
- Add cron job
- Front end
- see if title is in the headings
- allow crawl for all by catching exception and logging them
- allow ability to load jobs from past and skip seen jobs
- for add job listing, allow capability to add job posting or view job listing to be added, check for duplicates
- Optimize the crawlers
- add capability to be less verbose sqlite/

# Planned feature extension

- Allow Postgres and SQLite option (or more as needed)
- Add front end functionality to add job websites to database
- Use containerized services
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
