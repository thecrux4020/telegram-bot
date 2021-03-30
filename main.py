import telegram
import os
import logging
import configparser

from app.jobs.polls import Poll

DEFAULT_CONFIG_NAME = "settings.ini"
bot = channel_id = config = None

def setup_logging():
    """ Basic logging setup """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
def get_config():
    """ Read configuration file, and returns a configparser object """
    conf = configparser.ConfigParser()
    conf.read(DEFAULT_CONFIG_NAME)
    return conf

def should_start_webhook(operation_mode):
    """ Check if operation mode is webhook, and returns True or False """
    if operation_mode == "webhook":
        return True
    return False

def should_start_jobs(operation_mode):
    """ Check if operation mode is jobs, and returns True or False """
    if operation_mode == "jobs":
        return True
    return False

def get_job_by_name(name):
    """ Given a job name, instance the corresponding class and return it """
    if name == "POLL":
        job = Poll.setup(bot, channel_id, config)
    elif name == "METRICS":
        pass
    else:
        raise ValueError("Invalid job name. You must provide a valid job name inside \"JOB_NAME\" environment variable")

    return job

def start_jobs():
    """ Get job name from environment, and start the job """
    job_name = os.environ.get("JOB_NAME")
    job = get_job_by_name(job_name)
    job.start_job()

def main():
    # Security sensitive parameters got from environment..
    telegram_token = os.environ.get("TELEGRAM_TOKEN")

    # Other common parameters, get from config file
    global config
    config = get_config()
    global channel_id
    channel_id = config["telegram"]["channel_id"]
    operation_mode = config["app"]["operation_mode"]

    # Setup common things
    setup_logging()
    global bot
    bot = telegram.Bot(token=telegram_token)

    # Jobs startup logic
    if should_start_jobs(operation_mode):
        start_jobs()
    
    # Webhook startup logic
    if should_start_webhook(operation_mode):
        pass

def lambda_handler(event, context):
    main()

if __name__ == "__main__":
    main()