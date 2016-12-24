import fresh_tomatoes
import media

fight_club = media.Movie("Fight Club",
                        "https://goo.gl/4gCW02",
                        "https://youtu.be/BdJKm16Co6M")

pulp_fiction = media.Movie("Pulp Fiction",
                        "https://goo.gl/pfb3iH",
                        "https://youtu.be/s7EdQ4FqbhY")

inglourious_basterds = media.Movie("Inglorious Basterds",
                        "https://goo.gl/2OxcBD",
                        "https://youtu.be/6AtLlVNsuAc")

seven = media.Movie("Se7en",
                        "https://goo.gl/P00xJc",
                        "https://youtu.be/znmZoVkCjpI")

green_mile = media.Movie("The Green Mile",
                        "https://goo.gl/1LSsH5",
                        "https://youtu.be/ctRK-4Vt7dA")

silence_of_lambs = media.Movie("The Silence of the Lambs",
                        "https://goo.gl/zNUG35",
                        "https://youtu.be/RuX2MQeb8UM")

schindlers_list = media.Movie("Schindler's List",
                        "https://goo.gl/Pa7ZUw",
                        "https://youtu.be/JdRGC-w9syA")

the_godfather = media.Movie("The Godfather",
                        "https://goo.gl/UD98t2",
                        "https://youtu.be/sY1S34973zA")
			
shawshank = media.Movie("The Shawshank Redemption",
                        "https://goo.gl/i6veIJ",
                        "https://youtu.be/NmzuHjWmXOc")			
			

movies = [fight_club, pulp_fiction, inglourious_basterds, seven, green_mile, 
silence_of_lambs, schindlers_list, the_godfather, shawshank]
fresh_tomatoes.open_movies_page(movies)
