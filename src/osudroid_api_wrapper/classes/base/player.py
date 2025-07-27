import bs4
import datetime
import requests


class Player:
    def __init__(self):
        self.uid: int = 0
        self.username: str = None
        self.country: str = None
        self.score_rank: int = 0
        self.pp_rank: int = 0
        self.country_rank: int = 0
        self.pp: float = 0.0
        self.total_score: int = 0
        self.playcount: int = 0
        self.accuracy: float = 0.0
        self.registered_on: int = 0
        self.last_login: int = 0

    def __parse(self, soup):
        text_content = soup.get_text()
        country_index = text_content.find("Location:")
        self.country = (
            text_content[country_index + len("Location:") :].splitlines()[0].strip()
        )
        score_rank_index = text_content.find("Score Rank:")
        self.score_rank = int(
            text_content[score_rank_index + len("Score Rank:") :]
            .splitlines()[0]
            .strip()
            .replace("#", "")
        )
        pp_rank_index = text_content.find("PP Rank:")
        self.pp_rank = int(
            text_content[pp_rank_index + len("PP Rank:") :]
            .splitlines()[0]
            .strip()
            .replace("#", "")
        )
        self.username = soup.select_one(
            "html body main div nav div div div:nth-of-type(3) div:nth-of-type(1) a:nth-of-type(1)"
        ).text

        table = soup.find("table")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                if columns:
                    if columns[0].text == "Performance Points":
                        self.pp = float(
                            columns[1].text.replace(",", "").replace("pp", "")
                        )
                    elif columns[0].text == "Ranked Score":
                        self.total_score = int(columns[1].text.replace(",", ""))
                    elif columns[0].text == "Play Count":
                        self.playcount = int(columns[1].text.replace(",", ""))
                    elif columns[0].text == "Hit Accuracy":
                        self.accuracy = float(columns[1].text.replace("%", ""))
        return self

    @classmethod
    def _parse_from_bsoup(cls, soup) -> "Player":
        player = cls()
        player.__parse(soup)
        return player

    @classmethod
    def _from_api_response(cls, data) -> "Player":
        player = cls()

        player.uid = data["UserId"]
        player.username = data["Username"]
        player.pp_rank = int(data["GlobalRank"])
        player.country_rank = int(data["CountryRank"])
        player.total_score = int(data["OverallScore"])
        player.pp = int(data["OverallPP"])
        player.playcount = int(data["OverallPlaycount"])
        player.accuracy = float(data["OverallAccuracy"]) * 100
        player.registered_on = datetime.datetime.strptime(
            data["Registered"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).timestamp()
        player.country = data["Region"]
        return player

    @classmethod
    def from_droid_site(cls, uid: int) -> "Player":
        player = cls()
        url = f"https://osudroid.moe/profile.php?uid={uid}"
        response = requests.get(url)
        player.uid = uid
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        player.__parse(soup)
        return player

    @classmethod
    def from_api(cls, uid: int = None, username: str = None) -> "Player":
        if username:
            url = f"https://new.osudroid.moe/apitest/profile-username/{username}"
        elif uid:
            url = f"https://new.osudroid.moe/apitest/profile-uid/{uid}"
        response = requests.get(url)
        data = response.json()
        player = cls._from_api_response(data)
        return player

    @property
    def to_dict(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "country": self.country,
            "score_rank": self.score_rank,
            "pp_rank": self.pp_rank,
            "pp": self.pp,
            "total_score": self.total_score,
            "playcount": self.playcount,
            "accuracy": self.accuracy,
        }
