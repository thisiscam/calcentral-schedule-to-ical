# IMPORTANT! This repo currently doesn't seem to work any more, and the author no longer have access to calcentral. See pinned issue #8 for more detail, if you are willing to help out

# Usage

## Python Script

Automatically log in to CalCentral, fetch enrolled sections and generate a calendar file(.ical).

```
$ pip install -r requirements.txt
$ python transform.py [-o output_file]
```

## Chrome Extension

[Use with Chrome](https://chrome.google.com/webstore/detail/calcentral-schedule-to-ic/fepbenicplghedfhmehgdggnddakpdpm?authuser=2)

After installing and enabling the chrome extension, visit [CalCentral Academics](https://calcentral.berkeley.edu/academics "CalCentral Academics") -> Schedule Planner -> click "Organize and preview your upcoming semester"; you will be redirected to "berkeley.collegescheduler.com/spa#", and the extension icon should appear activated. Simply click the icon to download your calendar file and import to your calendar 
