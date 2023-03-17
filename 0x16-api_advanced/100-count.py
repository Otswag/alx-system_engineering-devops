#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """Recursively queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords.
    
    Args:
    subreddit (str): The name of the subreddit to search.
    word_list (list): A list of keywords to count.
    after (str): The token of the next page of results to fetch.
    word_count (dict): A dictionary to store the counts of each keyword.
    
    Returns:
    None
    """
    # Base case: If all pages have been fetched, print the sorted counts of keywords.
    if after == 'STOP':
        counts = [(k, v) for k, v in word_count.items()]
        counts.sort(key=lambda x: (-x[1], x[0]))
        for word, count in counts:
            print(f"{word}: {count}")
        return
    
    # Build the API request URL.
    base_url = "https://www.reddit.com"
    endpoint = f"/r/{subreddit}/hot.json"
    params = {"limit": 100}
    if after:
        params["after"] = after
    headers = {"User-Agent": "Mozilla/5.0"}
    url = base_url + endpoint
    
    # Send the API request.
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error {response.status_code}: Could not fetch data from {url}")
        return
    
    # Parse the response JSON and extract the titles.
    data = response.json()
    titles = [post["data"]["title"] for post in data["data"]["children"]]
    
    # Count the occurrences of each keyword in the titles.
    for title in titles:
        words = title.lower().split()
        for word in words:
            word = word.strip(".,?!-_:;")
            if word in word_list:
                word_count[word] = word_count.get(word, 0) + 1
    
    # Recursively call the function with the token of the next page of results.
    next_page = data["data"].get("after")
    count_words(subreddit, word_list, next_page, word_count)
