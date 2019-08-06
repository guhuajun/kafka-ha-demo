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

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "172.25.0.21:9092")

if __name__ == "__main__":
    # change logging config
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s.%(msecs)03d][%(filename)s:%(lineno)d][%(levelname)s]%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__file__)

    try:
        producer_delay = float(os.getenv('PRODUCER_DELAY', 1.0))
    except:
        producer_delay = 1.0
    logger.info('Producer delay: %s', producer_delay)

    def create_test_topic():
        client_id = 'producer-{0}'.format(str(uuid.uuid4()))
        admin_client = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVERS, client_id=client_id)

        topic_list = [NewTopic(name="test-{0}".format(str(x)),
                               num_partitions=1, replication_factor=1) for x in range(0, 10)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

    def send_message():
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        counter = 0
        while True:
            topic = 'test-{0}'.format(str(randint(0, 10)))
            body = '{0}:{1}'.format(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f'), str(uuid.uuid4()))
            producer.send(topic, str.encode(body))
            time.sleep(producer_delay)

            counter += 1
            if counter % 500 == 0:
                logger.info('Sent %s messages.', str(counter))

    try:
        create_test_topic()
    except Exception:
        pass

    send_message()
