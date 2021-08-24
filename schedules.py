#!/usr/bin/env python3

from datetime import datetime as dt, tzinfo, timedelta
import pytz
import uuid

def classes():
    return  {
        'ISYE6501-MSA': {   
            "code": "ISYE6501",     
            'name': 'Intro to Analytics modelling',
            'classes': {
                "days": ["MO", "WE"],
                "time": ["11:00", "1H15M"],
                "location": "Love 185",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "Joel Sokol",
                    "email": "jsokol@isye.gatech.edu",
                    "office_hours": [
                        {"days": ["WE"],
                        "time": ["12:30", "1H"],
                        "location": "Groseclose 419"
                        }]
                },
                {        
                    "role": "TA",
                    "name": "Di Liu",
                    "email": " dliu97@gatech.edu",
                    "office_hours": [
                        {"days": ["MO"],
                        "time": ["12:30", "1H"],
                        "location": "TBD"
                        }]
                }
            ],
            "key dates": [
                ("2021-10-06", "Quiz 1"), 
                ("2021-11-10", "Quiz 2"), 
                ("2021-12-01", "Course project due"), 
                ("2021-12-15", "Final Quiz")
            ]
        },
        'ISYE6669-AM': {
            "code": "ISYE6669",
            'name': 'Deterministic Optimization',
            'classes': {
                "days": ["MO", "WE"],
                "time": ["12:30", "1H15M"],
                "location": "IC 211",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "Renato Monteiro",
                    "email": "monteiro@isye.gatech.edu",
                    "office_hours": [
                        {"days": ["TU"],
                        "time": ["16:00", "1H"],
                        "location": "BlueJeans - see Canvas"
                        },
                        {"days": ["FR"],
                        "time": ["15:00", "1H"],
                        "location": "BlueJeans - see Canvas"
                        }]
                }
            ]
        },
        'ISYE/CSE6740-LAN' : {
            "code": "ISYE/CSE6740",
            'name': 'Computational Data Analysis',
            'classes': {
                "days": ["MO", "WE"],
                "time": ["14:00", "1H15M"],
                "location": "Kendeda 152",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "George Lan",
                    "email": " george.lan@isye.gatech.edu",
                    "office_hours": [
                        {"days": ["MO"],
                        "time": ["13:00", "1H"],
                        "location": "Groseclose 445"
                        }
                    ]
                },
                {        
                    "role": "TA",
                    "name": "Chung-yu Lin",
                    "email": "clin427@gatech.edu",
                    "office_hours": [
                        {"days": ["WE", "FR"],
                        "time": ["9:00", "3H"],
                        "location": "TBD"
                        }
                    ]
                },
                {        
                    "role": "TA",
                    "name": "Benjamin Espy",
                    "email": "ben.espy@gatech.edu",
                    "office_hours": [
                        {"days": ["TU", "TH"],
                        "time": ["9:30", "3H"],
                        "location": "TBD"
                        }
                    ]
                }
            ],
            "key dates": [
                ("2021-09-27", "Midterm 1"),
                ("2021-11-03", "Midterm 2"),
                ("2021-12-10", "Final")
            ]
        },    
        'CP8853-BD': {
            'code': "CP8853",
            'name': 'Climate Change Analytics',
            'classes': {
                "days": ["MO", "WE"],
                "time": ["9:30", "1H15M"],
                "location": "Architecture (West) 359",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "William J. Drummond",
                    "email": "bill.drummond@design.gatech.edu",
                    "office_hours": [                
                    ]
                }
            ]
        },
        'ISYE6404-A' : {
            'code': "ISYE6404",
            'name': 'Non-parametric data analysis',
            'classes': {
                "days": ["TU", "TH"],
                "time": ["8:00", "1H15M"],
                "location": "MRDC 2404",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "Jye-Chyi Lu",
                    "email": "jclu@isye.gatech.edu",
                    "office_hours": [                
                    ]
                }
            ]
        },
        "ISYE6413-A": {
            'code': 'ISYE6413',
            'name': 'Design of experiments',
            'classes': {
                "days": ["TU", "TH"],
                "time": ["9:30", "1H15M"],
                "location": "Coll of Computing 17",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "Roshan Vengazhiyil Joseph",
                    "email": "roshan@gatech.edu",
                    "office_hours": [                
                    ]
                }
            ]
        },
        "CSE6040-A": {
            'code': 'CSE6040',
            'name': 'Computing for Data Analysis',
            'classes': {
                "days": ["TU", "TH"],
                "time": ["14:00", "1H15M"],
                "location": "Klaus 1456",
            },
            "office_hours": [
                {        
                    "role": "Instructor",
                    "name": "Richard Wilson Vuduc",
                    "email": "richie@cc.gatech.edu",
                    "office_hours": [                
                    ]
                }
            ]
        }
    }


def get_classes(*args):
    cls = classes()
    if len(args) == 0:
        return list(cls.values())
    else:
        return [course for section, course in cls.items() if section in args]


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

def generate_course(course):
    #generate classes
    course_events = []
    course_events.append(generate_event(
        subject=" ".join([course["code"], course["name"], "lecture"]),
        start_time = course["classes"]["time"][0],
        duration= course["classes"]["time"][1],
        description="Scheduled class",
        location=course["classes"]["location"],
        recurrence=course["classes"]["days"],
        showAsBusy=True
    ))
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
    class_code = ""
    print("""
    This program generates .ics files for selected courses.
    Enter courses one by one using identifiers (see below for list).
    To end entering, type 'END'. This will save MSA.ics to working directory.

    Currently available course list (edit file to add more yourself):
    """)

    cls = list(classes())
    print(" ".join(cls) + "\n\n")
    schedule = []
    while(class_code != "END"):
        class_code = input("Enter class identifier or END to finish\n")
        if class_code in cls:
            schedule.append(class_code)
        elif class_code == "END":
            if len(schedule) == 0:
                print("No courses selected, exiting")
            else:
                calendar = generate_calendar([generate_course(c) for c in schedule])
                f = open("MSA calendar.ics", "w")
                f.write(calendar)
                f.close()
                print("Successfully saved MSA_calendar.ics")
                print("Contains classes: ", " ".join(schedule))
        else:
            print("Invalid course id - try again or type END to finish")

if __name__ == "__main__":
    main()



