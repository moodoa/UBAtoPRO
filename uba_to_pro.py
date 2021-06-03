import re
import requests
from bs4 import BeautifulSoup

class UBATOPRO:
    def _get_schools_url(self, year):
        content = requests.get(f"http://uba.tw/{year}/%E5%85%AC%E9%96%8B%E7%94%B7%E4%B8%80%E7%B4%9A/TeamRank").content
        soup = BeautifulSoup(content, "lxml")
        pattern = r".+Team/Index/(.+)"
        all_school_href = []
        for element in soup.select("table.record_tableHead")[-1].select("a"):
            school_href = element["href"]
            if re.findall(pattern, school_href):
                all_school_href.append(re.findall(pattern, school_href)[0])
        return all_school_href

    def _get_players_name(self, year, school_url):
        content = requests.get(f"http://uba.tw/{year}/%E5%85%AC%E9%96%8B%E7%94%B7%E4%B8%80%E7%B4%9A/Team/Index/{school_url}").content
        soup = BeautifulSoup(content, "lxml")
        names = []
        for name in soup.select_one("div#players").select("a"):
            if name.text not in names:
                names.append(name.text)
        return names

    def _non_playing_uba_players(self, start_year, end_year):
        all_players = []
        for year in range(start_year, end_year+1):
            for url in self._get_schools_url(year):
                for name in self._get_players_name(year, url):
                    if name not in all_players:
                        all_players.append(name)
        now_playing_players = []
        for url in self._get_schools_url(end_year):
            for name in self._get_players_name(end_year, url):
                if name not in now_playing_players:
                        now_playing_players.append(name)
        for player in now_playing_players:
            all_players.remove(player)
        return all_players
    
    def _get_plg_players(self):
        players = []
        for team in range(1, 5):
            content = requests.get(f"https://pleagueofficial.com/team/{team}").content
            soup = BeautifulSoup(content, "lxml")
            for element in soup.select_one("div.player_list").select("h3.mt-md-3"):
                element.span.extract()
                players.append(element.text.strip())
        return players
    
    def _get_sbl_players(self):
        players = []
        for team in range(196, 201):
            infos = requests.get(f"https://sleague.tw/jsons/teams/1/34/{team}/teamrosterlist.json").json()
            for info in infos:
                players.append(info["roster"]["name"])
        return players

if __name__ == "__main__":
    UBAtoPRO = UBATOPRO()
    non_playing_uba_players = UBAtoPRO._non_playing_uba_players(102, 109)
    plg_players = UBAtoPRO._get_plg_players()
    sbl_players = UBAtoPRO._get_sbl_players()
    pro_players = plg_players + sbl_players
    pro_count = 0
    print("進軍職業球員名單:")
    for player in pro_players:
        if player in non_playing_uba_players:
            pro_count += 1
            print(player)
    print(f"\n\n進入職業聯盟人數:{pro_count}\n\n非現役 UBA 男子一級球員人數:{len(non_playing_uba_players)}\n\n進軍職業比例:{round(pro_count/len(non_playing_uba_players)*100,2)}%")