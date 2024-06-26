import signal
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess
import os
import logging
from scheduler import schedule_task, stop_scheduled_task, get_scheduled_tasks, schedule_monthly_task, scheduled_tasks
from database import get_connection

app = Flask(__name__)

@app.route('/')

def settings():
    try:
        return render_template('settings.html')
    except Exception as e:
        logging.error(f"Error loading scripts: {str(e)}")
        return jsonify({'status': f'Error loading scripts: {str(e)}'}), 500


@app.route('/db_connection', methods=['POST'])
def db_connection():
    try:
        username = request.form.get('user-name')
        password = request.form.get('password')
        schema = request.form.get('schema')

        connection_properties = {
            'user': username,
            'password': password,
            'integratedSecurity': 'true',
            'authenticationScheme': 'NTLM',
            'domain': 'fsi'
        }

        response = get_connection()
        return jsonify({'status': response})
    except Exception as e:
        logging.error(f"Error in connection: {str(e)}")
        return jsonify({'status': f'Error in connection: {str(e)}'}), 500


@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')


if __name__ == '__main__':
    app.run(debug=True)