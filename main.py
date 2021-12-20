import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template
import os
import json
input_string ="Have a good day!"
html_str= ""

class Tree:
    def __init__(self, data, children =[]):
        self.data = data
        self.children = children
        self.parent = None
    
    def add_children(self,childs):
        for child in childs:
            child.parent = self
        self.children = self.children + childs

    def print_tree(self):
        print(self.data)
        if(len(self.children) > 0):
            for child in self.children:
                child.print_tree()
    
    def traverse(self):
        if len(self.children) == 0:
            return {}
        return {id(c): {"data": c.data, "children": c.traverse()} for c in self.children}





def ticket(table,website_weather,website_flight):
    return f"""
    <!DOCTYPE html>
<html>
<head>
        <meta charset="UTF-8"/>
        <title>Choose your satisfactory flight</title>
        <style>
            div {{ 
                color: hsl(9, 97%, 49%); 
                font-size: 24pt;      
            }} 
            </style>
    
</head>
<div id = "header"> Choose your satisfactory flight</div>
<p> The table below is the final result based on your selection!</p>
<body>


    {table}
    <p>If you want to check out the weather of your destination, <a href={website_weather}>you can click here!</a></p>
    <p>If you want to check out your ticket, <a href={website_flight}>you can click here!</a></p>
    <p> {{{{input_str}}}}</p>
</body>
</html>
    """

if __name__ == '__main__':
    city_df = pd.read_csv("city.csv")
    final_df1 = pd.read_csv("final_result.csv",index_col=False)

    final_df1.drop(final_df1[final_df1['price'] == "Info"].index, inplace = True)

    root = Tree("what date?")
    day0 = Tree("what weather0")
    day1 = Tree("what weather1")
    day2 = Tree("what weather2")
    root.add_children([day0])
    root.add_children([day1])
    root.add_children([day2])
    weather = []
    for i in range(9):
        weather.append(Tree(f'what price{i}'))
    day0.add_children(weather[0:3])
    day1.add_children(weather[3:6])
    day2.add_children(weather[6:9])

    price = []
    for i in range(18):
        price.append(Tree(f'what ticket{i}'))

    for i in range(9):
        weather[i].add_children(price[2*i:2*i+2])


    today = datetime.today()

    tomorrow = today + timedelta(days=1)
    tomorrow_str = str(tomorrow.year) + "-"+ str(tomorrow.month) + "-"+ str(tomorrow.day)
    day_after_today = today + timedelta(days=2)
    day_after_today_str = str(day_after_today.year) + "-"+ str(day_after_today.month) + "-"+ str(day_after_today.day)
    day_after_tomorrow = today + timedelta(days=3)
    day_after_tomorrow_str = str(day_after_tomorrow.year) + "-"+ str(day_after_tomorrow.month) + "-"+ str(day_after_tomorrow.day)

    weather_df =[]
    for index, row in final_df1.iterrows():
        if(row['date'] == tomorrow_str):
            weather_df.append(row['day1'])
        elif(row['date'] == day_after_today_str):
            weather_df.append(row['day2'])
        elif(row['date'] == day_after_tomorrow_str):
            weather_df.append(row['day3'])
    final_df1['weather'] = weather_df

    final_df1 = final_df1.drop(['day1','day2','day3'],axis = 1)
    final_df1['weather'] = final_df1['weather'].astype(int)
    final_df1 = final_df1.loc[final_df1['price'] != "Info"]
    final_df1 = final_df1.loc[final_df1['price'] != "$1,596"]
    final_df1['price'] = final_df1['price'].str.replace("$","")
    final_df1['price'] = final_df1['price'].astype(int)
    final_df1.to_csv("final_result1.csv",index=False)
    for index, row in final_df1.iterrows():
        if(row['date'] == tomorrow_str and row['weather'] < 32 and row['price'] < 200):
            data_i = Tree(index)
            price[0].add_children([data_i])
        if(row['date'] == tomorrow_str and row['weather'] < 32 and row['price'] >= 200):
            data_i = Tree(index)
            price[1].add_children([data_i])
        if(row['date'] == tomorrow_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] < 200):
            data_i = Tree(index)
            price[2].add_children([data_i])
        if(row['date'] == tomorrow_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[3].add_children([data_i])
        if(row['date'] == tomorrow_str and row['weather'] >= 59 and row['price'] < 200):
            data_i = Tree(index)
            price[4].add_children([data_i])
        if(row['date'] == tomorrow_str and row['weather'] >= 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[5].add_children([data_i])
            
        if(row['date'] == day_after_today_str and row['weather'] < 32 and row['price'] < 200):
            data_i = Tree(index)
            price[6].add_children([data_i])
        if(row['date'] == day_after_today_str and row['weather'] < 32 and row['price'] >= 200):
            data_i = Tree(index)
            price[7].add_children([data_i])
        if(row['date'] == day_after_today_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] < 200):
            data_i = Tree(index)
            price[8].add_children([data_i])
        if(row['date'] == day_after_today_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[9].add_children([data_i])
        if(row['date'] == day_after_today_str and row['weather'] >= 59 and row['price'] < 200):
            data_i = Tree(index)
            price[10].add_children([data_i])
        if(row['date'] == day_after_today_str and row['weather'] >= 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[11].add_children([data_i])

        if(row['date'] == day_after_tomorrow_str and row['weather'] < 32 and row['price'] < 200):
            data_i = Tree(index)
            price[12].add_children([data_i])
        if(row['date'] == day_after_tomorrow_str and row['weather'] < 32 and row['price'] >= 200):
            data_i = Tree(index)
            price[13].add_children([data_i])
        if(row['date'] == day_after_tomorrow_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] < 200):
            data_i = Tree(index)
            price[14].add_children([data_i])
        if(row['date'] == day_after_tomorrow_str and row['weather'] >=32 and row['weather'] < 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[15].add_children([data_i])
        if(row['date'] == day_after_tomorrow_str and row['weather'] >= 59 and row['price'] < 200):
            data_i = Tree(index)
            price[16].add_children([data_i])
        if(row['date'] == day_after_tomorrow_str and row['weather'] >= 59 and row['price'] >= 200):
            data_i = Tree(index)
            price[17].add_children([data_i])


    score_dic ={"000":0, "001":1, "010":2, "011":3, "020":4, "021":5,
    "100":6, "101":7, "110":8, "111":9, "120":10,"121":11,
    "200":12, "201":13, "210":14, "211":15, "220":16, "221":17}

    print("Hello! Welcome to my flight selection system!")
    choose_date = input("Please tell my whether you would like to choose? 0 for tomorrow. 1 for day after tomorrow. 2 for three days from now.")
    choose_weather= input("Please tell me the weather range you would like to choose for the destination. 0 for samller than 32F. 1 for between 32F and 59F. 2 for bigger than 59F.")
    choose_price = input("Please tell my the ticket price you would like to choose. 0 for under $200. 1 for over $200.")
    choose = choose_date + choose_weather + choose_price
    choose_index = score_dic[choose]
    final_choose_index = [] 

    for child in price[choose_index].children:
        final_choose_index.append(child.data)
    user_df = final_df1.loc[final_choose_index]
    unqiue_city = user_df['city'].unique()
    website_weather =""
    website_flight = ""
    table =""
    if(len(unqiue_city) > 0):
        length = len(unqiue_city)
        print("Great! We have found the ticket that meetes you requiremnts")
        choose_city = input(f'There are {length} you can choose. They are {unqiue_city}. So what is your choice?')
        user_df = user_df.loc[user_df['city'] == choose_city]
        #print(user_df)
        tabel =user_df.to_html()
        choose_airport = user_df['airport'].tolist()[0]
        choose_datei= user_df['date'].tolist()[0]
        #print(user_df)
        table = user_df.to_html()
        lat = city_df.loc[city_df['city'] == choose_city]['lat'].tolist()[0]
        lng = city_df.loc[city_df['city'] == choose_city]['lng'].tolist()[0]
        website_weather =  f'http://forecast.weather.gov/MapClick.php?lat={lat}&lon={lng}'
        website_flight = f'https://www.kayak.com/flights/DTW-{choose_airport}/{choose_datei}?sort=bestflight_a'
    html_str = ticket(table,website_weather = website_weather, website_flight = website_flight)
file = open("templates/flight.html","w")
file.write(html_str)
file.close()

json_file = root.traverse()
with open("tree.json", "w") as json_f:
    json.dump(json_file, json_f, indent=2)
os.system("python3 website.py")

