# This script addresses point 3 of the test
# The app subscribes to the queue defined in point 1, reads the random number from the broker, and calculates one
# minute, 5 minute, and 30 minutes averages. These are then sent back to the broker on a different topic.

from datetime import datetime, timedelta
import sys
import logging

from constants import USERNAME, PASSWORD, QUEUE_NAME, QUEUE_STAT
from custom_exceptions import PublishError, BrokerConnectionError
from utils import publish_to_queue, connect_broker


logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s")


class StatPublish:
    # This class is used to store the data and helper functions associated to the calculation of an average
    # for a specified duration - 1, 5 or 30mins
    def __init__(self, duration, stat_type):
        self.duration = duration
        self.duration_delta = timedelta(minutes=duration)
        self.stat_type = stat_type

        self.start_timer = datetime.now()
        self.current_sum = 0
        self.counter = 0

    def reset(self):
        self.current_sum = 0
        self.counter = 0
        self.start_timer = datetime.now()

    def add(self, random_number_received):
        self.current_sum += random_number_received
        self.counter += 1


def timer_add_compare(stat_publish, random_number_received):
    # This function is adds a value to the sum and publishes the data to the broker when required
    stat_publish.add(random_number_received)
    t_difference = datetime.now() - stat_publish.start_timer

    if t_difference >= stat_publish.duration_delta:
        avg = stat_publish.current_sum / stat_publish.counter
        msg = f"{stat_publish.stat_type}:{avg}"
        try:
            publish_to_queue(USERNAME, PASSWORD, QUEUE_STAT, msg)
        except PublishError as publish_stats_error:
            raise PublishError(
                f"Could not publish the following message {msg} to {QUEUE_STAT} ({publish_stats_error})"
            )

        stat_publish.reset()


def publish_stats():
    # this function establishes the connection to the broker and runs the process

    # connection to the broker
    try:
        _, channel = connect_broker(QUEUE_NAME, USERNAME, PASSWORD)
    except BrokerConnectionError as connection_error:
        raise BrokerConnectionError(f"Could not connect to broker ({connection_error})")

    # Initialisation of the counters and sums to calculate averages
    stat_publish_1min = StatPublish(1, "1")
    stat_publish_5mins = StatPublish(5, "5")
    stat_publish_30mins = StatPublish(30, "30")

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        random_number_received = int(body.decode())

        # Update sums and counters
        # push to the broker when the condition is met i.e the time elapsed is equal to the duration specified
        try:
            timer_add_compare(stat_publish_1min, random_number_received)
            timer_add_compare(stat_publish_5mins, random_number_received)
            timer_add_compare(stat_publish_30mins, random_number_received)
        except PublishError as error:
            raise PublishError(f"Could not publish stats ({error})")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        publish_stats()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
    except Exception as error:
        logging.error(error)
