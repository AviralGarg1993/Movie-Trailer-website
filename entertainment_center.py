import fresh_tomatoes
import media
import requests
import StringIO

#fight_club = media.Movie("Fight Club")

#shawshank = media.Movie("The Shawshank Redemption")

r = requests.get('https://raw.githubusercontent.com/AviralGarg1993/Movie-Trailer-website/movieList/movieList.txt')
print r.content

movies = []

s = StringIO.StringIO(r.content)
for line in s:
    eval('movies.append(media.Movie("' + line.rstrip().title() + '"))')
    
    

fresh_tomatoes.open_movies_page(movies)
