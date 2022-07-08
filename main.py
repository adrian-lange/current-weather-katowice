import requests
from bs4 import BeautifulSoup
import tweepy
import keys
import datetime


class Weather:

    list_of_measurements = [
        "Temperatura", "Ciśnienie zredukowane", "Wilgotność", "Wartość PM 2,5", "Wartość PM 10", "Wiatr"
        ]

    url = "https://meteo.gig.eu/#"
    

    def __init__(self, bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):

        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def create_post(self, measurement_values):
        api = tweepy.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_key,
                    consumer_secret=self.consumer_secret, access_token=self.access_token, access_token_secret=self.access_token_secret)

        number_of_value_pm_2_5 = int(measurement_values[self.list_of_measurements[3]].replace(" µg/m³", ""))
        number_of_value_pm_10 = int(measurement_values[self.list_of_measurements[4]].replace(" µg/m³", ""))
        smog_dict = {number_of_value_pm_2_5: None, number_of_value_pm_10: None}

        for key in smog_dict:
            if key in range(0, 38):
                smog_dict[key] = "🟢"
            elif key in range(38, 86):
                smog_dict[key] = "🟡"
            elif key in range(86, 121):
                smog_dict[key] = "🟠"
            else:
                smog_dict[key] = "🔴"

            date = datetime.datetime.now().strftime("%H:%M  %d.%m.%Y")
        try:
            api.create_tweet(
                text=f"#Pogoda #Katowice {date}\n\n🌤️ {self.list_of_measurements[0]}:  {measurement_values[self.list_of_measurements[0]]}\n🤯 {self.list_of_measurements[1]}:  {measurement_values[self.list_of_measurements[1]]}\n💦 {self.list_of_measurements[2]}:  {measurement_values[self.list_of_measurements[2]]}\n🚬 {self.list_of_measurements[3]}:  {measurement_values[self.list_of_measurements[3]]} {smog_dict[number_of_value_pm_2_5]}\n🚬 {self.list_of_measurements[4]}:  {measurement_values[self.list_of_measurements[4]]} {smog_dict[number_of_value_pm_10]}\n🌪️ {self.list_of_measurements[5]}:  {measurement_values[self.list_of_measurements[5]]}")
        except ValueError:
            print("Could not create tweet.")

def main():
    weather = Weather(keys.bearer_token, keys.api_key, keys.api_secret_key, keys.access_token, keys.access_token_secret)

    r = requests.get(weather.url)

    soup = BeautifulSoup(r.text, 'html.parser')

    measurement_values = {}

    for value in weather.list_of_measurements:
        measure_name = soup.find("td", text=f"{value}")
        measure_value = measure_name.next_sibling

        for i in range(len(measure_value)):
            if measure_value.find('small'):
                unwanted = measure_value.find('small')
                unwanted.extract()
                
        measurement_values[measure_name.text] = measure_value.text

    weather.create_post(measurement_values)


if __name__ == "__main__":
    main()