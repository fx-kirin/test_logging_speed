#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 fx-kirin <fx.kirin@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import datetime
import logging
import queue
import sys
import time
from logging.handlers import QueueHandler, QueueListener
from nalog import Logger

from benchmarker import Benchmarker

if __name__ == '__main__':
    log_queue = queue.Queue(-1)
    test_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)

    logger = logging.getLogger()

    #console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(threadName)s: %(message)s')
    #console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("queue_example.log")
    file_handler.setFormatter(formatter)

    listener = QueueListener(log_queue, file_handler)

    with Benchmarker(10000, width=40) as bench:
        @bench("queue logger")
        def _(bm):
            logger.addHandler(queue_handler)
            for i in bm:
                logger.warning('Look out!')
            logger.handlers = []

        @bench("default logger")
        def _(bm):
            logger.addHandler(file_handler)
            for i in bm:
                logger.warning('Look out!')
            logger.handlers = []

        @bench("only queuing")
        def _(bm):
            for i in bm:
                sys.exc_info()
                time.time()
                test_queue.put('Look out!')

        @bench("nalog")
        def _(bm):
            log = Logger(__name__, level="debug")
            for i in bm:
                log.info("Hello!")

    listener.start()

    listener.stop()
