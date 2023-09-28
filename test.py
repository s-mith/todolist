#python command line task keeper

import sys
from assignments import Assignment
from assignments import repeatAssignment
from time import sleep
import time
import json
import threading
import uuid

from inputvalidation import *





class App:

    def __init__(self):
        self.pendingassignments = []
        self.currentAssignment = {}
        self.completedassignments = []
        self.repeatassignments = []
        self.paused = False
        self.idlist = []


    def getidlist(self, filename):
        #get the id list from the json file and return it as a list
        with open(filename, 'r') as f:
            raw = f.read()

        #convert the json to a list of strings
        unpackedids = json.loads(raw)
        tempids = []
        for id in unpackedids:
            tempids.append(id)
        return tempids


    def getAssignments(self, filename):
        #get the assignments from thes json file and return them as a list
        with open(filename, 'r') as f:
            raw = f.read()

        #convert the json to a list of assignment objects
        unpackedassignments = json.loads(raw)
        tempassignments = []
        for assignment in unpackedassignments:
            tempassignments.append(Assignment(int(assignment['assign']), int(assignment['due']), assignment['title'], assignment['description'], assignment['uuid'], assignment['completed']))
        return tempassignments
    
    def getAssignmentsKeys(self, filename):
        #get the assignments from thes json file and return them as a list
        with open(filename, 'r') as f:
            raw = f.read()

        #convert the json to a list of assignment objects
        unpackedassignments = json.loads(raw)
        tempassignments = {}
        
        for assignment in unpackedassignments:
            tempassignments[assignment] = Assignment(int(unpackedassignments[assignment]['assign']), int(unpackedassignments[assignment]['due']), unpackedassignments[assignment]['title'], unpackedassignments[assignment]['description'], unpackedassignments[assignment]['uuid'], unpackedassignments[assignment]['completed'])
        return tempassignments
    
    def getRepeatAssignments(self, filename):
        with open(filename, 'r') as f:
            raw = f.read()

        #convert the json to a list of repeatassignment objects
        unpackedassignments = json.loads(raw)
        tempassignments = []
        for assignment in unpackedassignments:
            tempassignments.append(repeatAssignment(assignment['assign'], assignment['due'], assignment['title'], assignment['description'], assignment['uuid'], assignment['repeat'], assignment['hasrepeated']))
        return tempassignments
    

    def updateAssignments(self, filename, assignments):
        #update the json file with the list of assignments
        #convert the list of assignments to a list of dictionaries
        tempassignments = []
        for assignment in assignments:
            tempassignments.append(assignment.__dict__)
            
        #convert the list of dictionaries to a json string

        packedassignments = json.dumps(tempassignments)

        #write the json string to the file
        with open(filename, 'w') as f:
            f.write(packedassignments)

    def updateAssignmentsKeys(self, filename, assignments):
        #update the json file with the list of assignments
        #convert the list of assignments to a list of dictionaries
        tempassignments = {}
        for assignment in assignments:
            tempassignments[assignment] = assignments[assignment].__dict__
        #convert the list of dictionaries to a json string
        packedassignments = json.dumps(tempassignments)
        #write the json string to the file
        with open(filename, 'w') as f:
            f.write(packedassignments)

    def updateidlist(self, filename, ids):
        #save the list of strings to the json file
        packedids = json.dumps(ids)
        with open(filename, 'w') as f:
            f.write(packedids)

        


    

    

    def assignmentUpdateThread(self):
        #every minute update the list of current assignments and then if any are pass the assign date move them to the current assignment list and then print them
        while True:
            if not self.paused:
                print('\n'*100)
            #update the list of assignments
            self.pendingassignments = self.getAssignments('assignments.json')
            self.completedassignments = self.getAssignments('completed.json')
            self.currentAssignment = self.getAssignmentsKeys('inprogress.json')
            self.repeatassignments = self.getRepeatAssignments('repeat.json')
            self.idlist = self.getidlist('idlist.json')
            
            #check if any are past the the assignment date
            for objec in self.pendingassignments:
                if objec.assign < time.time():
                    
                    #move the assignment to the current assignment list
                    id = self.idlist.pop(0)
                    self.currentAssignment[id] = objec
                    #remove the assignment from the pending assignment list
                    self.pendingassignments.remove(objec)
            for objec in self.repeatassignments:
                # get the calendar day of the week
                
                #check if the assignment has repeated today
                if not objec.didToday():
                    
                    if objec.dotoday():
                        
                        if objec.dinamicAssign() < time.time():
                            
                            #move the assignment to the current assignment list
                            id = self.idlist.pop(0)
                            self.currentAssignment[id] = Assignment(objec.dinamicAssign(), objec.dinamicDue(), objec.title, objec.description)
                            objec.do()

            
            #update the json files
            if not self.paused:
                for key in self.currentAssignment:
                    print(key+":")
                    print(self.currentAssignment[key])
                print("Enter a command (add, complete, exit): ")

            self.updateAssignments('assignments.json', self.pendingassignments)
            self.updateAssignments('completed.json', self.completedassignments)
            self.updateAssignmentsKeys('inprogress.json', self.currentAssignment)
            self.updateAssignments('repeat.json', self.repeatassignments)
            self.updateidlist('idlist.json', self.idlist)
            sleep(5)
            

    def listme(self):
        #list the current assignments
        for key in self.currentAssignment:
            print(key+":")
            print(self.currentAssignment[key])

    def addTask(self):
        #get the user input for the assignment and add it to the list of pending assignments
        #get the user input for the assignment
        userinput = input("Is this a repeat assignment? (y/n): ")

        if userinput == 'n':
            assign = input("Enter the date for the assignment in the format dd.mm.yyyy: ")
            if assign == 'now':
                assign = int(time.time())
                due = int(time.time())

            else:
                if not monthdayyear(assign):
                    print("Invalid date")
                    return
                assign2 = input("Enter the time for the assignment in the format hh.mm: ")
                if not hourminute(assign2):
                    print("Invalid time")
                    return
            
                #convert the date to unix time
                assign = time.mktime(time.strptime(assign+' '+assign2 , '%d.%m.%Y %H.%M'))

                due = input("Enter the date for the turn in date in the format dd.mm.yyyy: ")
                if not monthdayyear(due):
                    print("Invalid date")
                    return
                due2 = input("Enter the time for the turn in date in the format hh.mm: ")
                if not hourminute(due2):
                    print("Invalid time")
                    return
                #convert the date to unix time
                due = time.mktime(time.strptime(due+' '+due2, '%d.%m.%Y %H.%M'))


            title = input("Enter the title for the assignment: ")



            description = input("Enter the description for the assignment: ")
            #add the assignment to assignments.json
            temp = self.pendingassignments
            temp.append(Assignment(assign, due, title, description))
            self.updateAssignments('assignments.json', temp)
        elif userinput == 'y':
            repeat = input("what is the repeat schedule? (daily, mon, tue, wed, thu, fri, sat, sun): ")
            if not day(repeat):
                print("Invalid repeat schedule")
                return
            assign = input("Enter the time for the assignment in the format hh.mm: ")
            if not hourminute(assign):
                print("Invalid time")
                return
            due = input("Enter the time for the turn in date in the format hh.mm: ")
            if not hourminute(due):
                print("Invalid time")
                return
            title = input("Enter the title for the assignment: ")
            description = input("Enter the description for the assignment: ")
            #add the assignment to assignments.json
            temp = self.repeatassignments
            temp.append(repeatAssignment(assign, due, title, description, str(uuid.uuid4()), repeat, []))
            self.updateAssignments('repeat.json', temp)

            

        
    def completeTask(self):
        #complete a task
        #get the user input for the task to complete
        
        userinput = input("Enter the id of the assignment you want to complete: ")
        #find the assignment in the list of current assignments
        if userinput in self.currentAssignment:
            #move the assignment to the completed assignments list
            temp = self.completedassignments
            temp.append(self.currentAssignment[userinput])
            self.updateAssignments('completed.json', temp)
            #remove the assignment from the current assignments list
            temp = self.currentAssignment
            temp.pop(userinput)
            self.updateAssignmentsKeys('inprogress.json', temp)
            #add the id back to the id list
            self.idlist.append(userinput)
            self.updateidlist('idlist.json', self.idlist)




    def userInputThread(self):
        #wait and detect user input for adding tasks, listing tasks and completing tasks
        while True:
            #sleep(1)
            #detect user input
            userinput = input("Enter a command (add, complete, exit): ")
            if userinput == 'add':
                #add a new task
                self.paused = True
                self.addTask()
                self.listme()
                self.paused = False
            elif userinput == 'complete':
                #complete a task
                self.paused = True
                self.completeTask()
                self.listme()
                self.paused = False
            elif userinput == 'exit':
                #exit the program
                sys.exit()
            else:
                print("Invalid command")
    

    def run(self):
        #start the assignment update thread
        assignmentupdatethread = threading.Thread(target=self.assignmentUpdateThread)
        assignmentupdatethread.start()
        #start the user input thread
        userinputthread = threading.Thread(target=self.userInputThread)
        userinputthread.start()
        #wait for the threads to finish
        assignmentupdatethread.join()
        userinputthread.join()


if __name__ == '__main__':
    app = App()
    app.run()