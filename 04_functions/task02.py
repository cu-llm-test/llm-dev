import urllib.request
import datetime

def save_url_content(url):
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")[:500]  # 先頭500文字だけ取得
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"{now}.txt", "w", encoding="utf-8") as file:
        file.write(content)
        return file.name

url = input("URLを入力してください: ")
file_name = save_url_content(url)
print(f"Content saved in: {file_name}")