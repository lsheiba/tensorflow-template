
import logging
from logging import config
import os
import sys

from mlboardclient.api import client


config.fileConfig("logging.conf")
SUCCEEDED = 'Succeeded'
FAILED = 'Failed'
LOG = logging.getLogger('TASKS')


def main():
    ml = client.Client()

    current_task_name = os.environ.get('TASK_NAME')
    LOG.info("Current task name = %s" % current_task_name)
    current_app = os.environ['APP_NAME']
    current_app_id = os.environ['APP_ID']
    
    LOG.info("Current app name = %s" % current_app)
    LOG.info("Current app id = %s" % current_app_id)

    app = ml.apps.get(current_app_id)
    
    for task in app.tasks:
        if task.name == current_task_name:
            continue
        
        LOG.info("Start task %s..." % task.name)
        started = task.start()
        
        LOG.info(
            "Run & wait [name=%s, build=%s, status=%s]"
            % (started.name, started.build, started.status)
        )
        completed = started.wait()
        
        if completed.status != SUCCEEDED:
            LOG.warning(
                "Task %s-%s completed with status %s." 
                % (completed.name, completed.build, completed.status)
            )
            LOG.warning("Workflow is completed with status ERROR")
            sys.exit(1)
        LOG.info(
            "Task %s-%s completed with status %s." 
            % (completed.name, completed.build, completed.status)
        )
    
    LOG.info("Workflow is completed with status SUCCESS")

if __name__ == '__main__':
    main()
