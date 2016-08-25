import json
from icalendar import Calendar, Event, vText
from dateutil import parser as du_parser
from dateutil.tz import tzlocal
import datetime
import getpass
import requests
import re
import sys

headers = {
    'Origin': 'https://auth.berkeley.edu',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F',
    'Connection': 'keep-alive',
}

def calnet_login(username, password):
    data = 'username={}&password={}&lt=LT-43243-qXqlbY7XisQrGGoQ7ZrnVeERNMJsi0-cas-p3.calnet.berkeley.edu&execution=885ce9c6-4e8a-4a1a-884d-854621b6ff6e_AAAAIgAAABBb3%2Bicw31fIN%2FoVRx01ulqAAAABmFlczEyOACI9J04kS%2BJJ%2FTnfif7hVyulMnN9G9%2F2VQQZdn2SvDFrpwbbpRuSehyEbUYaCkkuw2kXjazhihVKLzR0krHPtY6YgYJ3gUtAU3%2Fvu9n2XmRA8FrCVqe%2BGzqkScNr4%2B6AZ9QjQ0tq8kBy03OaUdNkmRC%2Bs44uDCjdPieVogMVl%2BNtt2eibP16EiqTrzNSiHh%2Fy8NRp4BxRXhDlrghxTv3KWop9Z317h2FBIGEqrj4%2B7N0XqOe4a2uVB74Toj2%2FXSISYsStyWu1TPTI1ymTiWJBPQHzS0c7nIBfmp7SdL%2FEPd6C%2Bb1nG8Wvh%2FT98qVVQKF1RUaUmQJLW6bYQJIzpjiy3CJQNQHH%2F5waPAqR09yWALqQaq9aOOB6dj%2BO5z2wO%2BByRQ0cGawBJAO4wPTwxuxHKXJSwYnTS%2FRhGfIOdUAqaK5TuF0LoQz68CX1rR%2FlaDrk10tCGzMq%2Bo%2FKNDxcX%2Bz02DsArhxUTdG%2Bw%2Fz0u9O1WGo378yqr4GEHk%2BYPpYd0aqSjDGUFDdj1urPxN6jrUUIkX%2BQSCQqRbDfXi5kV10qFk5Tg3q2wTGsrr0ooKIVNOI5sd09KVPfS7UekN3KYhfB4DCetzdbqP7BGZg3PQa65p3NPMAHf78mA6sr0DpYSELIPWeP0QFne%2B8v5KYDjIXsjaPIyKyFJS09XRkYaPiWdnn9Avy4UpU7EVl7GRiRhQ%2BMDYDg4d67KcaQ7ZtO8OMomMjA6ehWMkciN3ao86BaOHVWr8hVK842LQe8QcabBVQP8UQlv1TuwCubPhdka7e3u%2BN8n%2By20kMqooMURx9tKuELy8R%2FXqpPcIOpDw1QSiny%2Bj7sDrEn%2BtTRUawpji7L6X9dBsIzLLj0N383%2FMi68sV4fk7I9CMtRvyrxHP7jQZIGeg%2F53LWZRmUxDUqnaUYlzzRCf3cG0xt6RGqSXWmFMs%2B%2B1kwpoRnpgWyC3I9sDZ39QLO6ExsdwCyq2SvnVzSknk%2FUrDXu0xCxY%2Fxhu57D7mBOMP53bXq9etsGEndYaOZkZSMaUF3i4l3Vyv8g6CXuawAZmxDnihqVXbjIp%2FiJDuVBTnqplgBzLet0LBvc82JKaUOOMtzHMxN9rKUeVKCKjU2PnXoNrcwyauMvEzVfceAExK7J77Sjp5RJ68AU%2F4P8e%2BYWGNeQBd%2FernlSroQbE%2B4IKiCN8N4dyhawYZsNDlYQcip62I0sXs2WgNum0EbWz7y027v%2F4nkza8JwqjWknwle6kZ2OqLH07e7uN8Exac4cmkBL1WAUEa%2BOfoeoHuMsEC7zr6v09zCsFD9CiT5j1tJtDvdV2bD5wJVWtw95bp%2F40VaucM4OCGKONmZS4VtfcUEVDwa5k1i2OrmBa1jduEdXI5RDwOPin95G5DD0AGe9zVCri6I%2FjEJpmo7Dnyen8BtXwf47Ut3RkMMEE6wO2EZkRaQXToFCEzIrEBKjzzXJLFbgeEzL6ugy0gisYqN1uNtzaDa59eAdaBfq919GkfxwiL%2F3JutLmF3JPbcuqbZ8bPlUgMXbffTVFvSTZCOjE14kYNowLTMfnyYjVgcg2gks1vAlsXmWXoM7YKJSHC63Ds5j8uk9VoATl7J2F1O8PvBo%2FT6sXjhbV3BWz73ORL5JLeh9vfb771vuda8W8BCigNait7YIL7sNiWS4Tks26PxqK9WnEEm7h%2BgQJmetRgAhFAfBkHdJKugFHt54aadtOdMUyC%2BwXfiGJzA5TClIG6N%2B07DAY%2BlphkKHD%2BKRUNp%2FvoPt5cmvURYWUJMXDbYMTB3mjQw6AAhaWWe0y%2FvDyaffG3w464BsJ9JPCNQNDVoPRRJpdg1MF2yI%2B3aEsqHGMyqYTAN9NfTJz836MUNrUXkLIFMaIWANWokkJuErTC0N4tT7XQ8hWQQLGlFomT0oa49G1erOHgUpihzVAxKS%2FBLTdqkhKpk45E0rZVXL2kBntTdi7WHCK2cdj6%2BnRMRftBYGoV8vinLGWP%2BBHQFiDSog9Vg1nG50asFTGgmLbU%2BqIXGOdD385sCNk7YU1AX3xEJBfFMq3klKwDIFFPPDMeL7ms4laEwAweMV4IXxG1uNkG8Kvy%2BE%2BLeVl%2BzlXg3MZS83AL89WcgrbRZKqw7w7bEK5vuAV9tvtmSO2uvkXPWdN1YQFJo%2Figa4sNz0Nxy0MiAIclJzrQz40V7OQHHzxUa8B1AcjPovw6fgtVD7GXJIuvCnFfEXZEnhv%2BrdAlbrdOmIzEKsKgxFDcaPDHyXHIUmyD4xQdfeBl0zHIiUPitB3q72IrCNPz7U0PY5KTIDfMbJgaxTJG3tgXjpde9ni9BnnkVdqYwwoimZOLn4Sy0b8weNV6b2V8NDResDwArwepwuwCN%2FTScrfz9JyRler9aO9mLRBJOsURok5qWRT49dWzalnERQo40QVXb3E8k4GlQutOFKkxuVWrCaPzcGFUL26ZGrjVPBIxOTwEE6TrOrQk67NZ26n9bCuoEiYYuRdd2USndy7FJcHTVyEkXGiyfU2ZxNtesEcCS3R29c8IbFpE%2FshDcCWn9nKzyVaLv%2FVZrdU9R6l6s3SlFZ1y%2B%2BvR7JbkRA%2B91kn7pGgdwtFPDRAdTFJL4LaUuABAIL6GrfBTLMFCDh07cUsqlhc3hujPhPD8nKuUclJ%2BUeKDWDhepXgq835VNWG3quZ1u55kAqUMCZJOcXwV45uUdRuEy6ppVgcGgfbEO%2FHBzxLE5mcqEiiHkn39F9wQ9%2FqatQiRG%2F2arTaTGL37CyEdPVYTkBmUBs%2BV0T02MObxp97Vo%3D&_eventId=submit'.format(username, password)
    s = requests.Session()
    s.post('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F', headers=headers, data=data)
    return s

def get_userdata(session):
    schedule_response = session.get('https://calcentral.berkeley.edu/college_scheduler/UGRD/2168')
    matches = re.findall('jsonData = (.*?);\s*Scheduler.initialize', schedule_response.text, re.DOTALL)
    return json.loads(matches[0])

weekday_abbrv_converter = {"U": "SU", "M": "MO", "T": "TU", "W": "WE", "R": "TH", "F": "FR", "S": "SA"}

def make_calender(userdata_json):
    cal = Calendar()
    for section in userdata_json['currentSectionData']:
        dept, course_number, section_number, ccn = section['subjectId'], section['course'], section['sectionNumber'], section['id']
        meeting = section['meetings'][0]
        meeting_type = meeting['meetingType']
        start_date, end_date = du_parser.parse(meeting['startDate']), du_parser.parse(meeting['endDate'])
        start_time, end_time = datetime.datetime.strptime(str(meeting['startTime']), "%H%M"), datetime.datetime.strptime(str(meeting['endTime']), "%H%M")
        dtstart = start_date.replace(hour=start_time.hour, minute=start_time.minute)
        dtend = start_date.replace(hour=end_time.hour, minute=end_time.minute)
        byday = [weekday_abbrv_converter[x] for x in meeting['daysRaw']]
        location = meeting['location']
        section_name = "{}{} {} {}".format(dept, course_number, meeting_type, section_number)
        if len(byday) == 0:
            print "warning: Your {} has no appointed time, ignored in calender".format(section_name)
            continue
        event = Event()
        event.add('summary', section_name)
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        event['location'] = vText(location)
        event.add('rrule', {'freq': 'weekly', 'until': end_date, 'byday': byday})
        cal.add_component(event)
    return cal

def main(filename):
    username = raw_input('CalNet ID:')
    password = getpass.getpass()
    session = calnet_login(username, password)
    userdata_json = get_userdata(session)
    calender = make_calender(userdata_json)
    text = calender.to_ical()
    with open(filename, 'w+') as f:
        f.write(text)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ical from calcentral scheduler planner')
    parser.add_argument('-o', '--outfile', type=str, dest="outfile",
                        default="schedule.ical",
                        help="ouput filename")
    options = parser.parse_args()
    main(options.outfile)
