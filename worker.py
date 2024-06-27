import threading
from pymongo import MongoClient
import os
# import gridfs
from datetime import datetime
import time
from compress import CompressPDF

class WorkerThread(threading.Thread):
    
    def __init__(self, worker_id):
        super().__init__()
        
        # do db connection
        client = MongoClient(os.getenv('MONGO_URL'))
        self.db = client['taskmaster']
        self.assigned_tasks = self.db['assigned_tasks']
        
        self.worker_id = worker_id
        self.is_Free = True
        
    
    def run(self):
        # db=self.db
        mytask=[]     
        while True:
            if self.is_Free:
                print(f"Worker {self.worker_id} is free")
                for at in self.assigned_tasks.find({'worker_id':self.worker_id}):
                    mytask.append(at.get('_id'))    
                
                if mytask:    
                    self.is_Free = False
                    self.do_task(mytask)
                    self.assigned_tasks.delete_many({'worker_id':self.worker_id})
                    mytask.clear()
                
                self.is_Free = True
                    
                
                # self.is_Free = False
            else:
                print(f"Worker {self.worker_id} is busy")
                self.is_Free = True
            time.sleep(3)
    def do_task(self,mytask):
        db = self.db
        tasks=db['tasks']
        
        for task in mytask:
            tasks.update_one({'_id':task},{'$set':{'started_at':datetime.now()}})  
            
            print(f"Worker {self.worker_id} is doing task {task}")
            c=CompressPDF(task_id=task,worker_id=self.worker_id)
            c.compressPDF()
            
            
            tasks.update_one({'_id':task},{'$set':{'completed_at':datetime.now()}})  
            tasks.update_one({'_id':task},{'$set':{'completed_by':self.worker_id}})
        self.assigned_tasks.delete_many({'worker_id':self.worker_id})
        pass