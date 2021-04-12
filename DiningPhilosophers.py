from threading import Thread, Lock
import random
import time

numberOfPhilosophers = 5    # How many locks will be
runningTime = 10            # Time in seconds
printSwap = False           # True - print in console every lock swap

class Philosopher(Thread):
    isRunning = True

    def __init__(self,nr,left,right):
        self.nr = nr
        self.left = left
        self.right = right
        super().__init__()

    def run(self):
        while(self.isRunning):
            time.sleep(random.uniform(1,5)) # Random break
            print("Philosopher #{} is hungry".format(self.nr))
            self.eat()
    
    def eat(self):
        isSwapped  = False # Which fork is selected first; False - left, True - right
        fork_1, fork_2 = self.left, self.right
        while True:
            isLocked_fork_1 = fork_1.acquire(True,timeout=random.uniform(1,3)) 
            if isLocked_fork_1 == True:
                if printSwap:
                    if isSwapped == False:
                        print("Philosopher #{} picks up left fork".format(self.nr))
                    else:
                        print("Philosopher #{} picks up right fork".format(self.nr))

                isLocked_fork_2 = fork_2.acquire(False) # If philosopher can't pick up fork returns False, else True and locks

                if printSwap:
                    if isLocked_fork_2:
                        if isSwapped == False:
                            print("Philosopher #{} picks up right fork".format(self.nr))
                        else:
                            print("Philosopher #{} picks up left fork".format(self.nr))
                break
                fork_1.release() # If philosopher can't pick up second fork, he puts down first one and releases the lock
                if printSwap:
                    if isSwapped == False:
                        print("Philosopher #{} puts left fork down".format(self.nr))
                    else:
                        print("Philosopher #{} puts right fork down".format(self.nr))

            if printSwap:
                print("Philosopher #{} swaps forks".format(self.nr))
            fork_1, fork_2 = fork_2, fork_1 # Swap the order of picking up forks
            isSwapped = not isSwapped
        
        self.eating()
        try:
            fork_1.release()
            fork_2.release()
        except RuntimeError:
            pass

    def eating(self):
        print("Philosopher #{} starts eating".format(self.nr))
        time.sleep(random.uniform(3,5))
        print("Philosopher #{} ends eating".format(self.nr))
    
def run():
    if int(numberOfPhilosophers) < 2:
        exit()
    forks = [Lock() for i in range(numberOfPhilosophers)]

    philosophers = [Philosopher(i,forks[(i)%numberOfPhilosophers],forks[(i+1)%numberOfPhilosophers]) for i in range(numberOfPhilosophers)]

    Philosopher.isRunning = True

    for f in philosophers:
        f.start()

    time.sleep(runningTime)
    Philosopher.isRunning = False

run()

