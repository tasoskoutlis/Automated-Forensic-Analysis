#!/usr/bin/env python
import os

'''
Extract All User Information
'''
def extractNTUSER(users):
    
    for n in range(1, users + 1):
        
        os.system('python regparse.py --plugin userassist --hives files/NTUSER' + str(n) + '.DAT --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > csv/userassist' + str(n) + '.csv')

        os.system('python regparse.py --plugin runmru --hives files/NTUSER' + str(n) + '.DAT --format "{{ last_write }}|{{ key }}|{{ mruorder }}|{{ value }}|{{ data }}" > csv/mru' + str(n) + '.csv')

        os.system('python regparse.py --plugin recentdocs --hives files/NTUSER' + str(n) + '.DAT --format "{{last_write}}|{{key_name}}|{{key}}|{{value}}|{{data}}" > csv/recent' + str(n) + '.csv')

        os.system('python regparse.py --plugin lastvisitedmru --hives files/NTUSER' + str(n) + '.DAT > csv/lastvisitedmru' + str(n) + '.csv')


'''
Extract System information
'''
os.system('python regparse.py --plugin sysinfo --hives files/SYSTEM files/SOFTWARE --format "{{ last_write }}|{{ os_info }}|{{ installed_date }}|{{ registered_owner }}" > csv/sysinfo.csv')

os.system('python regparse.py --plugin services --hives files/SYSTEM --format "{{ last_write }}|{{ key_name }}|{{ image_path }}|{{ type_name }}|{{ display_name }}|{{ start_type }}|{{ service_dll }}" > csv/services.csv')

os.system('python regparse.py --plugin usbstor --hives files/SYSTEM --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > csv/usb.csv')



def main(): 
        
    users = 2
    
    extractNTUSER(users)


if __name__ == "__main__":
    main()