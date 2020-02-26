'''
Samaritan Security Alerts Function

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Kate Brune
'''

from app import check_for_unauthorized, add_new_alert


def check_for_alert(id : str):
    if check_for_unauthorized(id):
        alert(id)

def alert(id : str):
    add_new_alert(id)