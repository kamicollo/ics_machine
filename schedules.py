#!/usr/bin/env python3

from datetime import datetime as dt, tzinfo, timedelta
import pytz
import uuid
import glob
import pathlib
import os
import json
import sys


def get_classes(*args):
    cls = get_available_classes()
    if len(args) == 0:
        return list(cls.values())
    else:
        return [get_course(section)  for section in cls if section in args]


def get_course(course_code):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/sections/" + course_code + ".json"
    with open(path) as f:
        return json.load(f)


def generate_calendar(events):
    return ("""BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
PRODID:-//Aurimas//Just another python script//EN\n""" + "\n".join(["\n".join(e) for e in events]) + "\nEND:VCALENDAR")


def generate_event(subject, start_time, duration, description = None, location = None, recurrence = ["MO"], showAsBusy = True):
    date_string = "%Y%m%dT%H%M%S"
    now = dt.utcnow().strftime(date_string)
    tz = pytz.timezone("US/Eastern")
    day_map = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4}
    if len([i for i in recurrence if i not in day_map]) > 0:
        raise ValueError("Invalid day identifier provided")
    hour_start, minute_start = start_time.split(":")
    first_day = recurrence[0]    
    class_start = dt(2021, 8, 23, tzinfo = tz)
    class_end = dt(2021, 12, 18, tzinfo = tz)
    st_string = (class_start + timedelta(hours=int(hour_start), minutes=int(minute_start), days=day_map[first_day])).strftime(date_string)
    et_string = "PT" + duration
    rec_string = "FREQ=WEEKLY;UNTIL={};WKST=SU;BYDAY={}".format(class_end.strftime(date_string), ",".join(recurrence)) 
    return(
    """BEGIN:VEVENT
UID:{uid}
CREATED:{now}
DTSTAMP:{now}
LAST-MODIFIED:{now}
CLASS:Public
CATEGORIES:0
SEQUENCE:0
DTSTART;TZID={timezone}:{start_time}
DURATION:{end_time}
DESCRIPTION:{description}
SUMMARY:{subject}
LOCATION:{location}
TRANSP:{status}
RRULE:{rrule}
END:VEVENT """.format(
        now=now, 
        subject=subject,
        description=description,
        location=location,
        status= "OPAQUE" if showAsBusy else "TRANSPARENT",
        start_time=st_string,
        end_time=et_string,
        rrule=rec_string,
        timezone=class_start.strftime("%Z"),
        uid=str(uuid.uuid4()))
    )

def generate_course(course, mode = 'all'):
    #generate classes
    course_events = []
    if mode != "office_hours":
        course_events.append(generate_event(        
            subject=" ".join([course["code"], course["name"], "lecture"]),
            start_time = course["classes"]["time"][0],
            duration= course["classes"]["time"][1],
            description="Scheduled class",
            location=course["classes"]["location"],
            recurrence=course["classes"]["days"],
            showAsBusy=True
        ))
    if mode != "classes":
        for of_hour in course["office_hours"]:
            if len(of_hour["office_hours"]) > 0:
                for oh in of_hour["office_hours"]:
                    course_events.append(generate_event(
                        subject=" ".join([course["code"], "office_hours", of_hour["role"]]),
                        start_time= oh["time"][0],
                        duration= oh["time"][1],
                        description= "office_hours led by " + of_hour["name"] + " <{}>".format(of_hour["email"]),
                        location= oh["location"],
                        recurrence= oh["days"],
                        showAsBusy= False
                    ))         
    return(course_events)

def main():
    if len(sys.argv) > 1:
        #assume courses passed as parameters
        schedule = get_classes(*sys.argv[2:])
        mode = sys.argv[1]
    else:
        class_code = ""
        print("""
        This program generates .ics files for selected courses.
        Enter courses one by one using identifiers (see below for list).
        To end entering, type 'END'. This will save MSA.ics to working directory.

        Currently available course list (edit file to add more yourself):
        """)

        cls = get_available_classes()
        print(" ".join(cls) + "\n\n")
        schedule = []
        while(class_code != "END"):
            class_code = input("Enter class identifier or END to finish\n")
            if class_code in cls:
                schedule.append(get_course(class_code))
            elif class_code == "END":
                mode = ""
                while(mode not in ["all", "classes", "office_hours"]):
                    mode = input("Choose events to be included ('all', 'classes', 'office_hours'")
                break
            else:
                print("Invalid course id - try again or type END to finish")
        
    if len(schedule) == 0:
        print("No courses selected, exiting")
    else:
        calendar = generate_calendar([generate_course(c, mode) for c in schedule])
        f = open("MSA calendar_" + mode + ".ics", "w")
        f.write(calendar)
        f.close()
        print("Successfully saved MSA_calendar for " + mode + ".ics")
        print("Contains classes: ", " ".join(map(lambda x: x["code"], schedule)))
            


def get_available_classes():
    path = str(pathlib.Path(__file__).parent.resolve()) + "/sections/*.json"
    files = glob.glob(path)
    return [os.path.splitext(os.path.basename(i))[0] for i in files]

if __name__ == "__main__":
    main()



