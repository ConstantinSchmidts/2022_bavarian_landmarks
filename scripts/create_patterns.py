# Creating pattern file with names of landmarks for prodigy.
# -*- coding: utf-8 -*-
# import json
import srsly
import pandas as pd
import glob

# Handcollected example landmarks
terms = [
                "Funkhaus München",
                "Schloss Neuschwanstein",
                "Amtsgericht Eggenfelden",
                "Landratsamt Rottal-Inn",
                "Altes Rathaus",
                "Bayerische Staatskanzlei",
                "Bayerisches Staatsministerium für Ernährung, Landwirtschaft und Forsten",                 
                "Bayerisches Landwirtschaftsministerium",
                "Fuggerei",
                "Burg Trausnitz",
                "Schloss Nymphenburg",
                "Regensburger Dom",
                "Alte Mainbrücke",
                "Residenz Würzburg",
                "Residenz Ansbach",
                "Käppele",
                "Eremitage",
                "Kongresshalle Reichsparteitagsgel�nde",
                "Nürnberger Opernhaus",  
                "AKW Grafenrheinfeld",
                "KKW Grafenrheinfeld",
                "Atomkraftwerk Grafenrheinfeld",
                "Kernkraftwerk Grafenrheinfeld",
                "Limeseum",
                "Justizvollzugsanstalt Landsberg am Lech",
                "Hauptbahnhof München",
                "Nürnberg Hbf",
                "Augsburg Hauptbahnhof",
                "BMW-Werk Dingolfing",
                "Campeon", 
                "Therme Bad Wörishofen", 
                "Bleistiftfabrik",
                "Rhön-Klinikum Campus Bad Neustadt",
                "Isarphilharmonie",
                "Hackerbrücke",
                "Passionstheater Oberammergau",   
                "Bayerisches Eisenbahnmuseum",   
                "Hochschule für Allgemeine Innere Verwaltung Hof",   
                "Fraunhofer Institut für Silicatforschung",   
                "Erdgas Schwaben Arena Kaufbeuren",
                "Gasteig-Kulturzentrum",
                "Maximilianeum",
                "Justizpalast",
                "Landgericht Schweinfurt", 
                "Geburtshaus von Papst Benedikt XVI",  
                "Gärtnerplatztheater",
                "Kiliansbrunnen",
                "Pompejanum",
                "Kloster Banz",
                "Friedensengel München",
                "Krankenhaus Agatharied",
                "Gradierwerk Bad Kissingen",
                "Burg Falkenberg",
                "Rosenturm Kronach",
                "Prinz-Luitpold-Turm",
                "Basilika Vierzehnheiligen",
                "Karlstor",
                "Nabburger Tor",
                "Schloss Mespelbrunn",
                "Schloss Dennenlohe",
                "Schloss Ehrenburg",
                "Schloss Johannisburg",
                "Münchner Hofbräuhaus",
                "Schöner Brunnen Nürnberg", 
                "Schloss Elmau", 
                "Neue Residenz Bamberg", 
                "Orangerie Ansbach", 
                "Plassenburg", 
                "Rathaus Straubing", 
                "Salzbergwerk Berchtesgaden", 
                "Salzstadel Regensburg", 
                "Schönborner Hof Aschaffenburg", 
                "Schöner Brunnen (Nürnberg)", 
                "Schöner Turm (Erding)", 
                "Stift Haug", 
                "St. Johann Baptist (Neu-Ulm)", 
                "Synagoge Bayreuth", 
                "Tucherschloss Nürnberg", 
                "Veste Oberhaus", 
                "Walhalla Donaustauf", 
                "Weinstadel Nürnberg", 
                "Wimmer Ross Pfarrkirchen", 
                "Bohrturm Luitpoldsprudel", 
                "Geburtshaus Papst Benedikt", 
                "Landestheater Schwaben",
                "Schloss Höchstädt"                                                                                     
            ]

patterns = []

# Reformat list of term to patterns 
for entity in terms:
    pl = []
    for word in entity.split():
            pl.append({"lower": word.lower()})
    LaMa_dict = {"label": "LM", "pattern": pl}  
    patterns.append(LaMa_dict)

# Read in all .csv files in data folder
path = './data/*.csv' 
csv_files=glob.glob(path) 

import pandas as pd
df_from_each_file = (pd.read_csv(f, encoding="utf-8", header=None, sep=",") for f in csv_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

# Reshape to pattern dict and add to pattern list
for i in range(len(concatenated_df)):
    # Only use patterns of a certain length, no abbreviations
    if len(concatenated_df.iloc[i,0]) > 2:
        pl = []
        for word in concatenated_df.iloc[i,0].split():
            pl.append({"lower": word.lower()})
        LaMa_dict = {"label": "LM", "pattern": pl}  
        patterns.append(LaMa_dict)

# Save as .jsonl file
srsly.write_jsonl("./data/patterns.jsonl", patterns)
        