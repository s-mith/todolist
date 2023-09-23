
import uuid
import time
class Assignment:

    def __init__(self, assign, due, title, description, uuid=uuid.uuid4 , completed = False):
        self.uuid = uuid
        self.assign = assign
        self.due = due
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        #convert the due unix time to a readable date
        import time
        readable = time.strftime('%m/%d/%Y', time.localtime(self.due))
        clock = time.strftime('%H:%M:%S', time.localtime(self.due))
        ampm = time.strftime('%p', time.localtime(self.due))
        return f"{self.title} id:{self.uuid} \nDue: {readable} {clock}{ampm} \t Description: {self.description}\n"


class repeatAssignment(Assignment):
    #this is a class for an assignment that repeats every week or every day
    def __init__(self, assign, due, title, description, uuid=uuid.uuid4, completed = False, repeat = 'null', hasrepeated = []):
        super().__init__(assign, due, title, description, uuid, completed)
        self.repeat = repeat
        self.hasrepeated = hasrepeated

    def didToday(self):
        #check if the assignment has repeated today
        import time
        #get dd.mm.yyyy
        day = time.strftime('%d.%m.%Y', time.localtime(time.time()))
        #check if that day is in self.hasrepeated
        if day not in self.hasrepeated:
            return False
        else:
            return True
        
    def dinamicAssign(self):
        # assign is a 24 hour time convert it to unix using today's date
        import time
        #get dd.mm.yyyy
        day = time.strftime('%d.%m.%Y', time.localtime(time.time()))
        #convert the date to unix time
        assign = time.mktime(time.strptime(day, '%d.%m.%Y')+time.strptime(self.assign, '%H.%M'))
        
        return assign
    
    def dinamicDue(self):
        # due is a 24 hour time convert it to unix using today's date
        import time
        #get dd.mm.yyyy
        day = time.strftime('%d.%m.%Y', time.localtime(time.time()))
        #convert the date to unix time
        due = time.mktime(time.strptime(day, '%d.%m.%Y')+time.strptime(self.due, '%H.%M'))
        
        return due

        
    def dotoday(self):
        if self.repeat == "null":
            return False
        elif self.repeat == "daily":
            return True
        elif self.repeat == "mon":
            # check if today is monday
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Mon":
                return True
            else:
                return False
        elif self.repeat == "tue":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Tue":
                return True
            else:
                return False
        elif self.repeat == "wed":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Wed":
                return True
            else:
                return False
        elif self.repeat == "thu":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Thu":
                return True
            else:
                return False
        elif self.repeat == "fri":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Fri":
                return True
            else:
                return False
        elif self.repeat == "sat":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Sat":
                return True
            else:
                return False
        elif self.repeat == "sun":
            day = time.strftime('%a', time.localtime(time.time()))
            if day == "Sun":
                return True
            else:
                return False
        else:
            return False
        
    def do(self):
        # add the current day to the list of days the assignment has repeated
        day = time.strftime('%d.%m.%Y', time.localtime(time.time()))
        self.hasrepeated.append(day)