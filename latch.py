'''
import.io client library - latch class

This file contains a latch class, which is used in the example code file

As the import.io client library is asynchronous, if you are writing a small
python script or are dependent on waiting for results before continuing your
code, the latch class will help you to "synchronise" your Python code around
the client library

First, construct a latch object with the number of queries you are waiting for
as the argument, in this example we are waiting for 5 queries:
    queryLatch = latch(5)

Then, issue your queries. In the callback, make sure you "countdown" the latch,
to let it know that the query has finished, like this:
    queryLatch.countdown()

Finally, once you have issued your queries (called importio.query()) then you can
"await" on the latch. This has the effect of holding your python code until the
queries have all finished:
    queryLatch.await()

Dependencies: Python 2.7

@author: dev@import.io
@source: https://github.com/import-io/importio-client-libs/tree/master/python
'''

import threading

class latch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def countdown(self):
        with self.lock:
            self.count -= 1

            if self.count <= 0:
                self.lock.notifyAll()

    def await(self):
        with self.lock:
            while self.count > 0:
                self.lock.wait()