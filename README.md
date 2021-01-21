# Book recommendation system

This repository shows all the code necessary to build an engine to recommend books based on similar summaries. 
Details about the project can be found in [this article](https://yan-gobeil.medium.com/how-simple-is-it-to-build-an-end-to-end-item-based-recommender-system-90f6d959e7c2) 
and the app has been released on [heroku](https://recommending-books.herokuapp.com/)
and is available on [RapidAPI](https://rapidapi.com/yangobeil/api/recommending-books).

The notebook `data.ipynb` contains the code used to scrape book data from [leslibraires.com](leslibraires.com) and
to encode all the summaries into vectors using Google's Universal Sentence Encoder. The vectors are used to find
similarities between books.

The recommendations found are then made available using a flask app in `app.py`. A part of the app is a web interface 
and the rest is a REST api. The api has been released on [RapidAPI]().

The final data with the recommendations is saved in `books.pkl`.

## Requirements

All the code is written in python 3.7 and the following packages are used:
- tensorflow-hub
- tensorflow-text
- scikit-learn
- numpy
- flask
- beautifulsoup4
- requests
- gunicorn