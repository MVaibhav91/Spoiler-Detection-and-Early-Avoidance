from bs4 import BeautifulSoup
import requests
from spoileravanish import is_spoiler


base_link = "https://www.imdb.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

# returns {status, title, poster, rating(1,2), plot}
def getMovie(movie_id):
    fetch_movie_details = base_link + "title/" + movie_id
    response = requests.get(fetch_movie_details, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = {'status': False}

    print("\nInside getMovie function\n")
    try:
        title = soup.find("h1", {"data-testid": "hero-title-block__title"}).text
        result['title'] = title
        print("\n"+title+"\n")
        try:
            result['poster'] = soup.find("img", {'class': 'ipc-image', 'loading': 'eager'})['src']
        except:
            result['poster'] = None
        try:
            rating = soup.find("span", {'class': "sc-7ab21ed2-1 jGRxWM"}).text
            raters = soup.find("div", {'class': "sc-7ab21ed2-3 dPVcnq"})
            if raters:
                raters = raters.text
            result['rating'] = (rating,raters)
        except:
            result['rating'] = None
        try:
            result['plot'] = soup.find("span", {'data-testid': 'plot-xl'}).text
        except:
            result['plot'] = None

        return result
    except:
        return result
        


def fetchReviewsAPI(movie_id):
    fetch_review_details = base_link + "title/" + movie_id + "/reviews"
    response = requests.get(fetch_review_details, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    result = {'status': False}

    try:
        search_content = soup.find("div", class_="lister-list")
        search_content = search_content.find_all("div", class_="text")
        reviews = []
        for i in search_content:
            review = i.text
            stat = False
            try:
                stat = is_spoiler(review)
                reviews.append((review,stat))
            except:
                reviews.append((review,stat))
            # reviews.append(review)
        result['status'] = True
        result['reviews'] = reviews
        return result
    except Exception as e:
        return {'status': False, 'error': e}

# def fetchMovieAPI(movie_id):
#     fetch_query_details = base_link + "title/" + movie_id
#     response = requests.get(fetch_query_details, headers=headers, verify=False)
#     soup = BeautifulSoup(response.content, "html.parser")
#     result = {'status': False}

#     try:
#         title = soup.find("h1", {"data-testid": "hero-title-block__title"}).text
#         result['title'] = title
#         search_content = soup.find("div", class_="sc-7643a8e3-2 ebKPVC")
#         if search_content is None:
#             search_content = soup.find("div", class_="sc-7643a8e3-6 bunqBa")
#         try:
#             poster = search_content.find("img", class_="ipc-image")["src"]
#             print("----",poster,"----")
#             result['poster'] = poster
#         except:
#             pass
#         try:
#             summary = soup.find("div", {"data-testid": "plot"}).find("span", {"role": "presentation"}).text
#             result['summary'] = summary
#         except:
#             pass
#         try:
#             all_genres = soup.find("div", class_="ipc-chip-list__scroller").find_all("span",class_="ipc-chip__text")
#             genres = []
#             for genre in all_genres:
#                 genres.append(genre.text)
#             result['genres'] = genres
#         except:
#             pass
#         result['status'] = True
#         # for k,v in result.keys:
#             # print(k,": -->",v)
#         return result
#     except Exception as e:
#         return {'status': False, 'error': e}


def fetchQuery(query):
    fetch_query_details = base_link + "search/title/?title=" + query
    response = requests.get(fetch_query_details)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        search_content = soup.find("div", class_="lister-list")
        search_content = search_content.find_all("div", class_="lister-item")
        search_result = []
        for movie in search_content:
            image = movie.find("div",class_="lister-item-image").find("img")
            title = image["alt"]
            movie_id = image["data-tconst"]
            image = image["loadlate"]
            year = movie.find("span",class_="lister-item-year").text
            search_result.append((movie_id,title,year,image))
        
        return {"status": True, "result": search_result}
    except Exception as e:
        return {'status': False, 'error': e}

# class Movie:
#     def __init__(self, id, )


# SpoilerDetection - v1.5

def fetch_query(title):
    '''
    SpoilerDetection - v1.5
    Search movies based on 'title' 
    '''
    fetch_query_details = base_link + "search/title/?title=" + title
    response = requests.get(fetch_query_details)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        search_content = soup.find("div", class_="lister-list")
        search_content = search_content.find_all("div", class_="lister-item")
        
        result_set = []
        
        for movie in search_content:
            movie_set = {
                'id': None,
                'title': None,
                'year': None,
                'img': None
            }
            image = movie.find("div",class_="lister-item-image").find("img")
           
            movie_set['id'] = image["data-tconst"]
            movie_set['title'] = image["alt"]
            movie_set['img'] = image["loadlate"]
            movie_set['year'] = movie.find("span",class_="lister-item-year").text
            
            result_set.append(movie_set)
        
        return {
            'status': True,
            'query': title,
            'movie_counts': len(result_set),
            'movie_set': result_set
        }
    
    except Exception as e:
        return {
            'status': False,
            'error': e
        }



def get_movie(id):
    '''
    SpoilerDetection - v1.5
    Get reviews by 'movie_id'
    '''
    fetch_review_details = base_link + "title/" + id + "/reviews"
    response = requests.get(fetch_review_details, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        search_content = soup.find("div", class_="lister-list")
        search_content = search_content.find_all("div", class_="text")
        
        reviews = []
        spoilers = 0

        for i in search_content:
            review = i.text
            stat = False
            try:
                stat = is_spoiler(review)
                if stat:
                    spoilers += 1
                reviews.append({
                    'review': review,
                    'is_spoiler': stat
                })
            except:
                reviews.append({
                    'review': review,
                    'is_spoiler': stat
                })
    
        return {
            'status': True,
            'total': len(reviews),
            'spoilers': spoilers,
            'reviews': reviews
        }
    
    except Exception as e:
        return {
            'status': False, 
            'error': e
        }
