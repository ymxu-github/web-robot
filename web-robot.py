# Author: ymxu
# Created: 2026/9/30 14:17
# File: web-robot.py
import re

import requests
import csv
from lxml import html

# Constants
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL_1 =f"{TMDB_BASE_URL}/movie/top-rated" # Top-rated movies URL (first page)
TMDB_TOP_URL_2 =f"{TMDB_BASE_URL}/discover/movie/items" # Top-rated movies URL (page two onward)
MOVIE_LIST_CSV_FILE = "csv_data/movies.csv"

def get_item_value(document, xpath):
    """Return the first value from the XPath result, or an empty string if none exists."""
    results = document.xpath(xpath)
    return results[0].strip() if results else ""

# Format the release date.
def format_release_date(release_date):
    match =  re.search(r"(\d{4}-\d{2}-\d{2})", release_date)
    if match:
        return match.group()
    return ""

# Format the runtime as a number of minutes.
def format_runtime(runtime):
    h_match = re.search(r"(\d+)h", runtime)
    m_match = re.search(r"(\d+)m", runtime)

    total_minutes = 0
    if h_match:
        total_minutes += int(h_match.group(1)) * 60
    if m_match:
        total_minutes += int(m_match.group(1))

    return total_minutes

# Get detailed information about a movie.
def get_movie_info(movie_info_url):
    # Request the movie details page.
    response = requests.get(movie_info_url, timeout=60)
    document = html.fromstring(response.text)

    # Movie title
    title = get_item_value(document, '//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    # Release year
    year = get_item_value(document, '//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
    # Language
    language = get_item_value(document, '//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    # Overview
    overview = get_item_value(document, '//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')
    # Tagline
    tagline = get_item_value(document, '//h3[@class="tagline"]/text()')
    # Release date
    release_date = get_item_value(document, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')
    # Runtime
    runtime = get_item_value(document, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
    # Genres
    genres = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
    # User score
    user_score = get_item_value(document, '//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
    # Directors and screenwriters
    directors = []
    screenwriters = []
    peoples = document.xpath('//ol[@class="people no_image"]/li')
    for person in peoples:
        character = person.xpath('./p[@class="character"]/text()')
        if character and "Director" in character[0]:
            director_name = person.xpath('./p[1]/a/text()')
            directors.append(director_name[0].strip() if director_name else "")
        if character and any(role in character[0] for role in ("Writer", "Screenplay")):
            screenwriter_name = person.xpath('./p[1]/a/text()')
            if screenwriter_name:
                screenwriters.append(screenwriter_name[0].strip())

    movie_info = {
        "Movie Title": title,
        "Release Year": year.replace("(", "").replace(")", ""),
        "Tagline": tagline,
        "Release Date": format_release_date(release_date),
        "Runtime (minutes)": format_runtime(runtime),
        "Language": language,
        "Genres": ','.join(genres) if genres else "",
        "User Score": user_score,
        "Director": ','.join(directors) if directors else "",
        "Screenwriter": ','.join(screenwriters) if screenwriters else "",
        "Overview": overview
    }

    print(f"Retrieved movie information: {movie_info}")

    return movie_info

# Save movie information to a CSV file.
def save_all_movies(all_movies):
    with open(MOVIE_LIST_CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Movie Title", "Release Year", "Tagline", "Release Date", "Runtime (minutes)", "Language", "Genres", "User Score", "Director", "Screenwriter", "Overview"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_movies)


# Main function containing the core workflow.
def main():
    # Fetch the top-rated movie listings from the first five pages.
    all_movies = []
    for page_num in range(1, 6):
        # 1. Send an HTTP request to retrieve the top-rated movie listings.
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_1, timeout=60)
        else:
            data = f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-01&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated"
            response = requests.post(TMDB_TOP_URL_2, data=data, timeout=60)

        # 2. Parse the HTML and extract the movie list.
        document = html.fromstring(response.text)
        movie_list = document.xpath('//*[@class="media-list-results contents"]/div')

        # 3. Iterate over the movie list and retrieve each movie's details.
        for movie in movie_list:
            movie_urls = movie.xpath('./div/div/a/@href')
            if movie_urls:
                movie_info_url = f"{TMDB_BASE_URL}{movie_urls[0]}"
                # Request the movie details page.
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)

    # 4. Save the movie information to a CSV file.
    print("Saving movie information to CSV...")
    save_all_movies(all_movies)

if __name__ == "__main__":
    main()