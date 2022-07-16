from operator import indexOf
from pickle import FALSE
from sqlalchemy import true
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import matplotlib.pyplot as plt
import requests
import random
import spacy
import re

# function to print sentiments
# of the sentence.
#https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict

def year_api(year, Country=''):
    #https://api-ninjas.com/api/historicalevents
    text = year
    if Country:
        text2 = Country
    else:
        text2 = 'United States'
    api_url = 'https://api.api-ninjas.com/v1/historicalevents?text={}&year={}'.format(text2,text)
    response = requests.get(api_url, headers={'X-Api-Key': 'kdNf4ATih7ynuA5NrY7Wiw==BctHq5CL6xpjuPjj'})
    if response.status_code == requests.codes.ok:
        res_json = response.json()
        #print(res_json)
        #first five response
        paragraph = ""
        if len(res_json)>3:
            for num in range(0,4):
                paragraph = paragraph + res_json[num]['event'] + " \n"
        else:
            for num in range(0,len(res_json)):
                paragraph = paragraph + res_json[num]['event'] + " \n"
    else:
        print("Error:", response.status_code, response.text)
        return ""
    return paragraph

def famous_quote_api():
    #https://rapidapi.com/saicoder/api/famous-quotes4/
    url = "https://famous-quotes4.p.rapidapi.com/random"
    querystring = {"category":"all","count":"2"}
    headers = {
	    "X-RapidAPI-Key": "80ce0759c9mshe3ab43f2d0c7a14p1e9db2jsn89f2b419cb42",
	    "X-RapidAPI-Host": "famous-quotes4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)


def show_bar_chart(yr, yr_sent):
    #https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
    # x-coordinates of left sides of bars 
    left = [1, 2, 3, 4, 5]
    
    # heights of bars
    height = []
    for i in yr_sent:
        height.append(i['compound']*100)
    
    # labels for bars
    tick_label = yr
    
    # plotting a bar chart
    plt.bar(left, height, tick_label = tick_label,
            width = 0.8, color = ["red" if i <= 0 else "green" for i in height])
    
    plt.ylim(-100,100)

    # naming the x-axis
    plt.xlabel('Years')
    # naming the y-axis
    plt.ylabel('Percentage sentiment')
    # plot title
    plt.title('Sentiment from %s to %s' %(yr[0],yr[4]))
    
    # function to show the plot
    plt.show()

def Get_points(Guess, Score):
    if Guess < 0 and Score > 0:
        return 0
    elif Guess > 0 and Score < 0:
        return 0
    else:
        diff = abs(Guess - Score)
    points = 0
    if diff == 0:
        points = points + 90
    elif diff <= 5 and diff > 0:
        points = points + 70
    elif diff <= 15 and diff > 5:
        points = points + 50
    elif diff > 15 and diff <=35:
        points = points + 40
    elif diff > 35 and diff <=50:
            points = points + 30
    else:
        points = points + 10
    return points

def random_cntry_yr(input_cntry=""):
    r_list = []
    country = ""
    r1 = random.randint(0, 2)
        #United States 1900 - 2021
        #Russia 1990 - 2021
        #China 1950 - 2021
        #Japan 1960 - 2000
    c = ["China","United States","Japan"]
    if not input_cntry:
        country = c[r1]
    if country == c[0] or input_cntry == "China" or input_cntry == "c":
        #China 1950 - 2021
        r_list.append(random.randint(1950, 2021))
        r_list.append("China")
    if country == c[1] or input_cntry == "United States" or input_cntry == "u":
        #United States 1900 - 2021
        r_list.append(random.randint(1900, 2021))
        r_list.append("United States")
    if country == c[2] or input_cntry == "Japan" or input_cntry == "j":
        #Japan 1960 - 2000
        r_list.append(random.randint(1960, 2021))
        r_list.append("Japan")
    return r_list



#https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/
#Have Easy, Medium and Hard mode
#Easy -> first two letter
#Medium -> one letter
#Hard -> none
#default is GPE
def NER(sentence):
    GPE, PERSON, EVENT, NORP, ORG, LOC = False, False, False, False, False, False
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    Ent_map = {}
    #PERSON, NORP (nationalities, religious and political groups), FAC (buildings, airports etc.), ORG (organizations), 
    # GPE (countries, cities etc.), LOC (mountain ranges, water bodies etc.), PRODUCT (products), EVENT (event names), 
    # WORK_OF_ART (books, song titles), 
    #LAW (legal document titles), LANGUAGE (named languages), DATE, TIME, PERCENT, MONEY, QUANTITY, ORDINAL and CARDINAL.
    #print(ent.text, ent.start_char, ent.end_char, ent.label_)
    for ent in doc.ents:
        if ent.label_ == "GPE" and GPE == False:
            GPE = True
            Ent_map["GPE"] = str(ent.text)
            sentence = sentence.replace(str(ent.text), gen_blank(ent.end_char,ent.start_char,ent.text,"(GPE)"), 1)
        if ent.label_ == "PERSON" and PERSON == False:
            PERSON = True
            Ent_map["PERSON"] = str(ent.text)
            sentence = sentence.replace(str(ent.text),gen_blank(ent.end_char,ent.start_char,ent.text,"(PERSON)"), 1)
        if ent.label_ == "EVENT" and EVENT == False:
            EVENT = True
            Ent_map["EVENT"] = str(ent.text)
            sentence = sentence.replace(str(ent.text),gen_blank(ent.end_char,ent.start_char,ent.text,"(EVENT)"), 1) 
        """
        if ent.label_ == "NORP" and NORP == False:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            NORP = True
            Ent_map["NORP"] = str(ent.text)
            sentence = sentence.replace(str(ent.text),gen_blank(ent.end_char,ent.start_char,ent.text,"(NORP):"), 1)
        """
        if ent.label_ == "ORG" and ORG == False:
            ORG = True
            Ent_map["ORG"] = str(ent.text)
            sentence = sentence.replace(str(ent.text),gen_blank(ent.end_char,ent.start_char,ent.text,"(ORG)"), 1)
        if ent.label_ == "LOC" and LOC == False:
            LOC = True
            Ent_map["LOC"] = str(ent.text)
            sentence = sentence.replace(str(ent.text),gen_blank(ent.end_char,ent.start_char,ent.text,"(LOC)"), 1)
    r_list = []
    r_list.append(Ent_map)
    r_list.append(sentence)
    return r_list

def gen_blank(end, start, text, label):
    diff = int(end)-int(start)
    blank = "_" * diff
    #looks for the spaces in the text
    spaces = [i.start() for i in re.finditer(" ", text)]
    #includes the spaces inside the blank
    for ind in spaces:
        blank = blank[:ind] + " " + blank[ind+1:]
    blank = label + blank
    return blank
        
def guess_blank(map,ent,guess):
    for key in map:
        if key == ent:
            if pre_process(map[key]) == pre_process(guess):
                return True
    return False

def Look_for_key(map, element):
    for key in map:
        if key == element:
            return True
    return False

def pre_process(t):
    t = t.replace(" ", "")
    return re.sub(r'[^a-z\d ]',' ',t.lower())

def get_hint(map):
    ret_list = []
    ret_str = ""
    l = {}
    # for each key we split the values by spaces
    for key in map:
        l[key] = map[key].split(" ")
    
    for k in l:
        ret_str = ret_str + k + ": "
        for v in l[k]:
            ret_str = ret_str + v[0][0] + " "
            ret_str = ret_str + "_ " * int(len(v)-1)
            #"Total length: " + str(len(v)) + "characters"
        ret_str = ret_str + " "
        ret_list.append(ret_str)
        #default back to blank
        ret_str = ""
    return ret_list

def split_paragraph(par):
    l = par.split("\n")
    return l


# Driver code
# Make a guessing game with sentiment guesser -> closer you are the more points.
# store the values into a lreaderboard
if __name__ == "__main__" :
    #holds the list of years
    list_of_years = []
    #guess on the sentiment
    sent_guess = []
    year = input("Enter a year:")
    list_of_years.append(year)
    print(list_of_years)
    years_sentiment = []
    for yr in list_of_years:
        sentence = year_api(str(yr))
        years_sentiment.append(sentiment_scores(sentence))
    print(sentence)
    NER(sentence)
    
    #make a graph of 5 years of positive graph sentiment

    #holder for event

    #TODO: add pasring for verbs/adj?? https://www.nltk.org/book/ch05.html
   
    #SPeech to text? https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/
   
    #Include an text mode
    #Include Twitter API? or FAmous Quote API or Twitch API

    #get the time of the tweet -> store into database -> mood of tweets morning, afternoon, and dinner
    #https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/?ref=lbp

    #include language check https://pypi.org/project/language-check/

