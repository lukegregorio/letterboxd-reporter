from bs4 import BeautifulSoup
import requests


def get_user_films(user_url):
    # get all pages of user films
    user_films_pages = get_user_films_pages(user_url)

    # store film url and rating
    film_data = {}

    for user_film_page in user_films_pages:

        response = requests.get(user_film_page)
        soup = BeautifulSoup(response.content, "html.parser")

        film_poster_soups = soup.find_all("li", {"class": "poster-container"})

        for film_poster in film_poster_soups:

            film = get_film_info_poster(film_poster)
            film_data.update(film)

    return film_data


def get_user_films_pages(user_url):

    response = requests.get(user_url)
    soup = BeautifulSoup(response.content, "html.parser")

    page_links = soup.select(".paginate-pages a")

    if len(page_links) == 0:
        # if there is only one page
        page_urls = [user_url]
    else:
        last_page_number = int(page_links[-1].text)
        page_urls = [
            user_url + f"page/{page_number}/"
            for page_number in range(1, last_page_number + 1)
        ]

    return page_urls


def get_film_info_poster(poster_soup):
    # get title
    div = poster_soup.find("div", class_="linked-film-poster")
    title = div.find("img").get("alt")

    # get rating of film
    film_rating = get_rating(poster_soup)

    film = {title: {"user_rating": film_rating}}

    return film


def get_rating(film_soup):

    rating_span = film_soup.find("span", class_="rating")
    # check if rating is available
    if rating_span:
        # get rating
        class_attribute = rating_span["class"]
        for attribute in class_attribute:
            if "rated-" in attribute:
                film_rating = (
                    int(attribute.split("rated-")[-1]) / 2
                )  # convert to 5 star scale from 10 star scale
    else:
        film_rating = None

    return film_rating


if __name__ == "__main__":
    user_url = "https://letterboxd.com/gregs_pictures/films/"
    user_films = get_user_films(user_url)
    print(user_films)
