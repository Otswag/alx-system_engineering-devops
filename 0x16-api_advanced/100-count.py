#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, counts={}):
    """ Base case: no more posts to fetch """
    if after == '':
        """ Sort the counts dictionary by count (descending) and word (ascending) """
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        """ Print the counts for each keyword """
        for word, count in sorted_counts:
            print(word + ':', count)
        return

    """ Fetch the next page of posts from the subreddit """
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100, 'after': after}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, params=params, headers=headers)

    """ Check for a valid response """
    if response.status_code != 200:
        print('Error:', response.status_code)
        return

    """ Parse the response JSON """
    data = response.json()
    posts = data['data']['children']

    """ Process each post """
    for post in posts:
        title = post['data']['title'].lower()
        """ Count the occurrences of each keyword in the title """
        for word in word_list:
            count = title.count(word.lower())
            if count > 0:
                """ Add the count to the counts dictionary """
                if word in counts:
                    counts[word] += count
                else:
                    counts[word] = count

    """ Recursively call the function with the after parameter set to the last post's ID """
    last_post_id = posts[-1]['data']['name']
    count_words(subreddit, word_list, after=last_post_id, counts=counts)
