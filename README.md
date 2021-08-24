# ics_machine
A simple Python script to generate ics calendars for GT MSA 2021 Fall semester.

## Course sections currently covered
['ISYE6501-MSA', 'ISYE6669-AM', 'ISYE6740-LAN', 'CP8853-BD', 'ISYE6404-A', 'ISYE6413-A', 'CSE6040-A', 'ISYE6333-A']

## How to use - easy way
1. Download the schedules.py
2. Make it executable with chmod +x schedules.py
3. Run it with ./schedules.py and follow instructions

## How to use - with cmd arguments
You can also run the script with command line arguments
./schedules.py all|classes|office_hours SECTION_ID SECTION_ID SECTION_ID
e.g. `./schedules.py classes ISYE6669-AM ISYE6404-A ISYE6413-A CP8853-BD CSE6040-A ISYE6333-A ISYE6501-MSA ISYE6740-LAN`

## Alternative use - via interactive shell / etc.
1. Import the module
2. Get relevant classes using get_classes("class1", "class2", "class3"...)
3. Generate ics representations of them (e.g. [generate_event(i) for i in selected_classes]
4. Generate a combined calendar representation (e.g. generate_calendar(events))

## Other
* Feel free to submit pull requests to add other courses
* Better documentation pending
* Adding key dates (exams, etc) is in TODO

Enjoy!




