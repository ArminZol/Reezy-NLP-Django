import praw
from saver import save

user_agent = ('RedScrape 0.1')

reddit = praw.Reddit(user_agent=user_agent)

subreddit = reddit.get_subreddit('askreddit')

text = []

for submission in subreddit.get_new(limit=5000):
	print 'Title:', submission.title
	print "Text: ", submission.selftext
	print "Score: ", submission.score

	text.append(submission.title)
	text.append(submission.selftext)

	try:
		submission.replace_more_comments(limit=50, threshold=0)
	except:
		continue

	for comment in submission.comments:
		try:
			print 'Comment Body:', comment.body
			text.append(comment.body)
		except:
			pass

	print "---------------------------------\n"

	save(text, 'new_data.txt')
	text = []