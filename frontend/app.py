from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '6d1209d285f8030865a7faac38ec5b5e4c5d11fa994f0854'


# Create SQL conn
def get_db_connection():
    conn = sqlite3.connect('../database/jobs.db')
    conn.row_factory = sqlite3.Row
    return conn


# Get search row
def get_search_row(link):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM joblisting WHERE url = ?', (link,)).fetchone()
    conn.close()
    return row


# Get results row
def get_results_row(link):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM jobs WHERE job_link = ?', (link,)).fetchone()
    conn.close()
    return row


# Homepage
@app.route("/")
def index():
    conn = get_db_connection()
    searchTableData = conn.execute('SELECT * FROM joblisting').fetchall()
    resultsTableData = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('index.html', searchTableData = searchTableData, resultsTableData = resultsTableData)


# Add new search row
@app.route('/add_search', methods=('GET', 'POST'))
def add_search():
    if request.method == 'POST':
        exists = get_search_row(request.form['url'])

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
            conn.execute('INSERT INTO joblisting (company_name, job_title, url, company_website) VALUES (?, ?, ?, ?)', (company_name, job_title, url, company_website))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('add_search.html')


# Navigate to update page
@app.route('/update', methods=('POST',))
def update():
    row = get_search_row(request.form['link'])
    return render_template('update.html', row=row)


# Update search row
@app.route('/send_update', methods=('POST',))
def send_update():
    company_name = request.form['company_name']
    job_title = request.form['job_title']
    url = request.form['url']
    company_website = request.form['company_website']

    exists = get_search_row(url)

    if exists and url != request.form['original_link']:
        flash('This url already appears in another entry. Please enter a unique url.')
    elif not job_title:
        flash('Job title is required!')
    elif not url:
        flash('Job listings link is required!')
    else:
        conn = get_db_connection()
        conn.execute('UPDATE joblisting SET company_name = ?, job_title = ?, url = ?, company_website = ? WHERE url = ?', (company_name, job_title, url, company_website, request.form['original_link']))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('update.html', row = get_search_row(request.form['original_link']))


# Delete new search row
@app.route('/delete', methods=('POST',))
def delete():
    del_type = request.form['del_type']

    if del_type == 'joblisting':
        conn = get_db_connection()
        conn.execute('DELETE FROM joblisting WHERE url = ?', (request.form['link'],))
    else:
        conn = get_db_connection()
        conn.execute('DELETE FROM jobs WHERE job_link = ?', (request.form['link'],))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))