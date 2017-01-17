if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

let weekday_abbrv_converter = {"U": "SU", "M": "MO", "T": "TU", "W": "WE", "R": "TH", "F": "FR", "S": "SA"}

let vtimezone_str = 
`BEGIN:VTIMEZONE
TZID:America/Los_Angeles
X-LIC-LOCATION:America/Los_Angeles
BEGIN:DAYLIGHT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
TZNAME:PDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
TZNAME:PST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE`;

let vtimezoneComp = new ICAL.Component(ICAL.parse(vtimezone_str));
let tzid = vtimezoneComp.getFirstPropertyValue('tzid');
let timezone = new ICAL.Timezone({
  component: vtimezoneComp,
  tzid
});

function makeCalender(userdata) {
    let cal = new ICAL.Component(['vcalendar', [], []]);
    pacific_time = 'America/Los_Angeles'; // Berkeley uses Pacific time
    cal.updatePropertyWithValue('X-WR-TIMEZONE', pacific_time);
    cal.addSubcomponent(vtimezoneComp);
    for(section of userdata['currentSectionData']) {
        let dept = section['subjectId'], 
            course_number = section['course'], 
            section_number = section['sectionNumber'], 
            ccn = section['id']
        ;
        let section_dept_and_number = "{0} {1}".format(dept, course_number);
        if(section['meetings'].length == 0) {
            console.warn("warning: Your {0} has no meeting, ignored in calender".format(section_dept_and_number));
            continue;
        }
        let meeting = section['meetings'][0];
        let meeting_type = meeting['meetingType'];
        let start_date = new Date(meeting['startDate']);
            end_date = new Date(meeting['endDate']);
        let start_time = meeting["startTime"], end_time = meeting['endTime'];
        let dtstart = new Date(start_date.getUTCFullYear(), start_date.getUTCMonth(), start_date.getUTCDate(), start_time / 100, start_time % 100, 0);
        let dtend = new Date(start_date.getUTCFullYear(), start_date.getUTCMonth(), start_date.getUTCDate(), end_time / 100, end_time % 100, 0);
        let byday = meeting['daysRaw'].split('').map(function(x) { return weekday_abbrv_converter[x]; } );
        let location = meeting['location'];
        let event_name = "{0} {1} {2}".format(section_dept_and_number, meeting_type, section_number);
        if(byday.length == 0) {
            console.warn("warning: Your {} has no appointed time, ignored in calender".format(event_name));
            continue;
        }
        let vevent = new ICAL.Component('vevent'),
            event = new ICAL.Event(vevent);
        event.summary = event_name;
        event.startDate = ICAL.Time.fromJSDate(dtstart).convertToZone(timezone);
        event.endDate = ICAL.Time.fromJSDate(dtend).convertToZone(timezone);
        event['location'] = location;
        let rrule = new ICAL.Recur({
            'freq': 'WEEKLY',
            'until': ICAL.Time.fromJSDate(end_date).convertToZone(timezone),
            'byday': byday
        });
        vevent.updatePropertyWithValue('rrule', rrule);
        cal.addSubcomponent(vevent);
    }
    return cal;
}

chrome.pageAction.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(
        tab.id, 
        'get_userdata', 
        responseCallback=function(userdata) {
            calender = makeCalender(userdata);
            let calendar_str = calender.toString();
            let download_str_uri = 'data:text/calender;charset=utf-8,' + encodeURIComponent(calendar_str);
            chrome.downloads.download({
                url: download_str_uri,
                filename:"schedule.ics",
                saveAs: true
            });
        }
    );
});


chrome.runtime.onInstalled.addListener(function() {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([
      {
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { urlContains: 'https://berkeley.collegescheduler.com/' },
          })
        ],
        actions: [ new chrome.declarativeContent.ShowPageAction() ]
      }
    ]);
  });
});