from .base.player import Player
from .base.beatmap import Beatmap
from .base.mods import Mods
import datetime
from typing import List

class Score:
    def __init__(self):
        self.scoreid: int = 0
        self.filename: str = None
        self.h300k: int = 0
        self.h300: int = 0
        self.h100k: int = 0
        self.h100: int = 0
        self.h50: int = 0
        self.h0: int = 0
        self.beatmap: Beatmap = Beatmap()
        self.player: Player = Player()
        self.score: int = 0
        self.combo: int = 0
        self.mods: Mods = Mods()
        self.accuracy: float = 0.0
        self.pp: float = 0.0
        self.date: int = 0
        self.grade: str = None
        self.misses: int = 0


        
        
    @classmethod
    def _parse_from_bsoup(cls, soup, ptype:str = "Recent Plays") -> 'List[Score]':
        scores = []
        divs = soup.find_all('div', style="text-align: center; margin-left: 5px; margin-top: 30px;")
        top_div = next(
            (div for div in divs if div.find('b', style="color: #EB2F96;") and div.find('b').text == ptype),
            None
        )

        if not top_div:
            return scores

        top_div = top_div.find_next_sibling()
        for li in top_div.find_all('li', class_='li', style='margin-left: 15px; margin-right: 10px;'):
            score = cls()
            score.grade = li.find('img')['src'].replace('./assets/img/ranking-', '').replace('.png', '')
            div = li.find('div', style='margin-bottom: 15px')
            if div:
                inner_div = div.find('div', style='margin: 0; color: black;')
                small_element = inner_div.find('small', style='margin-left: 50px;')
                details_lines = small_element.get_text(strip=True).split(' / ')
                score.date = datetime.datetime.strptime(details_lines[0], "%Y-%m-%d %H:%M:%S").timestamp()
                score.pp = float(details_lines[1].replace("pp: ", "").replace(",", "")) if details_lines[1].replace("pp: ", "") != "None" else 0.0
                score.score = int(details_lines[2].replace("score:", "").replace(",", ""))
                score.mods = Mods.from_droid_site(details_lines[3].replace("mod: ", ""))
                score.combo = int(details_lines[4].replace("combo:", "").replace("x", ""))
                score.accuracy = float(details_lines[5].replace("accuracy:", "").replace("%", ""))
                score.misses = inner_div.find('small', style='color: #A82C2A;').get_text(strip=True).split(': ')[-1]
                hash_content = inner_div.find('span', style='display:none;').contents[0].split(':')[1].replace('}', '')
                score.beatmap = Beatmap.get_beatmap(md5=hash_content)
            scores.append(score)
        return scores


    @classmethod    
    def _from_api_response(cls, data) -> 'Score':
        score = cls()
        score.scoreid = data['ScoreId']
        score.filename = data['Filename']
        score.mods = Mods.from_droid_api(data['Mods'])
        score.score = data['MapScore']
        score.combo = data['MapCombo']
        score.grade = data['MapRank']
        score.h300k = data['MapGeki']
        score.h300 = data['MapPerfect']
        score.h100k = data['MapKatu']
        score.h100 = data['MapGood']
        score.h50 = data['MapBad']
        score.h0 = data['MapMiss']
        score.accuracy = data['MapAccuracy'] * 100
        score.pp = data.get('MapPP', 0)
        score.date = datetime.datetime.strptime(data['PlayedDate'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        
        return score
    
    @property
    def to_dict(self):
        return {
            'scoreid': self.scoreid,
            'filename': self.filename,
            'h300k': self.h300k,
            'h300': self.h300,
            'h100k': self.h100k,
            'h100': self.h100,
            'h50': self.h50,
            'h0': self.h0,
            'beatmap': self.beatmap.to_dict if self.beatmap else None,
            'player': self.player.to_dict,
            'score': self.score,
            'combo': self.combo,
            'mods': self.mods.to_dict,
            'accuracy': self.accuracy,
            'pp': self.pp,
            'date': self.date,
            'grade': self.grade,
            'misses': self.misses
        }