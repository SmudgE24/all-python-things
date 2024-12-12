import datetime

now = datetime.datetime.now
dt = datetime.datetime.minute
now = now()

timeLeft = dt(year = 2023, month = 12, day = 25, hour = 8, minute = 0) - dt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)

print (timeLeft.minute)
print ('Hello this is your local christmas countdown there is', timeLeft.minute) 
