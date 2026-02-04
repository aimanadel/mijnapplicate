"""Crud functions for event table"""

from datetime import datetime
from dateutil.parser import isoparse
from flask import Blueprint

from app.db import execute_query

bp = Blueprint("events", __name__)


def create_event(description: str, date: str):
    """Creates new event row in the database

    Args:
        description (str): Description of the event
        date (datetime): Date of the event

    Returns:
        insert_id (int): Insert id given by database
    """
    query = "INSERT INTO Event (description, eventDate) VALUES (?, ?)"
    parsed_date = isoparse(date)
    if check_date_passed(date) is False:
        # Parse the ISO 8601 datetime string and format it for MySQL
        formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')

        result = execute_query(query, (description, formatted_date))
        insert_id = result["insertId"]
        return insert_id


def get_event(event_id):
    """_summary_

    Args:
        event_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    query = "SELECT * FROM Event WHERE eventId = ?"
    result = execute_query(query, event_id)
    if result:
        event = result[0]
        return event


def get_events():
    """AI is creating summary for get_events

    Returns:
        [type]: [description]
    """
    query = "SELECT * FROM Event"
    events = execute_query(query)
    return events


def update_event(event_id: int, description: str, date: str):
    """_summary_

    Args:
        event_id (int): _description_
        description (str): _description_
        date (str): _description_
    """
    query = "UPDATE Event SET description = ?, eventDate = ? WHERE eventId = ?"
    print(execute_query(query, (description, date, event_id)))


def delete_event(event_id: int):
    pass

def check_date_passed(date: str):
    """Check if the event date has passed

    Args:
        date (str): Event date in ISO 8601 format

    Returns:
        bool: True if the event date has passed
    """
    parsed_date = isoparse(date)
    return parsed_date < datetime.now()

from app.events import routes
