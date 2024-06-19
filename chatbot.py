import re
import pickle
import pprint
import random
import os
from difflib import SequenceMatcher
import json

def create_user_model():
    user_model = {
        "name": [],
        "likes": [],
        "dislikes": []
    }
    return user_model

def save_user_model(user_model, filename):
    user_model_filename = "user_model.json"
    if os.path.exists(user_model_filename):
        with open(filename, 'r') as f:
            user_model = json.load(f)
    with open(filename, 'w') as f:
        json.dump(user_model, f)

with open('database.pkl', 'rb') as db:
    movies_db = pickle.load(db)

# pprint.pprint(movies_db)

def filter_question(querry):
    if re.search(r'\b(cast|actors|stars)\b', querry):
        return 0
    elif re.search(r'\b(direction|directors|directed)\b', querry):
        return 1
    elif re.search(r'\b(writers|authors|written|writer)\b', querry):
        return 2
    elif re.search(r'\b(rated|audiance|age|category)\b', querry):
        return 3
    elif re.search(r'\b(run|time|run time|runtime|duration)\b', querry):
        return 4
    elif re.search(r'\b(year|release)\b', querry):
        return 5
    elif re.search(r'\b(imdb|score|rating)\b', querry):
        return 6 
    else:
        return None
    
def filter_movie(querry):
    if re.search(r'\b(dune|dune part two)\b', querry):
        return "Dune Part Two"
    elif re.search(r'\b(taste|things|taste of things)\b', querry):
        return "The Taste of Things"
    elif re.search(r'\b(iron|claw|iron claw)\b', querry):
        return "The Iron Claw"
    elif re.search(r'\b(zone|intrest|zone of interest)\b', querry):
        return "The Zone of Interest"
    elif re.search(r'\b(society|snow|society of the snow)\b', querry):
        return "Society of the Snow"
    elif re.search(r'\b(all of Us|strangers|all of Us strangers)\b', querry):
        return "All of Us Strangers"
    elif re.search(r'\b(holdovers|hold)\b', querry):
        return "The Holdovers"
    else:
        return None

def similarity(query, movie_title):
    max_similarity = 0
    most_similar_index = -1
    for i in range(7,len(movies_db[movie_title])):
        similarity_ratio = SequenceMatcher(None, query, movies_db[movie_title][i]).ratio()
        if similarity_ratio > max_similarity:
            max_similarity = similarity_ratio
            most_similar_index = i
    return most_similar_index

print("Bot> Hello, Welcome to the movie bot!")
print("Bot> Whats you name: ")
name=input(" You> ")
user_model_filename = "user_model.json"
if os.path.exists(user_model_filename):
    with open(user_model_filename, 'r') as f:
        user_model = json.load(f)
    if name in user_model["name"]:
        print(f"Bot> Welcome Back!, {name}")
        print(f"Bot> I remmembered you prefrences {user_model['likes'][user_model['name'].index(name)]}")

else:
    user_model = create_user_model()
    print("Bot> Welcome to the movie bot, I can answer you questions on 2024 movies :)")
    user_model["name"].append(name)
    print("Bot> Here are some introductory questions to know you better... :D")
    print("Bot> What kind of movies do you like")
    user_model["likes"].append(input(" You> "))
    print("Bot> What are some things you want me to avoid")
    user_model["dislikes"].append(input(" You> "))
    save_user_model(user_model, user_model_filename)
    

print("Bot> How can I help you today?")
while True:
    querry=input(" You> ")
    querry = querry.lower()
    movie=filter_movie(querry)
    question=filter_question(querry) 
    if re.search(r'\b(hi|hello|good|how are you|whatsup|hey)\b', querry):
        print("Bot> Hello! I am a movie bot, how can I help you today :)")
    elif re.search(r'\b(quit|exit|bye)\b', querry):
        print(f"Bot> Goodbye! See you soon {name} :(\n")
        break
    elif re.search(r'\b(list|top|movies|best|others)\b', querry):
        print(f"Bot> {movies_db["movies list"]}")
    elif re.search(r'\b(story|plot|description|storyline|reviews|crowd|talk|review|opinion)\b', querry):
        if movie is None:
            print("Bot> Yep, for which movie would you like too see?")
            querry=input(" You> ")
            querry = querry.lower()
            movie=filter_movie(querry)
        print(f"Bot> {movies_db[movie][similarity(querry, movie)]}")    
    elif movie is not None and question is not None:    
        print(f"Bot> {movies_db[movie][question]}")
    elif movie is not None and question is None:
        print("Bot> Yes! What do you want to know about this movie?")
        querry=input(" You> ")
        querry = querry.lower()
        question=filter_question(querry)
        print(f"Bot> {movies_db[movie][question]}")
    elif movie is None and question is not None:
        print("Bot> Sure, for which movie would you like this information?")
        querry=input(" You> ")
        querry = querry.lower()
        movie=filter_movie(querry)
        print(f"Bot> {movies_db[movie][question]}")
    else:
        print("Bot> Please type a valid request. I am a humble movie bot! :)")
