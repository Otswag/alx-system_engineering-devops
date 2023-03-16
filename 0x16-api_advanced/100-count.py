#!/usr/bin/python3
import praw

def count_words(subreddit, word_list, counts=None):
    if counts is None:
        counts = {}
    reddit = praw.Reddit(client_id='your_client_id',
                         client_secret='your_client_secret',
                         user_agent='your_user_agent')
    try:
        hot_posts = reddit.subreddit(subreddit).hot(limit=10)
    except praw.exceptions.Redirect:
        return
    for post in hot_posts:
        words = post.title.lower().split()
        for word in word_list:
            if word.lower() in words:
                if word.lower() in counts:
                    counts[word.lower()] += words.count(word.lower())
                else:
                    counts[word.lower()] = words.count(word.lower())
    if word_list:
        count_words(subreddit, word_list[:-1], counts)
    else:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(word, count)
