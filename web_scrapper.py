#  make sure you have installed the below packages and libs before running the code :)
from bs4 import BeautifulSoup
import requests
import re
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pprint
PATH = os.getcwd()
DATA_PATH=PATH+ "/data"
if os.path.exists(DATA_PATH):
   os.rmdir(DATA_PATH)
os.makedirs(DATA_PATH)
def read_sentences_from_file(file_path):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
      for line in file:

        sentences.append(line.strip())  
    return sentences
def similarity(sentence1, sentence2):
    words1 = set(sentence1.lower().split())
    words2 = set()
    csentence2 = re.sub(r'[^\w\s]', '', sentence2)
    words2 = set([w.lower() for w in csentence2.split() if w not in stop_words and w.isalnum()])
    shared_words = words1.intersection(words2)
    if len(shared_words) >= 5:
      return True
    return False
print("\n\nTOPIC: BEST MOVIES 2024 \nWebsite: The Week & IMDB(for some facts)")
print("\nLETS START SCRAPPING THE WEB\n\n!!!Please be paitent each process takes time!!!\n\n")
starter_url = "https://theweek.com/culture-life/film/2024-film-releases-most-anticipated-new-movies"
r = requests.get(starter_url)
data = r.text
soup = BeautifulSoup(data, "html.parser")
movies_list = soup.find_all(class_='article-body__section')
body_tag = soup.find('div', class_="article__body")
raw_text = body_tag.get_text().lower().replace("\n", "")
main_url_text=sent_tokenize(raw_text)
urls=[]
for p in body_tag.find_all('p'):
  for l in p.find_all('a'):
    urls.append(l.get('href'))
urls = sorted(urls)
print(f"Got {len(urls)} URLs, some of them are: ")
print(urls[:5])
clean_text=[]
for i in range(len(urls)):
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
  req = requests.get(urls[i], headers=headers)
  soup = BeautifulSoup(req.text, "html.parser")
  if soup.find('main'):
    data = soup.find('main').text.lower().replace("\n", "").replace("\t", "")
    clean_text.append(data)
    FILE_PATH=DATA_PATH+'/filename{0}.txt'.format(i)
    with open(FILE_PATH, 'w', encoding='utf-8') as output:
      output.write('\n'.join(data.split('.')))
    # with open('urls.txt', 'a') as u:
    #   u.write('\n'+urls[i]+' --> filename{0} '.format(i))
with open(DATA_PATH+'/filename.txt', 'w', encoding='utf-8') as output:
  output.write('\n'.join(main_url_text))
with open(DATA_PATH+"/filename33.txt", 'r', encoding='utf-8') as file:
  txt=file.read()
with open(DATA_PATH+"/filename33.txt", 'w', encoding='utf-8') as file:
  file.write(txt.replace('.','\n'))
print("\nData Extracted from the urls and stored in the same folder")
# print("URL to file mapping stored in urls.txt file")
cleaned=[]
for ct in clean_text:
  dct=[]
  words = word_tokenize(ct)
  for w in words:
    if w not in stop_words and w.isalnum():
      dct.append(lemmatizer.lemmatize(w))
#   print(len(words),">>",len(dct))
  cleaned.append(' '.join(dct))
print("Cleaned the text for geting important words")
names=[]
for m in movies_list:
  if m.text not in names:
    names.append(m.text.replace(":", '').replace("-", ' '))
names[7], names[12] = names[12], names[7]
cleaned=names+cleaned+names
tfidf_vectorizer = TfidfVectorizer(max_features=15)
tfidf_matrix = tfidf_vectorizer.fit_transform(names+cleaned)
feature_names = tfidf_vectorizer.get_feature_names_out()
important_terms = set()
for i in tfidf_matrix.indices:
  important_terms.add(feature_names[i])
print("\nHere's the list of 10 important words from the text")
print(sorted(list(important_terms)))
print("\nWe are going with the movie titles as it organizes the knowledge base neatly")
print("\nNow lets get some facts form the imdb site that will help in filtering info from websites that we scraped eariler")
imdb=["tt15239678", "tt19760052", "tt21064584","tt7160372","tt21192142","tt14849194","tt16277242"]
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
facts={
    "title": [],
    "starcast": [],
    "directors": [],
    "writers": [],
    "rated": [],
    "runtime": [],
    "year":[],
    "imdb": [],
}
for i in range(len(imdb)):
  url="https://www.imdb.com/title/{0}/".format(imdb[i])
  r = requests.get(url,headers=headers)
  data = r.text
  soup = BeautifulSoup(data, "html.parser")
  body_tag = soup.find('div', class_="bdjVSf")
  facts['title'].append(body_tag.span.text)
  arr = body_tag.ul.find_all('li')
  facts['year'].append(arr[0].text)
  facts['rated'].append(arr[1].text)
  facts['runtime'].append(arr[2].text)
  facts['imdb'].append(body_tag.find('span', class_="ipc-btn__text").span.text)
  data = soup.find('div', class_="rbXFE") .find_all('ul', class_='ipc-inline-list')
  directors = [tag.text for tag in data[0].find_all('a')]
  writers = [tag.text for tag in data[1].find_all('a')]
  stars = [tag.text for tag in data[2].find_all('a')]
  facts['directors'].append(directors)
  facts['writers'].append(writers)
  facts['starcast'].append(stars)
print("\nLets add these facts to the database/ knowledge base")
database = {}
match_sentence={}
for i in range(len(facts['title'])):
    title = facts['title'][i].replace(":", '')
    starcast = ', '.join(facts['starcast'][i])
    directors = ', '.join(facts['directors'][i])
    writers = ', '.join(facts['writers'][i])
    rated = facts['rated'][i]
    runtime = facts['runtime'][i]
    year = facts['year'][i]
    imdb_rating = facts['imdb'][i]
    match_sentence[title] =f"{title} {starcast} {directors} {writers}".replace(',', '')
    sentences = [
        f"The starcast of the movie {title} includes {starcast}.",
        f"The movie {title} is directed by {directors}.",
        f"The writers of the movie {title} are {writers}.",
        f"The movie {title} is rated {rated}.",
        f"The runtime of the movie {title} is {runtime}.",
        f"The movie {title} was released in {year}.",
        f"The IMDb rating of the movie {title} is {imdb_rating}."
    ]    
    database[title] = sentences
print("\n\nDatabase created successfully.")
print("Now Lets Add Content to the database")
match_sentence['Other movie reviews']='Gladiator 2 Spider Man Beyond the Spider Verse Beetlejuice 2 Mufasa The Lion King Joker Folie à Deux Alien Romulus The Garfield Movie IF'
files = sorted(os.listdir(DATA_PATH))
for filename in files:
  if filename[-4:] == ".txt":
    sentences=read_sentences_from_file(DATA_PATH+'/'+filename)
    for input_sentence in sentences:
      fg=False
      for movie_title, movie_sentences in database.items():
        if similarity(match_sentence[movie_title], input_sentence):
          input_sentence = re.sub(r'[^\w\s.,!?]', '', input_sentence)
          input_sentence = re.sub(r'\s+', ' ', input_sentence)
          database[movie_title].append(input_sentence.strip())
          fg=True
          break
      if fg:
        break
database['Other movie reviews']=[]
database['movies list']=f"These are all the best movies of 2024 according to the \"wired\" - {', '.join(names)}"
for filename in files:
  if filename[-4:] == ".txt":
    sentences=read_sentences_from_file(DATA_PATH+'/'+filename)
    for input_sentence in sentences:
      if similarity(match_sentence['Other movie reviews'], input_sentence):
        input_sentence = re.sub(r'[^\w\s.,!?]', '', input_sentence)
        input_sentence = re.sub(r'\s+', ' ', input_sentence)
        database['Other movie reviews'].append(input_sentence.strip())
print("\n\n\nFinally, after a long period  of processing...")
print("Dumping the database into pickle file for chatbot usage")
print("Here is your Movie Database: \n")
pprint.pprint(database)
with open('database.pkl', 'wb') as db:
  pickle.dump(database, db)