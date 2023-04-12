import requests
import constants
from processors.firebase_processor import FirebaseProcessor


class Responses:
    database: FirebaseProcessor

    def __init__(self):
        self.database = FirebaseProcessor()

    def sample_response(self, input_text: str, user_id: str) -> str:
        user_exists_flag = self.__user_exists(user_id)
        print(user_exists_flag)
        return "Поки що я цього не розумію"

    async def handle_location(self, user_id: str, latitude: str, longitude: str) -> str:
        user_exists_flag = self.__user_exists(user_id)

        if user_exists_flag is not True:
            self.database.add_user_data_to_db(user_id, latitude, longitude)

        request = requests.get(url=
                               f'http://api.weatherapi.com/v1/current.json?key={constants.WEATHER_API_KEY}&q={latitude},{longitude}&lang=uk')

        data = request.json()

        current_weather = str(data['current']['condition']['text']).lower()
        current_degrees = int(data['current']['temp_c'])
        degrees_text = 'градусів'

        if current_degrees % 2 == 0:
            degrees_text = 'градуси'

        degrees_text += ' тепла' if current_degrees >= 0 else degrees_text + ' морозу'

        return f'Зараз на вулиці {current_weather} і {current_degrees} {degrees_text}'

    def __user_exists(self, user_id: str) -> bool:
        return self.database.check_if_user_exists(user_id)
