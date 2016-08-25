import json
from icalendar import Calendar, Event, vText
from dateutil import parser as du_parser
from dateutil.tz import tzlocal
import datetime

weekday_abbrv_converter = {"U": "SU", "M": "MO", "T": "TU", "W": "WE", "R": "TH", "F": "FR", "S": "SA"}

class_json_file = "class.json"

cal = Calendar()

with open(class_json_file) as data_file:    
    class_json = json.load(data_file)
    for section in class_json['sections']:
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
        event = Event()
        event.add('summary', section_name)
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        event['location'] = vText(location)
        event.add('rrule', {'freq': 'weekly', 'until': end_date, 'byday': byday})
        cal.add_component(event)

print cal.to_ical()