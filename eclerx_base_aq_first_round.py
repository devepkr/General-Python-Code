import json
import requests
from bs4 import BeautifulSoup

class InterviewsQuestion:
    def __init__(self):
        self.url = 'https://www.walgreens.com/store/c/jergens-natural-glow---firming-self-tan-lotion/ID=prod3252493-product'
        self.header = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
        }


    def requests_hit(self):
        sess = requests.session()
        res = sess.get(self.url, headers=self.header)
        soup = BeautifulSoup(res.content, 'lxml')
        return soup


    def extract_data(self):
        soup = self.requests_hit()
        json_script = soup.find('script', type='application/ld+json')
        if json_script:
            try:
                data = json.loads(json_script.string)
                item = data.get('aggregateRating', {})
                ratingValue = item.get('ratingValue', 'N/A')
                reviewCount = item.get('reviewCount', 'N/A')
                print(f"ratingValue ---: {ratingValue}, reviewCount ---: {reviewCount}")
            except json.JSONDecodeError:
                print("Failed to parse JSON.")

call_scraper = InterviewsQuestion()
call_scraper.extract_data()




"""
Expected output
1,5,8,10
2,6,9,11
3,7,8,12
4,5,8,13

"""

arr = [[1,2,3,4],[5,6,7],[8,9],[10,11,12,13]]
n = len(arr)
for i in range(n):
    row = []
    for j in range(n):
        k = i - len(arr[j-1])
        try:
            row.append(str(arr[j][i]))
        except IndexError:
            row.append(str(arr[j][k]))

    print(", ".join(row))


""" select * from emp order by salary desc  limit 3 offset 2 """

