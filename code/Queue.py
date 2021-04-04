import sys


class Queue:
    def __init__(self):
        self.queue = []
    
    
    def enqueue(self, elementToEnqueue):
        self.queue.append(elementToEnqueue)
    

    def dequeue(self):
        if self.isEmpty():
            sys.exit("Error: Cannot dequeue from empty queue")
        else:
            return self.queue.pop(0)
    

    def isEmpty(self):
        return (len(self.queue) == 0)
    

    def getSize(self):
        return len(self.queue)


    def printQueue(self):
        if self.isEmpty():
            print("Queue is empty.")
        else:
            print("Queue:", self.queue)

