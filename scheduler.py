import datetime
from threading import Timer
from flask import jsonify
import logging

logging.basicConfig(level=logging.DEBUG)
scheduled_tasks = []


def schedule_task(script_name, start_date, start_time, run_script):
    try:
        run_datetime = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        delay = (run_datetime - datetime.datetime.now()).total_seconds()

        if delay < 0:
            logging.error(f"Scheduled time {start_date} {start_time} is in the past.")
            return jsonify({'status': f'Error: Scheduled time {start_date} {start_time} is in the past'}), 400

        t = Timer(delay, run_script, args=(script_name,))
        t.start()

        task = {
            'script_name': script_name,
            'run_date': start_date,
            'run_time': start_time,
            'thread': t
        }

        scheduled_tasks.append(task)
        logging.info(f'Script {script_name} scheduled for {start_date} at {start_time}.')
        return jsonify({'status': f'Script {script_name} scheduled for {start_date} at {start_time}'}), 200
    except Exception as e:
        logging.error(f"Error scheduling script {script_name}: {str(e)}")
        return jsonify({'status': f'Error scheduling script: {str(e)}'}), 500


def stop_scheduled_task(script_name=None):
    global scheduled_tasks
    logging.info(f"Attempting to stop tasks. Current tasks: {len(scheduled_tasks)}")
    tasks_to_remove = []
    if script_name:
        tasks_to_remove = [task for task in scheduled_tasks if task['script_name'] == script_name]
        if not tasks_to_remove:
            logging.error(f'No scheduled task found for {script_name}.')
            return jsonify({'status': f'No scheduled task found for {script_name}'}), 400
    else:
        tasks_to_remove = scheduled_tasks.copy()  # Copy the list to avoid modifying while iterating

    for task in tasks_to_remove:
        logging.info(f"Cancelling task: {task['script_name']}")
        task['thread'].cancel()
        scheduled_tasks.remove(task)

    if script_name:
        logging.info(f'Scheduled task for {script_name} cancelled.')
        return jsonify({'status': f'Scheduled task for {script_name} cancelled'})
    else:
        logging.info('All scheduled tasks stopped.')
        scheduled_tasks = []  # Clear the scheduled_tasks list
        return jsonify({'status': 'All scheduled tasks stopped.'})


def schedule_monthly_task(script_name, start_date, start_time, run_script):
    try:
        start_datetime = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        current_datetime = start_datetime

        def schedule_next_run():
            nonlocal current_datetime
            delay = (current_datetime - datetime.datetime.now()).total_seconds()

            if delay < 0:
                # If the scheduled time has passed, move to the next month
                current_datetime = current_datetime.replace(day=1, month=current_datetime.month + 1)
                schedule_next_run()
                return

            t = Timer(delay, run_and_reschedule)
            t.start()

            task = {
                'script_name': script_name,
                'run_date': current_datetime.strftime("%Y-%m-%d"),
                'run_time': start_time,
                'thread': t
            }

            scheduled_tasks.append(task)
            logging.info(f'Script {script_name} scheduled for {current_datetime.strftime("%Y-%m-%d")} at {start_time}.')

        def run_and_reschedule():
            run_script(script_name)
            # Move to the next month
            nonlocal current_datetime
            current_datetime = current_datetime.replace(day=1, month=current_datetime.month + 1)
            schedule_next_run()

        schedule_next_run()

        return jsonify({'status': f'Script {script_name} scheduled monthly from {start_date} at {start_time}'}), 200
    except Exception as e:
        logging.error(f"Error scheduling script {script_name}: {str(e)}")
        return jsonify({'status': f'Error scheduling script: {str(e)}'}), 500


def get_scheduled_tasks():
    return scheduled_tasks
