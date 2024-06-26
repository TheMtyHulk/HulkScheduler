# optimized task scheduler using PSO-MCT alorithm



to run this 
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
create a .env file in the workspace in the .env file
```
MONGO_URL=your mongdb url
```

create a folder named "worker_files"

to run this 
in your terminal

```
py init.py -w 5
```
here the number 5 determines number of workers

after it starts you can see worker files in worker_files