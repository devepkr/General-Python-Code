import json
import psycopg2
import requests



def get_response():
    sess = requests.Session()
    url = 'https://jsonplaceholder.typicode.com/posts'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    res = sess.get(url, headers=headers)
    res.raise_for_status()
    return res

def get_data():
    res = get_response()
    json_data = json.loads(res.text)
    return json_data



def save_data_postgres(json_data):
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="7789"
    )
    cursor = connection.cursor()
    print(f"Connection to PostgreSQL established successfully.{cursor}")
    # Create table if not exists
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS posts (
                postId INT PRIMARY KEY,
                title TEXT,
                body TEXT);
        """)
    # Check if data is already inserted
    cursor.execute("SELECT COUNT(*) FROM posts;")
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        print("Data already inserted.")
        cursor.close()
        connection.close()
        return

    # Insert data
    for item in json_data:
        cursor.execute(
            """
                INSERT INTO posts (postId, title, body)
                VALUES (%s, %s, %s)
            """, (item['id'], item['title'], item['body']))

    connection.commit()
    print("Data inserted successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    data = get_data()
    save_data_postgres(data)
