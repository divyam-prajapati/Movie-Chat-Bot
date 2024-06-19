# Movie-Chat-Bot

# PROJECT 1
## Rules-Based Chatbot for 2024 Movie Information

This project is a rules-based chatbot that provides information about the most anticipated movies of 2024. The chatbot utilizes a knowledge base created by scraping relevant data from various websites, primarily "The Week" and IMDb.

### Prerequisites

Before running the code, ensure that you have the following dependencies and libraries installed:

- Python 3.x
- beautifulsoup4
- requests
- re
- os
- nltk
- scikit-learn
- pickle
- difflib
- json

You can install these dependencies using pip:

```bash
pip install beautifulsoup4 requests nltk scikit-learn difflib
```

### Web Crawler

To create the knowledge base by scraping the web, run the following command:
```bash
python web_crawler.py
```
This script will scrape the necessary information from the websites, process the data, and create a knowledge base stored in a database.pkl file.

### Chatbot

To start the chatbot and interact with it, run the following command:
```bash
python chatbot.py
```
To exit the chatbot, simply type quit or exit.

# PROJECT 2
## Chatbot with encoder-decoder and attension mechanism
For details on the model and the approach please read this [report](https://github.com/divyam-prajapati/Movie-Chat-Bot/blob/main/DBP230000_PROJECT2_REPORT.pdf)

The Code is availabe in the [notebook](https://github.com/divyam-prajapati/Movie-Chat-Bot/blob/main/DBP230000_NLP_MovieBot.ipynb).
