

def monthdayyear(string):
    #check if the format of the inputted string matches dd.mm.yyyy if it does return the string otherwise return false
    
    if len(string.split(".")) != 3:
        return False
    if not string.split(".")[0].isdigit() or not string.split(".")[1].isdigit() or not string.split(".")[2].isdigit():
        return False
    if 1 <= int(string.split(".")[0]) <= 31 and 1 <= int(string.split(".")[1]) <= 12 and 1 <= int(string.split(".")[2]):
        return string
    
def hourminute(string):
    #check if the format of the inputted string matches hh:mm if it does return the string otherwise return false
    
    if len(string.split(".")) != 2:
        return False
    if not string.split(".")[0].isdigit() or not string.split(".")[1].isdigit():
        return False
    if 0 <= int(string.split(".")[0]) <= 23 and 0 <= int(string.split(".")[1]) <= 59:
        return string
    
def yesno(string):
    #check if the format of the inputted string matches y/n if it does return the string otherwise return false
    
    if string.lower() == "y" or string.lower() == "n":
        return string
    if string.lower() == "yes" or string.lower() == "no":
        if string.lower() == "yes":
            return "y"
        else:
            return "n"
    else:
        return False
    
def day(string):
    #check if the format of the inputted string matches daily,mon,tue,wed,thu,fri,sat,sun if it does return the string otherwise return false
    
    if string.lower() == "daily" or string.lower() == "mon" or string.lower() == "tue" or string.lower() == "wed" or string.lower() == "thu" or string.lower() == "fri" or string.lower() == "sat" or string.lower() == "sun":
        return string
    if string.lower() == "monday":
        return "mon"
    if string.lower() == "tuesday":
        return "tue"
    if string.lower() == "wednesday":
        return "wed"
    if string.lower() == "thursday":
        return "thu"
    if string.lower() == "friday":
        return "fri"
    if string.lower() == "saturday":
        return "sat"
    if string.lower() == "sunday":
        return "sun"
    else:
        return False