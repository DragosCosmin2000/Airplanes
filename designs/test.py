'''import os, sys
import threading
import time
class myThread(threading.Thread):
   def __init__(self, name, duration):
        threading.Thread.__init__(self)
        self.duration = duration
        self.name = name

   def run(self):
        i = 0
        while True:
            time.sleep(1)
            if i == self.duration:
                break
            i += 1

        print(self.name, "ready")

t1 = myThread("t1", 10)
t2 = myThread("t2", 5)
t3 = myThread("t3", 10)

t1.start()
t2.start()
t3.start()
print("something between")
t1.join()
t2.join()
t3.join()
print("main ready")'''

class chestii(object):
    def __init__(self):
        self.val = 3

class fct(object):
    def __init__(self, obj):
        self.obj = obj
    def run(self):
        self.obj.val = 1

ch = chestii()
fct1 = fct(ch)
#fct1.run()

print(ch.val)





