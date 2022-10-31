# This script addresses point 4 of the test
# This application subscribes to the statistics calculated in point 3, and prints these out in the console.

import sys
import logging

from constants import QUEUE_STAT, USERNAME, PASSWORD
from custom_exceptions import BrokerConnectionError
from utils import connect_broker

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')


def display_stats():
    # connection to the broker
    try:
        _, channel = connect_broker(QUEUE_STAT, USERNAME, PASSWORD)
    except BrokerConnectionError as connection_error:
        raise BrokerConnectionError(f"Could not connect to broker ({connection_error})")

    def callback(ch, method, properties, body):
        # Print the results into the console
        result = body.decode()
        res_split = result.split(":")

        print(f"\t{res_split[0]}\t\t | \t {res_split[1]} ")

    channel.basic_consume(queue=QUEUE_STAT, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    print("+------------------------+------------------------+")
    print(f"\tDuration (min)\t | \t Mean value ")
    print("+------------------------+------------------------+")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        display_stats()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except Exception as error:
        logging.error(error)
