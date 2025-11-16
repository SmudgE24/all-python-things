import datetime as dt
import time as t

#dt.timedelta.total_seconds
#
#sound_file = '/home/pi/Downloads/mixkit-classic-alarm-995.wav'
#
#wave_obj = sa.WaveObject.from_wave_file(sound_file)
#play_obj = wave_obj.play()
#play_obj.wait_done()
n1 = 1
in_one = 0
in_one = input('1 = Christmas, 2 = Ethan, 3 = year-seven')
#in_one = input


def christmas():
    christmas = dt.datetime(2024, 12, 25, 7, 30, 0)
    now = dt.datetime.now()
    diff = dt.timedelta.total_seconds(christmas - now)
    
    while diff>0:
        now = dt.datetime.now()
        diff = dt.timedelta.total_seconds(christmas - now)
        print (round(diff, 1),' seconds "til Christmas')
        #t.sleep(0.1)
        #play_obj = wave_obj.play()
        
    if diff == 0:
        print ('IT"S CHRISTMAS!!!!!!!!!!')
        while n1 == 1:
            print ('IT"S CHRISTMAS!!!!!!!!!!')

def ethanbirthday():
    ethan = dt.datetime(2024, 3, 24, 7, 30, 0)
    now = dt.datetime.now()
    diff = dt.timedelta.total_seconds(ethan - now)
        
    while diff>0:
        now = dt.datetime.now()
        diff = dt.timedelta.total_seconds(ethan - now)
        print (round(diff, 1),' seconds "til Ethans"s birthday')
        #t.sleep(0.01)
        #play_obj = wave_obj.play()
        
    if diff == 0:
        print ('IT"S ETHAN"S BIRTHDAY!!!!!!!!!!')
        while n1 == 1:
            print ('IT"S ETHAN"S BIRTHDAY!!!!!!!!!!')

def schoolstart():
    school = dt.datetime(2025, 9, 4, 8, 0, 0)
    now = dt.datetime.now()
    diff = dt.timedelta.total_seconds(school - now)
        
    while diff>0:
        now = dt.datetime.now()
        diff = dt.timedelta.total_seconds(school - now)
        rounded_diff = round(diff, 1)
        print (rounded_diff,' seconds "til school starts")
        #t.sleep(0.1)
        #play_obj = wave_obj.play()
        
    if diff == 0:
        print ('IT"S SCHOOL NOW!!!!!!!!!!')
        while n1 == 1:
            print ('IT"S SCHOOL NOW!!!!!!!!!!')

if (int(in_one)) == 1:
    christmas()
if (int(in_one)) == 2:
    ethanbirthday()
if (int(in_one)) == 3:
    schoolstart()


#mixkit-classic-alarm-995.wav
#/home/pi/Downloads
    
    
    



print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
print ('')
