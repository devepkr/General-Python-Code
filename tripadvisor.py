import json
import requests
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("tripadvisor_scraper.log", encoding="utf-8")])
logger = logging.getLogger(__name__)

class Tripadvisor:
    def __init__(self, LOCATION_ID, PROXIES, limit=20):
        self.url = 'https://www.tripadvisor.in/data/graphql/ids'
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/json',
            'origin': 'https://www.tripadvisor.in',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        self.location_id = LOCATION_ID
        self.proxies = PROXIES
        self.limit = limit
        self.offset = 0
        self.json_data_format = []

    def requests_hits(self):
        payload = [{
            'variables': {
                'locationId': self.location_id,
                'filters': [{'axis': 'LANGUAGE', 'selections': ['en']}],
                'limit': self.limit,
                'offset': self.offset,
                'sortType': None,
                'sortBy': 'SERVER_DETERMINED',
                'language': 'en',
                'useAwsTips': True,
            },
            'extensions': {
                'preRegisteredQueryId': '51c593cb61092fe5',
            },
        }]

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Request failed at offset {self.offset}: {e}")
            return None

    def get_data(self, data):
        try:
            reviews_data = data[0]['data'].get('ReviewsProxy_getReviewListPageForLocation')
            if not reviews_data:
                return False

            reviews = reviews_data[0].get('reviews', [])
            if not reviews:
                return False

            for items in reviews:
                rating = items['rating']
                review_text = items['text'].replace('\n', '')
                userProfile = items['userProfile']
                reviewer_name = userProfile['displayName']
                review_date = items['createdDate']
                platform = 'Tripadvisor'
                likes = ''
                language = items['language']
                publishedDate = items['publishedDate']

                self.json_data_format.append([{
                    "rating": rating,
                    "review_text": review_text,
                    "reviewer_name": reviewer_name,
                    "review_date": review_date,
                    "platform": platform,
                    "likes": likes,
                    "language": language,
                    "publishedDate": publishedDate

                }])

            return True
        except Exception as e:
            print(f"Data parsing failed at offset {self.offset}: {e}")
            return False

    def run_scraper(self):
        condition = 0
        while True:
            data = self.requests_hits()
            if not data:
                break

            has_more_value = self.get_data(data)
            if not has_more_value:
                break

            self.offset += self.limit
            time.sleep(1)

            # break the conditions which we want
            condition += 1
            if condition == 2:
                print("Condition Breaking loop.")
                # break

        # Save to file
        with open('tripadvisor_reviews.json', 'w', encoding='utf-8') as f:
            json.dump(self.json_data_format, f, ensure_ascii=False, indent=4)

        print(""" ************************************** PRINT RESULTS HERE ***************************************""")
        for review in self.json_data_format:
            print(review)

        logger.info(f"Total reviews collected: {len(self.json_data_format)}")


if __name__ == "__main__":
    logger.info("Starting TripAdvisor reviews extraction...")
    proxies = {
        "http": "http://vjgxfunn-rotate:u31zfomj2bo4@p.webshare.io:80/",
        "https": "http://vjgxfunn-rotate:u31zfomj2bo4@p.webshare.io:80/"
    }
    location_id = 23617224
    location_url = f"https://www.tripadvisor.in/Attraction_Review-d{location_id}"
    logger.info(f"Target TripAdvisor URL: {location_url}")
    scraper = Tripadvisor(location_id, proxies)
    scraper.run_scraper()
    logger.info("Completed TripAdvisor reviews extraction.")
