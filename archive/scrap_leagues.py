  def _get_team_match_history(self, season, urls):
    match_history = []
    for team in urls:
      team_name = team.split('/')[-1].replace('-Stats', '').replace('-','_').lower()
      team_mh = pd.read_html(team)[1]
      team_mh['season'] = season
      team_mh['league_id'] = self.league_id
      team_mh['league_name'] = self.name
      team_mh['team'] = team_name
      print(f'--{team_name}')

      data = requests.get(team)
      soup = BeautifulSoup(data.text, features= 'lxml')
      anchor = [link.get("href") for link in soup.find_all('a')]
      ##Shooting
      try:
        links = [l for l in anchor if l and 'all_comps/shooting/' in l]
        shooting = pd.read_html(f"https://fbref.com{links[0]}")[0]
        shooting.columns = shooting.columns.droplevel()
        team_mh = team_mh.merge(shooting[['Date', 'Sh', 'SoT']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Goalkeeping
      try:
        links = [l for l in anchor if l and 'all_comps/keeper' in l]
        goalkeeping = pd.read_html(f"https://fbref.com{links[0]}")[0]
        goalkeeping.columns = goalkeeping.columns.droplevel()
        team_mh = team_mh.merge(goalkeeping[['Date', 'Saves']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Passing
      try:
        links = [l for l in anchor if l and 'all_comps/passing' in l]
        passing = pd.read_html(f"https://fbref.com{links[0]}")[0]
        passing.columns = passing.columns.droplevel()
        team_mh = team_mh.merge(passing[['Date', 'Cmp', 'Att', 'PrgP', 'KP', '1/3']], on= 'Date')
        team_mh.rename(columns={'1/3': 'pass_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass
      ##Passing Types
      try:
        links = [l for l in anchor if l and 'all_comps/passing_types' in l]
        pass_types = pd.read_html(f"https://fbref.com{links[0]}")[0]
        pass_types.columns = pass_types.columns.droplevel()
        team_mh = team_mh.merge(pass_types[['Date', 'Sw', 'Crs']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Goal and Shot Creation
      try:
        links = [l for l in anchor if l and 'all_comps/gca' in l]
        goal_shotcreation = pd.read_html(f"https://fbref.com{links[0]}")[0]
        goal_shotcreation.columns = goal_shotcreation.columns.droplevel()
        team_mh = team_mh.merge(goal_shotcreation[['Date', 'SCA', 'GCA']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Defense
      try:
        links = [l for l in anchor if l and 'all_comps/defense' in l]
        defensive = pd.read_html(f"https://fbref.com{links[0]}")[0]
        defensive.columns = defensive.columns.droplevel()
        team_mh = team_mh.merge(defensive[['Date', 'Tkl', 'TklW', 'Def 3rd', 'Att 3rd', 'Blocks', 'Int']], on= 'Date')
        team_mh.rename(columns={'Att 3rd': 'Tkl_Att_3rd',
                                'Def 3rd': 'Tkl_Def_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass
      ##Possession
      try:
        links = [l for l in anchor if l and 'all_comps/possession' in l]
        possession = pd.read_html(f"https://fbref.com{links[0]}")[0]
        possession.columns = possession.columns.droplevel()
        team_mh = team_mh.merge(possession[['Date', 'Att 3rd']], on= 'Date')
        team_mh.rename(columns={'Att 3rd': 'Touches_Att_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass

      ##Misc
      try:
        links = [l for l in anchor if l and 'all_comps/misc' in l]
        misc = pd.read_html(f"https://fbref.com{links[0]}")[0]
        misc.columns = misc.columns.droplevel()
        if 'Recov' not in misc.columns:
          misc['Recov'] = None
        team_mh = team_mh.merge(misc[['Date', 'Fls', 'Off', 'Recov']], on= 'Date')
      except (ValueError, IndexError):
        pass

      match_history.append(team_mh)
      time.sleep(10)
    match_history = pd.concat(match_history)

    return match_history


