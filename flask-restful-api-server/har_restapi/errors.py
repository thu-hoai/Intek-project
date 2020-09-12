#!/usr/bin/env python3
"""Define Exception"""

from werkzeug.exceptions import BadRequest, Unauthorized


class NotJsonFormat(BadRequest):
    """Body Is Not Json Format Exception"""

    def __init__(self):
        super().__init__("Not A Json Format Exception")


class UndefinedHTTPHeader(BadRequest):
    """Undefined HTTP header"""

    def __init__(self):
        super().__init__("Undefined HTTP Header")


class WrongBodyMessage(BadRequest):
    """Wrong Body Message"""

    def __init__(self):
        super().__init__("Wrong Body Message")


class InvalidEmailAddress(BadRequest):
    """Invalid Email Exception"""

    def __init__(self):
        super().__init__("InValid Email Address")


class InvalidPassword(BadRequest):
    """Invalid Password Exception"""

    def __init__(self):
        super().__init__("Authentication failure")


class InvalidSignatureException(BadRequest):
    """Invalid Signature Exception"""

    def __init__(self):
        super().__init__("Invalid Request Signature")


class UnregisteredApplicationException(BadRequest):
    """Unregistered Application Exception"""

    def __init__(self):
        super().__init__("Unregistered Consumer Key Application")


class UnregisteredSessionException(BadRequest):
    """Unregistered Session Exception"""

    def __init__(self, session_id):
        super().__init__(description=f"Unregistered Session {session_id}")


class NotAnImageException(BadRequest):
    """Not An Image Exception"""

    def __init__(self):
        super().__init__("Uploaded file is not an Image")


class ManyAttachedFilesException(BadRequest):
    """Too Many Attached Files Exception"""

    def __init__(self):
        super().__init__("Please post one and only one file")


class ManyLocationException(BadRequest):
    """Too Many Location Exception"""

    def __init__(self):
        super().__init__("Many Location Exception")

class NoSuchFileException(BadRequest):
    """No Such Files Exception"""

    def __init__(self):
        super().__init__("Can not find the File Path")


class NotExistedReportException(Unauthorized):
    """Not Expired Report Exception"""

    def __init__(self, report_id):
        super().__init__(
            description=f"The report {report_id} is not registered")


class ExpiredSessionException(Unauthorized):
    """Expired Session Exception"""

    def __init__(self):
        super().__init__("Your session is expired.")


class ExistedPhotoInAnotherReportException(BadRequest):
    """Existed Photo In Another Report Exception"""

    def __init__(self, report_id):
        super().__init__(
            description=f"This photo has been already attached to another report {report_id}")


class MissingLatitudeOrLongitudeHeader(BadRequest):
    """Missing latitude or longitude Exception"""

    def __init__(self):
        super().__init__("Missing latitude or longitude")
