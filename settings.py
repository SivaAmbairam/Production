import signal
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess
import os
import logging
from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task, scheduled_tasks

app = Flask(__name__)
SCRIPTS_DIRECTORY = r"C:\Users\G6\PycharmProjects\WebScrappingWithWebPage/Scrapping Scripts"

UNWANTED_SCRIPTS = ['module_package.py']
@app.route('/')

@app.route('/settings')
def settings():
    return render_template('setting.html')


if __name__ == '__main__':
    app.run(debug=True)
