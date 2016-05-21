## De-duplicate Apple Calendars on Mavericks

Since OS 10.10 (Yosemite), Apple's "Calendar" program and iCloud service reportedly now removes any duplicate events when two or more calendars are combined. But on OS 10.9 (Mavericks), that functionality doesn't exist: when the merged calendar is uploaded to the iCloud server, each duplicate event generates an error that has to be dismissed manually.

This program combines the timezones and events of any number of exported `.ics` calendars whose paths are passed in on the command line:

```bash
python dedup_apple_calendars.py export_1.ics export_2.ics export_3.ics
```

and writes them to a single file called `merged_calendar.ics` in the present directory.

In the event of duplicate events that are fully identical, only one is retained.

If events are duplicated but have different `LAST-MODIFIED` or `DTSTAMP` properties, I believe Calendar will select the later date-stamp. With that belief in mind, I have omitted any comparison of these properties in selecting between otherwise-identical items. That may prove to be a design error, and I should experiment to see whether finer comparison should be done by this program.

[end]
