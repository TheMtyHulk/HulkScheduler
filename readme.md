# optimized task scheduler using PSO-MCT algorithm



To Run This Scheduling System
```
git clone https://github.com/TheMtyHulk/HulkScheduler.git

```
in your terminal 

```
cd HulkScheduler 

```

```
pip install -r requirements.txt
```

create a .env file in the workspace
```
MONGO_URL=your MongoDB URL
```

create a folder named "worker_files"
```
mkdir worker_files
```

to run this 
in your terminal

```
py init.py -w 5
```
here the number 5 determines the number of workers

after it starts you can see worker files in worker_files 
