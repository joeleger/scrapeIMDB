# scrapeIMDB
App to demo imdbpy package in a flask web app. This application scrapes user's file system for media content (vers. 1 is film) and adds the content
to a database. Files are parsed for a title and year and a query is sent to imdb via imdbpy package. We obtain an imdb_id for the movie and store in the 
database various attributes about the film, namely:
    imdb_id
    file_path
    title
    year
    genre
    rating
    actors
    directors
    writers
    plot
    runtime
    poster_url

Goal is to add more user input configuration.
There is a configuration class called Config. Set your file locations that you would like to scrape in this class. 
