import requests
from selectorlib import Extractor


class Calories:
    """Represents the amount calories, calculated using
    BMR = (10*weight) + (6.25*height) - (5*age) + 5 - (10*temperature)
    """

    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate(self):
        result = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5 - (10 * self.temperature)
        return result


class Temperature:
    """The temperature extracted from the
    timeanddate.com/weather webpage.
    """
    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    base_url = 'https://www.timeanddate.com/weather/'
    yaml_path = 'temperature.yaml'

    def __init__(self, country, city):
        self.country = country.replace(" ", "-")
        self.city = city.replace(" ", "-")

    def get(self):
        url = requests.get(f"{self.base_url}{self.country}/{self.city}")
        full_content = url.text
        extracted = Extractor.from_yaml_file(self.yaml_path)
        raw_result = extracted.extract(full_content)
        # result = float(raw_result['temp'].replace("\xa0°C", "").strip())
        result = float(raw_result['temp'].replace("°C", "").strip())
        return result


if __name__ == "__main__":
    temp = Temperature(country='Saudi Arabia', city='Jeddah').get()
    print(temp)
    cals = Calories(weight=70, height=176, age=35, temperature=temp)
    print(cals.calculate())
