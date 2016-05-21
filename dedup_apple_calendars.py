#!/usr/bin/python
# David Branner
# 20160520

import sys
import hashlib

"""Merge timezone-entities, event-entitites in .ics files; write to disk."""

# Top and bottom of calendar file.
calendar_start = ('''BEGIN:VCALENDAR\n'''
    '''METHOD:PUBLISH\n'''
    '''VERSION:2.0\n'''
    '''X-WR-CALNAME:Merged Calendar\n'''
    '''X-WR-CALDESC:Calender merged by program "dedup_applecalendars.py"\n'''
    '''CALSCALE:GREGORIAN''')

calendar_end = '''END:VCALENDAR'''

def main():
    if len(sys.argv) < 2:
        print('''\n    This program needs the names of .ics files as input '''
              '''in order to proceed.\n''')
        return
    merged_calendar = {'timezones': {}, 'events': {}}
    total_timezones = 0
    total_events = 0

    # Read and process all files.
    for f in sys.argv[1:]:
        file_content = read_ics_file(f)
        calendar_content = process_file_content(file_content)
        total_timezones += len(calendar_content['timezones'])
        total_events += len(calendar_content['events'])
        if calendar_content:
            merged_calendar['timezones'].update(calendar_content['timezones'])
            merged_calendar['events'].update(calendar_content['events'])

    # Report.
    print('Total timezones: {} ({}); total events: {} ({}).'.
            format(len(merged_calendar['timezones']),
                   len(merged_calendar['timezones']) - total_timezones,
                   len(merged_calendar['events']),
                   len(merged_calendar['events']) - total_events,
                   )
            )

    # Write merged calendar to disk.
    output(merged_calendar)

def read_ics_file(f):
    """Read and return file content as list of lines."""
    with open(f, 'r') as open_f:
        content = open_f.read().split('\n')
    return content

def process_file_content(content):
    """Create hash table of unique event and timezone entities."""
    choices = {'BEGIN:VEVENT':    ('events', 'END:VEVENT'),
               'BEGIN:VTIMEZONE': ('timezones', 'END:VTIMEZONE')}
    return_dict = {'timezones': {}, 'events': {}}
    accumulator = None
    for line in content:
        if line in choices:
            # New section begins. Initiate new accumulator
            accumulator = [line]
            current_item = line
        elif accumulator == None or line == calendar_end:
            continue
        else:
            # Line is not section-start; add to accumulator.
            accumulator.append(line)
            if line == choices[current_item][1]:

                # Section ends. Merge as string, hash, add to dict if needed.
                section = '\n'.join(accumulator)
                # Note that encoding and decoding steps are needed.
                new_key = hashlib.sha1(section.encode()).hexdigest()

                # Adding redundantly is perhaps faster than checking.
                return_dict[choices[current_item][0]][new_key] = section
    return return_dict

def output(calendar):
    """Concatenate timezone- and event-entities, attach head/tail, write."""
    # Convert calendar to strings.
    timezones = calendar['timezones'].values()
    events = sorted(calendar['events'].values())
    # Join all parts of calendar into a single string.
    output = '\n'.join([calendar_start,
                        '\n'.join(timezones),
                        '\n'.join(events),
                        calendar_end,
                        ''] # Final blank line is customary.
                     )
    with open('merged_calendar.ics', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()
