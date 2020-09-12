#!/usr/bin/env python3
"""Models of the application"""
import base64
import logging
import re
import uuid
from datetime import datetime, timedelta, timezone

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.types import Geometry
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from har_restapi.errors import (
    ExistedPhotoInAnotherReportException,
    ExpiredSessionException,
    InvalidSignatureException,
    NotExistedReportException,
    UnregisteredApplicationException,
    UnregisteredSessionException)
from har_restapi.utils import hash_message

# Globally accessible libraries
db = SQLAlchemy()

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

logger = logging.getLogger(__name__)


class Account(db.Model):
    """A Class of Account """
    __tablename__ = "account"
    account_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    email_address = db.Column(
        db.Text(),
        unique=True,
        nullable=False)
    password = db.Column(db.Text(), nullable=False)
    creation_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False)
    update_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False)
    session = db.relationship('Session', backref='account', uselist=False)
    report = db.relationship('Report', backref='report')

    def __init__(self, email_address, password):
        """The constructor of Account class

        Args:
            email_address (str): the email address of the user to
            password (str): the password of the user

        Raises:
            ValueError: the email address is not compliant with RFC 5322
        """
        hashed_password = self.hash_password(password)
        super().__init__(email_address=email_address, password=hashed_password)
        if not re.match(EMAIL_REGEX, self.email_address):
            raise ValueError("Invalid email address")

    @classmethod
    def authenticate(cls, email_address, password):
        """Authenticate of the given account

        Args:
            email_address (str): The provided email address
            password (str): The provided password

        Returns:
            Account obj: The email address is registered and
                the email and the password match together.
            None: The email address is not registered.

        Raise:
            Exception: The email address is registered but the email
                and the password don't match together.
        """
        existing_account = cls.query.filter_by(
            email_address=email_address).first()

        # In case the email address is not registered
        if not existing_account:
            return None

        # In case the email address is registered
        hashed_password = existing_account.password
        is_pass_existing = cls.check_password(hashed_password, password)
        logging.info("Is Password Existing? %s", is_pass_existing)
        if not is_pass_existing:
            raise Exception("Invalid password")

        # In case the email address is registered and
        # the email and the password match together.
        return existing_account

    @staticmethod
    def hash_password(password):
        """Hash pasword

        Args:
            password (str): The normal password

        Returns:
            str: Hashable password
        """
        return generate_password_hash(password)

    @staticmethod
    def check_password(password, normal_password):
        """Check if the hashable password is maching with the normal password

        Args:
            password (str): Hashable password

        Returns:
            bool:
                True if the hasable password is maching with
                    the normal password
                False otherwises
        """
        return check_password_hash(password, normal_password)


def get_expiration_time(update_time):
    """Calculate the expiration time of the session

    Args:
        update_time (datetime.datetime)

    Returns:
        datetime.datetime obj: the expiration time
    """
    return update_time + timedelta(days=30)


class Session(db.Model):
    """A Class of Session """
    __tablename__ = "session"
    # Define Session ID
    session_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    # Define Account id
    account_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('account.account_id'),
        unique=True,
        nullable=False)
    # Define Creation time of the session
    creation_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False)
    # Define Update time of the session
    update_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False)
    # Define Expiration time of the session
    expiration_time = db.Column(
        db.DateTime(timezone=True),
        default=get_expiration_time(datetime.utcnow()),
        nullable=False)

    def __init__(self, account_id):
        """The constructor of the Account

        Args:
            account_id (str): Identification of the account of a user
        """
        super().__init__(account_id=account_id)

    @classmethod
    def authenticate_session(cls, session_id):
        """Session authentication

        Args:
            session_id (str): the identification of the session

        Raises:
            UnregisteredSessionException: The provided session is unregistered
            ExpiredSessionException: The provided session is expired

        Returns:
            Session object
        """

        existing_session = cls.query.filter_by(session_id=session_id).first()

        # Raise an exception if the provided session have not registered
        if not existing_session:
            raise UnregisteredSessionException(str(session_id))

        # In case the session is expired, delete the session
        if existing_session.expiration_time < \
                datetime.utcnow().replace(tzinfo=timezone.utc):
            raise ExpiredSessionException()

        return existing_session

    @classmethod
    def update_session(cls, account_id):
        """Update session information

        Args:
            account_id (str): the identification of the account of a user

        Returns:
            Session object:
                If the provided session existed, returns the session which is
                    updated `update_time` and `expiration_time`
                If the provided session does not exist, returns a new session
        """
        session = cls.query.filter_by(account_id=account_id).first()
        # Update `Update time` and `expiration time` if it existed
        if session:
            session.update_time = datetime.utcnow()
            session.expiration_time = get_expiration_time(datetime.utcnow())
        # Create New Session if session have not existed
        else:
            session = cls(account_id)
            db.session.add(session)
        db.session.commit()
        return session


class Application(db.Model):
    """A Class of Application """
    __tablename__ = "application"
    # Define App ID
    app_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)

    # Define app name
    app_name = db.Column(
        db.Text(),
        unique=True,
        nullable=False
    )
    # Define consumer key
    consumer_key = db.Column(
        db.Text(),
        default=uuid.uuid4().hex,
        nullable=False
    )
    # Define consumer secret
    consumer_secret = db.Column(
        db.Text(),
        default=base64.urlsafe_b64encode(uuid.uuid4().hex.encode()).decode(),
        nullable=False
    )
    # Define creation time
    creation_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    # Define update time
    update_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    def __init__(self, app_name):
        """The constructor of Application

        Args:
            app_name (str): The name of the application
        """
        super().__init__(app_name=app_name)

    @classmethod
    def authenticate_application(
            cls, consumer_key, api_signature, path, body_message):
        """Handle the client application

        Args:
            consumer_key (str): the identification of the client application
            api_signature (str): the API Signature
            path (str): The endpoint of the method
            body_message (str): The string of the message body

        Raises:
            UnregisteredApplicationException: Unregistered Application Consumer Key
            InvalidSignatureException: Invalid Request Signature

        Returns:
            Application object: an existed client application
        """
        existing_application = cls.query.filter_by(
            consumer_key=consumer_key).first()

        # In case the consummer key is not registered
        if not existing_application:
            raise UnregisteredApplicationException()

        # In case the application is registered
        expected_api_signature = hash_message(
            existing_application.consumer_secret, path, body_message)
        logging.info('expected_api_signature %s', expected_api_signature)

        if expected_api_signature != api_signature:
            raise InvalidSignatureException()

        # In case the application address is registered
        return existing_application


class Report(db.Model):
    """A class representing a report of photo"""

    __tablename__ = "report"

    report_id = db.Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    account_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('account.account_id'),
        nullable=False
    )
    location = db.Column(
        Geometry(geometry_type='POINTZ', dimension=3),
        nullable=False
    )
    accuracy = db.Column(
        db.Float(),
        nullable=False
    )
    # Define creation time
    creation_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    # Define update time
    update_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    photo = db.relationship('Photo', backref='photo')

    def __init__(self, account_id, accuracy, location):
        """The constructor of the Report

        Args:
            account_id (str): the identification of the account who owns
                the report
            accuracy (float): Accuracy in meters of the geographic location
                of the heritage
            location (str): Information about the geographic location of
                the heritage at risk
        """
        super().__init__(
            account_id=account_id, accuracy=accuracy, location=location)

    @classmethod
    def authenticate_report(cls, report_id):
        """Report authentication

        Args:
            report_id (str): the UUID representing to the report id of the photo

        Raises:
            NotExistedReportException: the provided report_id is not found

        Returns:
            Report obj: the existing report
        """
        existing_report = cls.query.filter_by(report_id=report_id).first()
        if not existing_report:
            raise NotExistedReportException(str(report_id))
        return existing_report


class Photo(db.Model):
    """
    A class representing the photo of the report and declare its attributes:
    Attributes:
        photo_id: Identification of the photo that the RESTful API
            server generates.
        report_id: Identification of the report this photo is attached to.
        location: Geographic location where the photo has been taken.
        accuracy: Accuracy in meters of the geographic location of the heritage.
        bearing: Angle of the direction that the camera pointed to when
            this photo has been taken. The bearing is the number of degrees
            in the angle measured in a clockwise direction from the north line
            to the line passing through the location of the camera in
            the direction the camera was pointing at.
        creation_time: Date and time when the photo has been registered to
            the server platform.
        update_time: Date and time of the most recent modification of one of
            the attributes of this photo.
    """

    __tablename__ = "photo"

    # Identification of the photo that the RESTful API server generates.
    photo_id = db.Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    # Identification of the report this photo is attached to.
    report_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('report.report_id'),
        nullable=False
    )
    # Geographic location where the photo has been taken
    location = db.Column(
        Geometry(geometry_type='POINTZ', dimension=3),
        nullable=True
    )
    # Accuracy in meters of the geographic location of the heritage
    accuracy = db.Column(
        db.Float(),
        nullable=True
    )
    # # Angle of the direction that the camera pointed to when
    # # this photo has been taken.
    bearing = db.Column(
        db.Float(),
        nullable=True
    )
    # Define creation time
    creation_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    # Define update time
    update_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    def __init__(self, report_id, *args, **kwargs):
        """The constructor of the photo update """
        super(Photo, self).__init__(report_id=report_id, *args, **kwargs)

    @classmethod
    def authenticate_photo(cls, photo):
        """Photo authentication: check if the provided photo is registered or not

        Args:
            photo (Photo Object): The provided photo which is to be authenticated

        Raises:
            ExistedPhotoInAnotherReportException: In case the provided photo
                was uploaded in another report

        Returns:
            None: In case the provided photo was uploaded in the same report
            Photo object: In case the provided photo have not yet uploaded
        """
        image = Photo.query.filter_by(location=photo.location).first()
        if image:
            report = Report.query.filter_by(report_id=image.report_id)
            if not report:
                raise ExistedPhotoInAnotherReportException(image.report_id)

            # Do not add to database if the photo was uploaded
            return None

        # In case photo have not yet uploaded, add photo object to database
        db.session.add(photo)
        db.session.commit()
        # Update `update_time` of the report
        report = Report.query.filter_by(report_id=photo.report_id)
        report.update_time = datetime.utcnow()
        db.session.commit()
        return photo
