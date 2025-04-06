from ..classes.score import Score
from ..classes.base.player import Player
from typing import List
import bs4
import requests


class Profile():
    def __init__(self):
        self.player: Player = Player()
        self.recent_scores = []
        self.top_scores = []

    def __get_recent_scores(self, soup) -> List[Score]:
        recent_scores = Score._parse_from_bsoup(soup, "Recent Plays")
        player = Player._parse_from_bsoup(soup)
        for score in recent_scores:
            score.player = player
        self.recent_scores = recent_scores
        return recent_scores

    def __get_top_scores(self, soup) -> List[Score]:
        top_scores = Score._parse_from_bsoup(soup, "Top Plays")   
        player = Player._parse_from_bsoup(soup)
        for score in top_scores:
            score.player = player
        self.top_scores = top_scores
        return top_scores
    

    @classmethod
    def from_api(cls, uid: int = None, username: str = None) -> 'Profile':
        profile = cls()
        if username:
            url = f"https://new.osudroid.moe/apitest/profile-username/{username}"
        elif uid:
            url = f"https://new.osudroid.moe/apitest/profile-uid/{uid}"
        resp = requests.get(url)
        data = resp.json()
        profile.player = Player._from_api_response(data)
        for score in data['Last50Scores']:
            score_obj = Score._from_api_response(score)
            score_obj.player = profile.player
            profile.recent_scores.append(score_obj)
        for score in data['Top50Plays']:
            score_obj = Score._from_api_response(score)
            score_obj.player = profile.player
            profile.top_scores.append(score_obj)
        return profile
                

    @classmethod
    def from_droid_site(cls, uid: int) -> 'Profile':
        url = f"https://osudroid.moe/profile.php?uid={uid}"
        profile = cls()
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        profile.player = Player._parse_from_bsoup(soup)
        profile.player.uid = uid
        profile.__get_recent_scores(soup)
        profile.__get_top_scores(soup)
        return profile
                
    
    @property
    def to_dict(self):
        return {
            'player': self.player.to_dict if self.player else None,
            'recent_scores': [score.to_dict  for score in self.recent_scores],
            'top_scores': [score.to_dict for score in self.top_scores]
        }
                
                


        
    
