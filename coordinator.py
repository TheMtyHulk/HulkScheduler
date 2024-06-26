from  pymongo import MongoClient
import os
import threading
from worker import WorkerThread
from pso_algo import Task_Assignment_Calc
from datetime import datetime

class Coordinator:
    def __init__(self,num_workers) -> None:
        
        self.num_workers = num_workers
        self.stop_event = threading.Event()
        
        self.workers = []
        freeworkers = set()
        
        client = MongoClient(os.getenv('MONGO_URL'))
        self.db = client['taskmaster']
        self.tasks=self.db['tasks']
        
        # creating worker threads
        for i in range(num_workers):
            worker = WorkerThread(i)
            self.workers.append(worker)
            worker.start()
        
        # for worker in self.workers:
        #     worker.join().
            
        while True:
            self.checkTask()
    
    def checkTask(self):
        db = self.db
        tasks = db['tasks']
        undone_tasks=[]
        
        # check for available task and append to task_id to list
        
        for task in tasks.find({"picked_at": None}):
            undone_tasks.append(task.get('_id'))   
        
        if undone_tasks:
            self.assign_task(undone_tasks)
        pass
    
    def assign_task(self,undone_tasks:list):
        db = self.db
        # creating db for available tasks
        assigned_tasks = db['assigned_tasks']
        
        t=Task_Assignment_Calc(self.num_workers,undone_tasks)
        dist= t.get_distribution()
        # print(dist)
        # print(len(dist))
    
        for ud in undone_tasks:
            assigned_tasks.insert_one({'_id':ud,'worker_id':dist[ud]})
            self.tasks.update_one({'_id':ud},{'$set':{'picked_at':datetime.now()}})   
        

        # this is for testing purpose only
            
        
        
        

# this is for testing
# co=Coordinator(5)