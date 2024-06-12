import bs4
import pandas as pd
import requests


def scrape():
    res = requests.get("https://www.kinomalta.pl/seanse")
    soup = bs4.BeautifulSoup(res.content, features="html.parser")

    screening_times = soup.find(class_="screening-times")
    tags: list[bs4.Tag] = screening_times.find_all(class_=["today-date", "movie-link"])

    entries = []
    current_date = None
    for tag in tags:
        if tag.get("class")[0] == "today-date":
            current_date = tag.find("time").get("datetime")
            continue

        if not current_date:
            continue

        entries.append(
            (
                current_date,
                tag.find("span", class_="time").text.strip(),
                tag.find("span", class_="room").text.strip(),
                tag.find("span", class_="title").text.strip(),
            )
        )
    df = pd.DataFrame(entries, columns=("date", "time", "room", "title"))

    df.to_csv("screening_times.csv")


if __name__ == "__main__":
    scrape()
