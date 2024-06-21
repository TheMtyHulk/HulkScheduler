import sys, getopt
from scheduler import scheduler
def main(argv):
   # default algorithm:
   workers = 1
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
   scheduler()
   
if __name__ == "__main__":
   main(sys.argv[1:])

