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
        producer_delay = float(os.getenv('CONSUMER_DELAY', 1.0))
    except:                                                     
        producer_delay = 1.0                                    
    logger.info('Consumer delay: %s', producer_delay)

    bootstrap_servers = ["kafka1:19092", "kafka2:29092", "kafka3:39092"]
    
    def consume_message():
        topics = tuple('test-{0}'.format(str(x)) for x in range(0, 10))
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id='test')
        consumer.subscribe(topics=topics)

        counter = 0
        for msg in consumer:
            counter += 1
            if counter % 500 == 0:
                consumer.commit()
                # logger.info('Consumer metrics: %s.', str(consumer.metrics()))
                logger.info(msg)

    consume_message()
