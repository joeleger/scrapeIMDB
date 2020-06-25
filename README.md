# scrapeIMDB
App to demo imdbpy package in a flask web app. This application scrapes user's file system for media content (vers. 1 is film) and adds the content
to a database. Files are parsed for a title and year and a query is sent to imdb via imdbpy package. We obtain an imdb_id for the movie and store in the 
database various attributes about the film, namely:
- *imdb_id*
- *file_path*
- *title*
- *year*
- *genre*
- *rating*
- *actors*
- *directors*
- *writers*
- *plot*
- *runtime*
- *poster_url*

Goal is to add more user input configuration.
There is a configuration class called Config. Set your file locations that you would like to scrape in this class. 

### Requirements:
File types: We use the HTML <video> element to render video on a web page. This HTML element will render the following film types:
1. **MP4**
2. **WEBM**
3. **OGG** 

 We recommend that you use the above file types only.
 

### Naming convention for motion picture files.
The file name is required to be in the following format:
    *Title of movie* + *space(year).extension*
- Example
  *Once Upon a Time... In Hollywood*  The file name should be set as follows:
- **Once Upon a Time... In Hollywood (2019).mp4**

I natively support .mp4, webm and ogg extensions, but with future parameterized configuration you will be able to extend this.
Recently it is apparent that Chromium does not consistently render video files, namely mp4. This resulted in a downgrade 
to google chrome which solved the issue. I have never come across an ogg container containing video. Usually mp4 or mkv formats. 
I typically like mkv over mp4, but because of the limitation of the video tag and lack of support for mkv I have settled 
on mp4. I am testing webm to see how this container renders under various browsers that I normally use, Chrome, Opera and Edge. Edge does not
have support for webm however Opera and Chrome do. I converted a video from mp4 to webm with Handrake. My observations are that the time to 
convert the video was three times longer and the file size is twice as large. So far I am not a big fan of this format. 

The inspiration and source examples that embody much of this much thanks to Corey Shafer https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g, 
Miguel Grinberg https://blog.miguelgrinberg.com/index, the *imdbpy* package at https://imdbpy.github.io/ 
and the flask, python community for there generous knowledge sharing.
