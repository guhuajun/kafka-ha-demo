# -*- coding: utf-8 -*-
# pylint: disable=


import os
import logging
import time
import uuid
from datetime import datetime

import kafka
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "172.25.0.21:9094")

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
        
    def consume_message():
        consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS, group_id='test')
        consumer.subscribe(topics=('test',))

        counter = 0
        for msg in consumer:
            counter += 1
            if counter % 500 == 0:
                consumer.commit()
                logger.info('Consumer metrics: %s.', str(consumer.metrics()))
                logger.info(msg)

    consume_message()
