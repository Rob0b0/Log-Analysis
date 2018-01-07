#!/usr/bin/env python3
import psycopg2

print("News Report:")
print("__________________________")

db = psycopg2.connect("dbname=news")
# question 1
print("What are the most popular three articles of all time?")
c = db.cursor()
c.execute("select path, count(*) as visited from log group by path " +
          "order by visited desc limit 5")
mostHitFivePath = c.fetchall()
# print(mostHitFivePath[0][1])
# get the slugs
count = 0
for row in mostHitFivePath:
    if (count >= 3):
        break
    pathName = row[0]
    # print("Path: "+ pathName)
    if (pathName.startswith("/article/")):
        slug = pathName[9:]
        # print("slug: "+slug)
        # do query in articles
        # prevent sql injection
        c.execute("select title from articles where slug=%s;", (slug,))
        articleName = c.fetchall()
        # print(articleName[0])
        print(articleName[0][0] + " --- " + str(row[1]) + " views")
        count = count + 1

print("__________________________")


# Question 2
# Create view 'articleView'
c.execute("create view articleView as select path, count(*) as visited " +
          "from log group by path order by visited desc")
# concatenate '/article/' on articles' slug
c.execute("create view newSlug as select articles.author, articles.title, " +
          "'/article/' || articles.slug as slug, articles.id from articles;")
# left join newSlug and articleView:
c.execute("create view articleCount as select * from newSlug left join " +
          "articleView on newSlug.slug = articleView.path;")

c.execute("select authors.name, sum(articleCount.visited) as sumVisited from "
          + "authors left join articleCount "
          + "on authors.id = articleCount.author "
          + "group by authors.name "
          + "order by sumVisited desc;")
mostHitAuthors = c.fetchall()
print("Who are the most popular article authors of all time? ")

for row in mostHitAuthors:
    authorName = row[0]
    views = row[1]
    print("{} --- {} views".format(authorName, views))

print("__________________________")


# Question 3
# create view 'statusDay'
c.execute("create view statusDay as select time::date, status, count(*) " +
          "from log group by time::date, status;")

c.execute("select * from statusDay")
statusInfo = c.fetchall()
i = 0
dateList = []
while i < len(statusInfo):
    okCount = 0
    errorCount = 0
    date = statusInfo[i][0]
    status = statusInfo[i][1]
    count = statusInfo[i][2]
    if (date == statusInfo[i + 1][0] and status == '200 OK'):
        okCount = count
        errorCount = statusInfo[i + 1][2]
        if ((float(errorCount)) / (errorCount + okCount) > 0.01):
            dateList.append("{0:%Y-%m-%d}".format(date))
        i = i + 2
    else:
        i = i + 1

print("On which days did more than 1% of requests lead to errors?")
for date in dateList:
    print(date)

db.close()