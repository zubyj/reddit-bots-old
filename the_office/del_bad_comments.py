import praw

name = 'MichaelGScottBot'

reddit = praw.Reddit(name)
dwight = reddit.redditor(name)
counter = 0
for comment in dwight.comments.new(limit=None):
    if counter > 1:
        break
    counter+=1
    print(comment.body)
    print(comment.score)

    if comment.score < -3:
        comment.delete()