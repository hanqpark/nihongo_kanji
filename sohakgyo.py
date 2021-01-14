import requests
import csv
from bs4 import BeautifulSoup


def save_to_file(words):
    file = open("소학교.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["챕터", "한자", "음", "음독", "훈독"])
    for w in words:
        writer.writerow(list(w.values()))
    return


def extract_word_info(html, p):
    # 한자 추출
    hanja = html.find("a").get_text()

    # 음 추출
    kr_read = html.find("span", {"class": "kr_read"})
    if kr_read is None:
        kr_read = "음없음"
    else:
        kr_read = kr_read.get_text()

    # 음독 추출
    jp_read = html.find("div", {"class": "phnt"})
    if jp_read is None:
        jp_read = "음독없음"
    else:
        jp_read = jp_read.find("span", {"class": "area_read"}).get_text(strip=True)

    # 훈독 추출
    jp_mean = html.find("div", {"class": "idea"})
    if jp_mean is None:
        jp_mean = "훈독없음"
    else:
        jp_mean = jp_mean.find("span", {"class": "area_read"}).get_text(strip=True)

    return {
        "page": p,
        "hanja": hanja,
        "kr_read": kr_read,
        "jp_read": jp_read,
        "jp_mean": jp_mean,
    }


def extract_words(url):
    words = []
    for page in range(1, 45):
        print(f"Scrapping page {page}")
        res = requests.get(f"{url}{page}")
        soup = BeautifulSoup(res.text, "html.parser")
        result = soup.find_all("li", {"class": "lst_li2 hanja"})
        for r in result:
            word = extract_word_info(r, page)
            words.append(word)
    return words


if __name__ == "__main__":
    url = f"https://learn.dict.naver.com/m/jpdic/wordbook/kanji/500901/500902/words.nhn?filterType=0&orderType=2&pageNo="
    words = extract_words(url)
    save_to_file(words)
