import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin.db import Reference


class FirebaseProcessor:
    db_ref: Reference

    def __init__(self):
        cred = credentials.Certificate('service_key.json')

        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://python-tg-bot-default-rtdb.europe-west1.firebasedatabase.app'
        })

        self.db_ref = db.reference('py/')

    def check_if_user_exists(self, user_id: str) -> bool:
        print('Checking db...')
        data = self.db_ref.get(f'users/{user_id}')

        return data is not None

    def add_user_data_to_db(self, user_id: str, lat: str, long: str):
        print('Adding user to db...')
        data = self.db_ref.child(f'users/{user_id}')
        data.set({
            'userId': user_id,
            'latitude': lat,
            'longitude': long
        })