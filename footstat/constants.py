URL_FBREF = 'https://fbref.com'

NAME_CHANGES = {
    "Ath Paranaense": "Athletico Paranaense",
    "Atl Goianiense": "Atlético Goianiense",

    "Eint Frankfurt": "eintracht_frankfurt",
    "Gladbach": "monchengladbach",
    "Leverkusen": "bayer_leverkusen",
    "St. Pauli": "st_pauli",

    "Betis": "real_betis",

    "Inter": "internazionale",

    "Manchester Utd": "manchester_united",
    "Tottenham": "tottenham_hotspur",
    "Wolves": "wolverhampton_wanderers",
    "Sheffield Utd": "sheffield_united",
    "Newcastle Utd": "newcastle_united",
    "Brighton": "brighton_and_hove_albion",
    "West Ham": "west_ham_united",
    "Nott'ham Forest": "nottingham_forest",
    "West Brom": "west_bromwich_albion"
}

STATISTICS = {
    'all_comps/shooting/': [
        ['Date', 'Sh', 'SoT', 'Dist',], 
        []
    ],
    'all_comps/keeper': [
        ['Date', 'SoTA', 'Saves', 'PSxG'], 
        []
    ],
    'all_comps/passing': [
        ['Date', 'Cmp', 'Att', 'TotDist', 'PrgDist', 'Ast', 'xAG', 'xA', 'CrsPA', 'PrgP', 'KP', '1/3'], 
        {'1/3': 'pass_3rd'}
    ],
    'all_comps/passing_types': [
        ['Date', 'Sw', 'Crs', 'CK'], 
        []
    ],
    'all_comps/gca': [
        ['Date', 'SCA', 'GCA'], 
        []
    ],
    'all_comps/defense': [
        ['Date', 'Tkl', 'TklW', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Blocks', 'Int', 'Clr', 'Err'], 
        {'Att 3rd': 'Tkl_Att_3rd', 'Def 3rd': 'Tkl_Def_3rd', 'Mid 3rd': 'Tkl_Mid_3rd'}
    ],
    'all_comps/possession': [
        ['Date', 'Touches',	'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'PrgC', '1/3', 'Mis', 'Dis'], 
        {'Def Pen': 'Touches_Def_Pen', 'Def 3rd': 'Touches_Def_3rd', 'Mid 3rd': 'Touches_Mid_3rd', 'Att 3rd': 'Touches_Att_3rd', 'Att Pen': 'Touches_Att_Pen', '1/3': 'Carries_Att_3rd'}
    ],
    'all_comps/misc': [
        ['Date', 'CrdY', 'CrdR', 'Fls', 'Fld', 'Off', 'Recov', 'Won', 'Lost'], 
        {'Won': 'Aerials_Won', 'Lost': 'Aerials_Lost'}
    ]
}