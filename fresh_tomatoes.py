import webbrowser
import os
import re
import httplib
import json
from StringIO import StringIO

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
	  /*  background-image: url("https://static.pexels.com/photos/142928/pexels-photo-142928.jpeg");
	    background-repeat: repeat-y;
	    background-size: 100%;*/
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'https://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
	  <a href="https://github.com/AviralGarg1993/Movie-Trailer-website/edit/movieList/movieList.txt">.</a>
        </div>
      </div>
    </div>
    <p>Click the poster to watch trailer and click the "Watch movie" to be redirected to online movie link!</p>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img class="img-rounded" src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
    <a data-toggle="modal" target="_blank" href="{movie_link}" class="btn btn-primary" role="button">Watch Movie</a>
    <p><img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/New-imdb-logo.png" height=20px></img> <strong>{IMDBscore}</strong></p>
</div>
'''




# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBKF6SlnLWiPjWJWZFDBmrQcffD_1QGsNA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options + " trailer",
    part="id,snippet"
  ).execute()
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
	id = search_result["id"]["videoId"]
	return id

				    
				    
  
def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    counter = 0
    for movie in movies:
	print len(movies)- counter
	counter+=1
	movie_string = movie.title.translate(None, '\'')
	movie_string = movie_string.replace(' ', '-').lower()
	
	conn = httplib.HTTPSConnection("api.themoviedb.org")
	
	payload = "{}"

	conn.request("GET", "/3/search/movie?include_adult=false&page=1&query=" + movie_string + "&language=en-US&api_key=2ff2bbb8754c9814b0c7c5d861228792", payload)

	response = conn.getresponse()
	data = response.read()
	#io = StringIO(data)
	json_data = json.loads(data)
	base_url = 'http://image.tmdb.org/t/p/'
	file_size = 'w500'
	poster_path = json_data['results'][0]['poster_path']
	img_URL = base_url + file_size + poster_path
	score = json_data['results'][0]['vote_average']

	
        
	
	#Get putlocker link
	
	movie_link='http://putlockers.ch/watch-'+ movie_string +'-online-free-putlocker.html'
	
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=img_URL,
            trailer_youtube_id=youtube_search(movie.title),
	    movie_link=movie_link,
	    IMDBscore=score
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
