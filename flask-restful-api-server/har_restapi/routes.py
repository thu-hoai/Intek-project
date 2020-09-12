#!/usr/bin/env python3
""" Initialize Plugins"""
import json
import logging
import os

from flask import jsonify, request
from PIL import Image
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from har_restapi.errors import (
    NotJsonFormat,
    WrongBodyMessage, UndefinedHTTPHeader, NotAnImageException,
    ManyAttachedFilesException, ManyLocationException,
    MissingLatitudeOrLongitudeHeader)
from har_restapi.models import Account, Application, Photo, Report, Session, db
from har_restapi.utils import (
    create_directory_tree,
    is_an_allowed_file_extension,
    remove_photos_from_directory)

logger = logging.getLogger(__name__)

ENDPOINT = {
    'SESSION_CREATION': '/account/session',
    'REPORT_CREATION': '/report'
}
EXPECTED_SESSION_HEADER = ['X-Api-Key', 'X-Api-Sig']
EXPECTED_CONNECTION_BODY = ['email_address', 'password']
# Body of `/report` MUST have below keys
EXPECTED_LOCATION_BODY = ['latitude', 'longitude', 'accuracy']
EXPECTED_REPORT_HEADER = ['X-Api-Key', 'X-Api-Sig', 'X-Authentication']


def init_app(app):
    """Initialize app"""

    db.create_all()

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=code, message=e.description if code == 400 else str(e))

    @app.route(ENDPOINT['SESSION_CREATION'], methods=['POST'])
    def connect():
        """Support login session creation, for the HTTP method POST

        Raises:
            NotJsonFormat: The request body is not Json format
            UndefinedHTTPHeader: Missing Header Exception
            WrongBodyMessage: Missing Body Exception

        Returns:
            dict: Session information
        """

        # Get a header and body message of the request
        if not request.json:
            raise NotJsonFormat()
        body_message = request.json
        header = request.headers
        if not set(EXPECTED_SESSION_HEADER).issubset(header.keys()):
            raise UndefinedHTTPHeader()
        if not set(EXPECTED_CONNECTION_BODY).issubset(body_message.keys()):
            raise WrongBodyMessage()

        # Get ingredients
        email_address = body_message['email_address']
        password = body_message['password']

        # Authenticate client application
        Application.authenticate_application(
            header['X-API-Key'], header['X-API-Sig'], ENDPOINT['SESSION_CREATION'],
            body_message
        )
        # Authenticate the given account
        account = Account.authenticate(email_address, password)

        # In case account is existed, update the creation, update and expiration time
        if account:
            logging.info("Account is existed %s", account)
        # In case the account is not existing, create a new account, session
        else:
            logging.info("Account have not existed. Creating a new one")
            account = Account(email_address=email_address, password=password)
            db.session.add(account)
            db.session.commit()

        session = Session.update_session(account.account_id)
        return jsonify({
            'account_id': session.account_id,
            'expiration_time': session.expiration_time,
            'session_id': session.session_id})

    @app.route(ENDPOINT['REPORT_CREATION'], methods=['POST'])
    def create_report():
        """Create a report for endpoint `report`

        Raises:
            NotJsonFormat: The request body is not Json format
            WrongBodyMessage: Wrong body of the given request

        Returns:
            dict: JSON expression containing the following attributes:
                creation_time (required): Date and time when this report
                    has been registered to the server platform.
                report_id (required): Identification of the report as
                registered in the server platform.
        """
        # Get a header and body message of the request
        if not request.json:
            raise NotJsonFormat()
        header = request.headers
        body_message = request.json
        if not set(EXPECTED_REPORT_HEADER).issubset(header.keys()):
            raise UndefinedHTTPHeader()
        if 'location' not in body_message:
            raise WrongBodyMessage()
        location = body_message['location']
        if not set(EXPECTED_LOCATION_BODY).issubset(location.keys()):
            raise WrongBodyMessage()

        # Authenticate client application
        Application.authenticate_application(
            header["X-API-Key"], header["X-API-Sig"], ENDPOINT['REPORT_CREATION'],
            body_message)

        # Session authentication
        session = Session.authenticate_session(
            request.headers['X-Authentication'])

        # Get the location information
        point = get_location_data(location)

        # Create the report object and add to database
        report = Report(
            account_id=session.account_id, accuracy=location['accuracy'],
            location=point)
        db.session.add(report)
        db.session.commit()

        return jsonify(
            {
                'creation_time': report.creation_time,
                'report_id': report.report_id
            }
        )

    @ app.route('/report/<uuid:report_id>/photo', methods=['POST'])
    def add_report_photo(report_id):
        """Add report photo for the endpoint and the method POST

        Args:
            report_id (uuid.UUID): the UUID string representing the identification
                of the port to add the photo to.

        Raises:
            WrongBodyMessage: Wrong body of the given request

        Returns:
            dict: Json expresssion
                creation_time (required): Date and time when this photo
                    has been registered to the server platform.
                photo_id (required): Identification of the photo as
                    registered in the server platform.
                report_id (required): Identification of the report as
                    registered in the server platform.
        """
        # Authenticate provided report
        report = Report.authenticate_report(report_id)

        # Get the header and body message
        if not set(EXPECTED_REPORT_HEADER).issubset(request.headers.keys()):
            raise UndefinedHTTPHeader()
        if len(request.files) != 1:
            raise ManyAttachedFilesException()
        image = next(request.files.values())
        if sum(1 for _ in request.form.values()) > 1:
            raise ManyLocationException()
        data_location = next(request.form.values())

        # Authenticate client application
        application = Application.authenticate_application(
            request.headers["X-API-Key"], request.headers["X-API-Sig"],
            f'/report/<uuid:{report_id}>/photo', data_location)
        # Authenticate session
        session = Session.authenticate_session(
            request.headers['X-Authentication'])

        # Make sure the file is valid
        if not image or not is_an_allowed_file_extension(image.filename):
            raise NotAnImageException()
        try:
            image = Image.open(image)
        except IOError:
            raise NotAnImageException()

        # Get the photo object
        if request.form:
            location = json.loads(data_location)['location']
            pointz = get_location_data(location)
            bearing = location['bearing'] if 'bearing' in location else None
            accuracy = location['accuracy'] if 'accuracy' in location else None
            photo = Photo(
                report_id=report_id, location=pointz, accuracy=accuracy, bearing=bearing)
        else:
            photo = Photo(report_id=report_id)

        # Forbid Photo Multiple Usage
        if not Photo.authenticate_photo(photo):
            image = Photo.query.filter_by(location=photo.location).first()
            logging.info("Photo %s was uploaded", image.photo_id)
            return jsonify(
                {
                    "creation_time": image.creation_time,
                    "photo_id": image.photo_id,
                    "report_id": image.report_id
                }
            )

        # Create directory to store the image
        filename = secure_filename(image.filename)
        directory = app.config['UPLOAD_FOLDER']
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create directory tree and save image
        path = create_directory_tree(directory, 4, str(photo.photo_id))
        path_name = os.path.join(path, '.'.join([str(photo.photo_id), 'jpeg']))
        logging.info('path %s', path_name)
        image.save(path_name, optimize=True, quality=80)

        # Get the json expression
        return jsonify(
            {
                "creation_time": photo.creation_time,
                "photo_id": photo.photo_id,
                "report_id": photo.report_id
            }
        )

    @app.route('/report/<uuid:report_id>', methods=['DELETE'])
    def delete_report(report_id):
        """Delete the report following the specified endpoint

        Args:
            report_id (uuid.UUID): the identification of the report

        """
        # Authenticate session of the provided report
        report = Report.authenticate_report(report_id)

        # Get the header and body message
        if not set(EXPECTED_REPORT_HEADER).issubset(request.headers.keys()):
            raise UndefinedHTTPHeader()

        # Authenticate client application
        application = Application.authenticate_application(
            request.headers["X-API-Key"], request.headers["X-API-Sig"],
            f'/report/<uuid:{report_id}>/photo', '')
        # Authenticate Session
        session = Session.authenticate_session(
            request.headers['X-Authentication'])

        # Get and delete all photos of the provided report
        photos = Photo.query.filter_by(report_id=report_id).all()
        photo_id_list = []
        for photo in photos:
            photo_id_list.append(str(photo.photo_id))
            db.session.delete(photo)

        # Remove all photos file
        count = remove_photos_from_directory(
            app.config['UPLOAD_FOLDER'], photo_id_list)
        logging.info('The number of removed photo %s', count)
        # Get and delete report information
        db.session.delete(report)
        db.session.commit()

        return ''


def get_location_data(location):
    """Get the location information as a format

    Args:
        location (dict): a dictionary of location information

    Raises:
        MissingLatitudeOrLongitudeHeader: Missing latitude or longitude in location

    Returns:
        str: a string format of the location. Ex: 'POINTZ(12 23 22)'
    """
    if 'latitude' not in location or 'longitude' not in location:
        raise MissingLatitudeOrLongitudeHeader()
    if 'altitude' not in location:
        location_format = 'POINTZ({latitude} {longitude} 0)'
    else:
        location_format = 'POINTZ({latitude} {longitude} {altitude})'

    return location_format.format_map(location)
