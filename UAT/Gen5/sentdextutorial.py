# -*- coding: utf-8 -*-
"""
Created on Sun May  5 12:31:04 2019

@author: Michael
"""
import threading
from queue import Queue
import time

print_lock = threading.Lock()

def exampleJob(worker):  #pass worker to job
    time.sleep(0.5)
    
    with print_lock:
        print(threading.current_thread().name, worker)

def threader():
    while True:# Continues to run until Main thread dies (see Daemon)
        worker = q.get()
        exampleJob(worker)
        q.task_done()
        
        #Queue Job assignmnet
q = Queue()

for x in range(10): #Allows 10 threads
    t = threading.Thread(target = threader)
    t.daemon = True   #classify thread as daemon so it dies when main thread dies
    t.start() #starts the threading
    
start = time.time()
for worker in range(20):
    q.put(worker)  #sends worker to queue
    
q.join()

print('Entire job took:', time.time() - start())



