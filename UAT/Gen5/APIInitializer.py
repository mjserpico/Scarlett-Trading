#IBAPi default libraries
from ib.ext.Contract import Contract
from ib.ext.EWrapper import EWrapper
from ib.ext.EClientSocket import EClientSocket
from ib.ext.EReader import EReader
from ib.opt import Connection

#Default Python Libraries
from threading import Thread
import queue
import mysql.connector
from datetime import timedelta
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import os
import csv

#Scarlett Trading Libraries
import datalink   #universal login

"""
https://stackoverflow.com/questions/419163/what-does-if-name-main-do
"""



class Wrapper(EWrapper):
    """
    The wrapper deals with the action coming back from the IB gateway or TWS instance
    We override methods in EWrapper that will get called when this action happens, like currentTime
    """

    ## error handling code
    def init_error(self):
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None


    def is_error(self):
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    ## Time telling code
    def init_time(self):
        time_queue=queue.Queue()
        self._time_queue = time_queue

        return time_queue

    def currentTime(self, time_from_server):
        ## Overriden method
        self._time_queue.put(time_from_server)


class Client(EClientSocket):
    """
    _init__ is a special Python method that is automatically called 
    when memory is allocated for a new object. The sole purpose of __init__ is 
    to initialize the values of instance members for the new object
    """
    def __init__(self, wrapper):
        ## Set up with a wrapper inside
        EClientSocket.__init__(self, wrapper)

    def speaking_clock(self):
        """
        Basic example to tell the time
        :return: unix time, as an int
        """

        print("Getting the time from the server... ")

        ## Make a place to store the time we're going to return
        ## This is a queue
        time_storage=self.wrapper.init_time()

        ## This is the native method in EClient, asks the server to send us the time please
        self.reqCurrentTime()

        ## Try and get a valid time
        MAX_WAIT_SECONDS = 10

        try:
            current_time = time_storage.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            current_time = None

        while self.wrapper.is_error():
            print(self.get_error())

        return current_time
    
    def account_summary(self):
        print("Getting Account Summary server... ")

        ## Make a place to store the time we're going to return
        ## This is a queue
        account_storage=self.wrapper.init_time()

        ## This is the native method in EClient, asks the server to send us the time please
        self.reqCurrentTime()

        ## Try and get a valid time
        MAX_WAIT_SECONDS = 10

        try:
            current_time = time_storage.get(timeout=MAX_WAIT_SECONDS)
        except queue.Empty:
            print("Exceeded maximum wait for wrapper to respond")
            current_time = None

        while self.wrapper.is_error():
            print(self.get_error())

        return current_time

class App(Wrapper, Client):
    def __init__(self, ipaddress, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)

        self.init_error()

if __name__ == '__main__':
    ##
    ## Check that the port is the same as on the Gateway
    ## ipaddress is 127.0.0.1 if one same machine, clientid is arbitrary

    app = App("127.0.0.1", 4002, 10)
    
    current_time = app.speaking_clock()

    print(current_time)

    app.disconnect()
