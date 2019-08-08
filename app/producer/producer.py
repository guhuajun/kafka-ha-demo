# -*- coding: utf-8 -*-
# pylint: disable=


import os
import logging
import time
import uuid
from datetime import datetime
from random import randint

import kafka
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic


if __name__ == "__main__":
    # change logging config
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s.%(msecs)03d][%(filename)s:%(lineno)d][%(levelname)s]%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__file__)

    bootstrap_servers = ["kafka1:19092", "kafka2:29092", "kafka3:39092"]

    def create_test_topic():
        client_id = 'producer-{0}'.format(str(uuid.uuid4()))
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers, client_id=client_id)

        topic_list = [NewTopic(name="test-{0}".format(str(x)),
                               num_partitions=10, replication_factor=3) for x in range(1, 6)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

    def send_message():
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

        counter = 0
        while True:
            topic = 'test-{0}'.format(str(randint(0, 10)))
            key = bytes(randint(1, 10))
            body = '{0}:{1}'.format(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f'), str(uuid.uuid4()))
            producer.send(topic, str.encode(body), key=key)
            time.sleep(producer_delay)

            counter += 1
            if counter % 500 == 0:
                logger.info('Sent %s messages.', str(counter))

    try:
        start_delay = float(os.getenv('START_DELAY', 1.0))
        producer_delay = float(os.getenv('PRODUCER_DELAY', 1.0))
    except:
        start_delay = 30
        producer_delay = 1.0
    logger.info('Producer delay: %s', producer_delay)

    # :(, make sure kafka cluster is ready brfore creating topics.
    # It's frustrated when docker-compose is difficult to control start order.
    logger.info('Wating for %s seconds...', start_delay)
    time.sleep(start_delay)

    create_test_topic()
    send_message()
