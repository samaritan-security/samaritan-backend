'''
Samaritan Security Alerts Function

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Kate Brune, Ryan Goluch
'''

from app import check_for_unauthorized, add_new_alert

from_email = "samaritan.sec@gmail.com"
from_password = "sdmay2045"

def check_for_alert(id: str, camera_id: str):
    if check_for_unauthorized(id):
        alert(id, camera_id)


def alert(id: str, camera_id: str):
    add_new_alert(id, camera_id)


def send_alert_email(image):

    return True