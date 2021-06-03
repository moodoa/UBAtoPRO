# UBAtoPRO
784 為 102 學年至今曾打過 UBA 但已離開之球員的人數，而其中只有 65 人能進軍職業(P+LEAGUE、SBL)，比例約為 8.3%。

![alt text](https://wowsight.tw/wp-content/uploads/2019/03/193059.jpg)

## _non_playing_uba_players
* 變數為 `start_year` 以及 `end_year`，分別為欲查詢之起始學年以及結束年份。
* 回傳值為起始學年開始至結束年份止(不包含)之所有打過 UBA 的球員名單。

## plg_players
* 回傳值為現役 PLEAGUE 球員名單。

## sbl_players
* 回傳值為現役 SBL 球員名單。

## Requirements
python 3

## Usage

```
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

```
## Installation
`pip install -r requriements.txt`。