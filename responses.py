import json
from datetime import datetime
import requests

import constants


def sample_response(input_text: str) -> str:
    formatted_message = str(input_text).lower()

    if formatted_message in ("hello", "hi"):
        return "Hello! It's my bot"

    if formatted_message in ("time", "date"):
        now = datetime.now()

        date_time = now.strftime("%d/%m/%y")

        return str(date_time)

    return "Sorry i don't quite understand you"


async def handle_location(latitude: str, longitude: str) -> str:
    request = requests.get(url=
                           f'http://api.weatherapi.com/v1/current.json?key={constants.WEATHER_API_KEY}&q={latitude},{longitude}&lang=uk')

    data = request.json()

    current_weather = str(data['current']['condition']['text']).lower()
    current_degrees = int(data['current']['temp_c'])
    degrees_text = 'градусів'

    if current_degrees % 2 == 0:
        degrees_text = 'градуси'

    if current_degrees > 0:
        degrees_text += ' тепла'
    else:
        degrees_text += ' морозу'

    return f'Зараз на вулиці {current_weather} і {current_degrees} {degrees_text}'
