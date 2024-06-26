import sys, getopt
import scheduler 

def main(argv):
   # default algorithm:
   workers = 3
   try:
      opts, args = getopt.getopt(argv,"w:",["workers="])
   except getopt.GetoptError:
      print("init.py -w <workers>")
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-w", "--workers"):
         # use alternative workes value if provided:
         workers = arg
   print ("Using no of workers: ", workers)
   
   #calling the scheduler class constructor
   s=scheduler.scheduler()
   s.schedule("tasks")
   
   import coordinator
   coordinator.Coordinator(int(workers))
   
if __name__ == "__main__":
   main(sys.argv[1:])

