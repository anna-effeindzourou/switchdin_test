# This script addresses point 1 of the test
# The process publishes a random number between 1 and 100 to an MQTT topic in a message broker
# at a random interval between 1 and 30 seconds.

from random import randint
import sys
from time import sleep
import logging

from constants import QUEUE_NAME, USERNAME, PASSWORD
from custom_exceptions import PublishError
from utils import publish_to_queue

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')


def publish_random():
    # Pick a random number between 1 and 100
    random_number = randint(1, 100)
    # Pick a random number between 1 and 30.
    random_interval = randint(1, 30)

    # Pause
    sleep(random_interval)

    # Publish message
    try:
        publish_to_queue(USERNAME, PASSWORD, QUEUE_NAME, random_number)
    except PublishError as publish_error:
        raise PublishError(f"Could not publish random number to {QUEUE_NAME} ({publish_error})")


if __name__ == '__main__':
    try:
        while True:
            publish_random()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except PublishError as publish_error:
        logging.error(publish_error)
