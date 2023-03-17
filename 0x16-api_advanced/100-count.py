#!/usr/bin/python3
import requests
import re

def count_words(subreddit, word_list, after=None, counts=None):
    # Initialize counts dictionary on first call
    if counts is None:
        counts = {}

    # Make API request
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": "100", "after": after}
    response = requests.get(url, headers=headers, params=params)

    # Handle invalid subreddit or no matching posts
    if response.status_code != 200:
        return

    # Parse titles for each post and update counts dictionary
    data = response.json()["data"]
    for child in data["children"]:
        title = child["data"]["title"].lower()
        for word in word_list:
            # Ensure exact word match and not partial matches like java.
            match = re.findall(rf"\b{word}\b", title)
            if match:
                counts[word] = counts.get(word, 0) + len(match)

    # Recursively call function to get next page of results
    if data["after"] is not None:
        count_words(subreddit, word_list, data["after"], counts)
    else:
        # Sort and print results
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
