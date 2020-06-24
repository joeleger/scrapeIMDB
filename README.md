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

Requirements:
File types: We use the HTML <video> element to render video on a web page. This HTML element will render the following film types:
MP4. WEBM and OGG.
Naming convention for motion picture files.
The file name is required to be in the following format:
    Title of movie + space(year).extension
    example - Once Upon a Time... In Hollywood should be named as follows:
        Once Upon a Time... In Hollywood (2019).mp4
We natively support .mp4, webm and ogg extensions, but with future parameterized configuration you will be able to extend this.
