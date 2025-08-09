# -*- coding: utf-8 -*-
# pylint: disable=


import os
import logging
import time
import uuid
from datetime import datetime
from random import randint

import kafka
from kafka import KafkaConsumer


if __name__ == "__main__":
    # change logging config
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s.%(msecs)03d][%(filename)s:%(lineno)d][%(levelname)s]%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__file__)

    try:
        start_delay = float(os.getenv('START_DELAY', 1.0))
        consumer_delay = float(os.getenv('CONSUMER_DELAY', 1.0))
    except:
        start_delay = 30
        consumer_delay = 1.0
    logger.info('Consumer delay: %s', consumer_delay)

    bootstrap_servers = ["kafka1:19092", "kafka2:29092", "kafka3:39092"]

    # :(, make sure kafka cluster is ready before creating topics.
    # It's frustrated when docker-compose is difficult to control start order.
    logger.info('Wating for %s seconds...', start_delay)
    time.sleep(start_delay)

    def consume_message():
        topics = tuple('test-{0}'.format(str(x)) for x in range(1, 6))
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id='test')
        consumer.subscribe(topics=topics)

        counter = 0
        for msg in consumer:
            counter += 1
            if counter % 500 == 0:
                consumer.commit()
                logger.info(msg)

    consume_message()
