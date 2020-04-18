'''
Samaritan Security Alerts Function

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Kate Brune, Ryan Goluch
'''

from app import check_for_unauthorized, add_new_alert, get_camera_by_id, get_person_by_id
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from_email = "samaritan.sec@gmail.com"
from_password = "sdmay2045"


def check_for_alert(id: str, camera_id: str):
    if check_for_unauthorized(id):
        alert(id, camera_id)


def alert(id: str, camera_id: str):
    add_new_alert(id, camera_id)


def send_alert_email(alert: object, receiver: str):
    """

    Parameters
    ----------
    receiver
    alert : object
    """
    msg = MIMEMultipart()
    msg['Subject'] = "New Un-Authorized Alert: " + alert.ref_id
    msg['From'] = from_email
    msg['To'] = receiver
    r_name = receiver.split('@')[0]

    # Building msg body
    msg_header = MIMEText("Dear " + r_name + ",\n")
    camera = get_camera_by_id(alert.camera_id)
    msg_body = MIMEText("There was a new alert on " + camera.nickname + " of an unknown person.\n" +
                        "The image of the unknown person was captured at " + alert.created_at +
                        " and can be seen in the email attachments.\n" +
                        "Please log into Samaritan to determine if this person should remain un-authorized.\n\n" +
                        "Sincerely,\nThe Samaritan Security Team")

    img = get_person_by_id(alert.ref_id)
    msg_image = MIMEImage(img.image)

    msg.attach(msg_header)
    msg.attach(msg_body)
    msg.attach(msg_image)

    try:
        server = smtplib.STMP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, receiver, msg.as_string())
        server.quit()
        print("Success: email sent")
        return True
    except:
        print("Email failed to send.")
        return False
