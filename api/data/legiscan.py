'''
Pull data from Legiscan API

LEGISCAN_API_KEY environment variable must be set with valid API key for the
script to succeed

Usage:
python -m api.data.legiscan

Options:
-j / --json - Write API output to JSON file
'''
import argparse, json

from os import environ
from typing import Any, Dict

import requests

from ..database import engine, SessionLocal
from ..models import Bill

LEGISCAN_API_KEY = environ.get('LEGISCAN_API_KEY')
LEGISCAN_API_URL = 'https://api.legiscan.com/'
LEGISCAN_API_OP = 'getMasterList'
STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", action="store_true",
                        help="Write API data to JSON files")
    return parser


def setup_database() -> SessionLocal:
    '''
    TODO: Use Alembic or other migration tool
    For now - this drops and recreates tables in local DB
    '''
    Bill.metadata.drop_all(engine)
    Bill.metadata.create_all(engine)

    session = SessionLocal()
    return session


def get_state_bills(write_json: bool, session: SessionLocal) -> None:
    for state in STATES:
        data = fetch_state_bills(state, write_json)
        write_to_database(state, data, session)


def fetch_state_bills(state: str, write_json: bool) -> Dict[str, Any]:
    payload = {
        'key': LEGISCAN_API_KEY,
        'op': LEGISCAN_API_OP,
        'state': state
    }
    resp = requests.get(LEGISCAN_API_URL, params=payload)
    resp.raise_for_status()

    data = resp.json()
    if write_json:
        write_json_file(state, data)
    return data


def write_json_file(state: str, data: Dict[str, Any]) -> None:
    with open(f'{state}_bill_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


def write_to_database(state: str, data: Dict[str, Any], session: SessionLocal) -> None:
    session_info = data['masterlist']['session']
    session_id = session_info['session_id']
    session_name = session_info['session_name']
    bill_data = [b for key, b in data['masterlist'].items() if key != 'session']
    for bill in bill_data:
        session.add(Bill(state=state,
                         session_id=session_id,
                         session=session_name,
                         **bill))
    # TODO: status_date or last_action_date may have invalid value '0000-00-00'
    # Need to catch those errors, if present, prior to committing to DB
    session.commit()


def main() -> None:
    if not LEGISCAN_API_KEY:
        raise RuntimeError('API Key not defined')
    parser = init_argparse()
    args = parser.parse_args()
    write_json = args.json
    session = setup_database()
    get_state_bills(write_json, session)


if __name__ == '__main__':
    main()
