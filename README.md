# MoodleCall

My little moodle REST API caller

## Usage

```python
from moodle import Moodle

url = 'https://moodlesite.example.com/webservice/rest/server.php'
token = 'token from moodle'
moodle = Moodle(url, token)

# Moodle site info:
print(moodle('core_webservice_get_site_info'))

# Create courses:
res = moodle('core_course_create_courses', {'courses': [{
    'shortname': 'bestcourse',
    'fullname': 'My best course',
    'categoryid': 1,
}]})
print(res)

```
