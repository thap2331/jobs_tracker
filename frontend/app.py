import sys
sys.path.insert(0, '.')

from flask import Flask, render_template, request, url_for, redirect, flash
from psycopg2.extras import RealDictCursor
import sqlite3, psycopg2, os, time, subprocess, json

from database.db_configs import GetDBCreds
from database.db_manager import DBConnect
import datetime
from utils.utils import DateTimeUtils
from build_cron_job import BuildCron

conn_string             = GetDBCreds().get_conn_string_python_psycopg2()
absolute_path_from_env  = GetDBCreds().get_absolute_path()
run_mode                = GetDBCreds().get_runmode()


app = Flask(__name__)
app.config['SECRET_KEY'] = '6d1209d285f8030865a7faac38ec5b5e4c5d11fa994f0854'

# Create SQL conn
def get_db_connection():
    try:
        conn = psycopg2.connect(conn_string)
        return conn
    except Exception as e:
        print("Cannot connect to pg using ",conn_string, '\n error:', e)

# Get one row
def get_row(table, column, values):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{values}'")
    row = cursor.fetchone()
    conn.close()
    return row

# Homepage
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM joblisting')
    searchTableData = cursor.fetchall()

    cursor.execute('SELECT * FROM jobs')
    resultsTableData = cursor.fetchall()

    cursor.execute('SELECT * FROM cronjobslist')
    cronJobListData = cursor.fetchall()

    cursor.execute('SELECT * FROM cronlogs')
    cronlogsData = cursor.fetchall()
    if cronlogsData:
        for row in cronlogsData:
            print(row.get("last_attempted_crawl"), type(row.get("last_attempted_crawl")))
            last_attempted_crawl = row.get("last_attempted_crawl")
            if isinstance(last_attempted_crawl, datetime.datetime):
                row["last_attempted_crawl"] = DateTimeUtils().convert_utc_to_pst(row.get("last_attempted_crawl"))
    
    cursor.execute('SELECT * FROM crawlogs')
    crawledData = cursor.fetchall()
    if crawledData:
        for row in crawledData:
            last_attempted_crawl = row.get("last_attempted_crawl")
            if isinstance(last_attempted_crawl, datetime.datetime):
                row["last_attempted_crawl"] = DateTimeUtils().convert_utc_to_pst(row.get("last_attempted_crawl"))
    
    conn.close()
    activeTab = request.args.get("activeTab") if request.args.get("activeTab") else "scraping-list" 
    return render_template(
        'index.html',
        searchTableData = searchTableData, 
        resultsTableData = resultsTableData,
        cronJobListData = cronJobListData,
        cronlogsData = cronlogsData,
        crawledData = crawledData,
        runMode     = run_mode,
        activeTab   = activeTab
        )


# Add new search row
@app.route('/add_search', methods=('GET', 'POST'))
def add_search():
    if request.method == 'POST':
        exists = get_row('joblisting','url',request.form['url'])

        company_name = request.form['company_name']
        job_title = request.form['job_title']
        url = request.form['url']
        company_website = request.form['company_website']

        if exists:
            flash("The url already exists in the database. If you would like to alter information for this entry, use the update option.")
        elif not job_title:
            flash('Job title is required!')
        elif not url:
            flash('Job listings link is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO joblisting (company_name, job_title, url, company_website) VALUES (%s, %s, %s, %s)', (company_name, job_title, url, company_website))

            conn.commit()
            conn.close()
            return redirect(url_for('index', activeTab='scraping-list'))

    return render_template('add_search.html')


# Navigate to update page
@app.route('/update', methods=('POST',))
def update():
    row = get_row('joblisting','url',request.form['link'])
    return render_template('update.html', row=row)


# Update search row
@app.route('/send_update', methods=('POST',))
def send_update():
    company_name = request.form['company_name']
    job_title = request.form['job_title']
    url = request.form['url']
    company_website = request.form['company_website']

    exists = get_row('joblisting','url',url)

    if exists and url != request.form['original_link']:
        flash('This url already appears in another entry. Please enter a unique url.')
    elif not job_title:
        flash('Job title is required!')
    elif not url:
        flash('Job listings link is required!')
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE joblisting SET company_name = %s, job_title = %s, url = %s, company_website = %s WHERE url = %s', (company_name, job_title, url, company_website, request.form['original_link']))

        conn.commit()
        conn.close()
        return redirect(url_for('index', activeTab='scraping-list'))
    
    return render_template('update.html', row = get_search_row(request.form['original_link']))


# Delete new search row
@app.route('/delete', methods=('POST',))
def delete():
    del_type = request.form['del_type']

    activeTab="scraping-list"
    if del_type == 'joblisting':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM joblisting WHERE url = %s', (request.form['link'],))
    elif del_type == "cronjobslist":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cronjobslist WHERE cronid = %s', (request.form['cronid'],))
        activeTab="cronjobs-list"
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE job_link = %s', (request.form['link'],))

    conn.commit()
    conn.close()
    return redirect(url_for('index', activeTab=activeTab))

# Add new search row
@app.route('/add_cronjob', methods=('GET', 'POST'))
def add_cronjob():
    exists=False
    if request.method == 'POST':

        absolute_path   = request.form['absolute_path']
        jobtype         = request.form['jobtype']
        cronjob         = request.form['cronjob']
        boxtype         = request.form['boxtype']

        if not absolute_path:
            absolute_path = absolute_path_from_env

        if exists:
            flash("The url already exists in the database. If you would like to alter information for this entry, use the update option.")
        elif not absolute_path:
            flash(f'Absolute Path is required! Either put it in env file or fill it in.')
        else:
            BuildCron().build_cron_job_commands(
                absolute_path=absolute_path,
                jobtype=jobtype,
                cronjob=cronjob,
                boxtype=boxtype
                )
            return redirect(url_for('index', activeTab='cronjobs-list'))

    return render_template('add_cron_job.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)