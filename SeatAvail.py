#Course seat Availabilty Notification
from bs4 import BeautifulSoup
from lxml import html
import requests

textfilepath='SeatAvail/coursefile.txt'

def notify_user(available_courses):
    ecampus_link='https://ecampus.scu.edu'
    message = 'Courses available!:\n'+'\n\n'.join(available_courses)+'\nGet on it! '+ecampus_link
    send_message_to_slack(message)

def send_message_to_slack(message):
    import requests
    import json
    post = {"text": message}
    try:
        #web_hook= Insert slack webhook here
        requests.post(web_hook,data=json.dumps(post))
    except Exception as em:
        print("EXCEPTION: " + str(em))

def get_all_courses(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    req = requests.get(url,headers=agent)
    page = BeautifulSoup(req.text, "html.parser")
    table_rows = page.find("table",{"id":"zebra"}).findAll("tr")
    #print(table_rows)
    all_courses=[]
    for row in table_rows[1:-1]:
        temp = row.text
        temp=' '.join(temp.split())+' Seat(s)'
        all_courses.append(temp)
    return all_courses

def get_my_courses():
    lines = [line.rstrip('\n') for line in open(textfilepath)]
    return lines

def main():
    #Term number 4020 in Winter 2019, increments by 20 each regular quarter and 40 in summer. Who knows why
    given_courses = get_my_courses()
    print(given_courses)
    current_term=4020
    classes_url='https://legacy.scu.edu/courseavail/search/index.cfm?fuseAction=search&StartRow=1&EndRow=31&MaxRow=10000&term=%d&acad_career=all&school=&subject=&catalog_num=&instructor_name1=&days1=&start_time1=6&start_time2=&available=yes&header=no&footer=no'%current_term
    available_courses = get_all_courses(classes_url)
    #Find matches
    matches=[]
    for course in given_courses:
        for a in available_courses:
            a=a.replace(',',' ')
            if course.upper() in a.upper():
                matches.append(a)

    if len(matches)!=0:
        notify_user(matches)


if __name__== "__main__":
    main()