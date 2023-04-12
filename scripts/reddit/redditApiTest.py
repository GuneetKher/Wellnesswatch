from redditApi import SubredditScrapper
from datetime import datetime


sub = SubredditScrapper('mentalhealth')
after = datetime(2022, 12, 3)
before = datetime(2022, 12, 4)
sub.PostsBetween(after,before)