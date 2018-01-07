# Udacity - Log Analysis Project
### Author: Yunbo Chen

## How to Run:
After going into the directory of the files, simply run `python NewsReport.py` as indicated in the first line of ` Example_Output.txt`. 

## Design Prospect
1. For the first question, I just simply run a direct query on the database and use python to loop through and print out the output.

2. For the second question, I created a `newSlug` view to recreate an "articles" table with slug name concatenated with '/article/' path name. 
```sql
create view articleView as 
select path, count(*) as visited from log group by path 
order by visited desc
```

Then I created a view for the previous answer, which is the most visited articles with number of visits. 
```sql
create view newSlug as 
select articles.author, articles.title, '/article/' || articles.slug as slug, articles.id 
from articles;
```
Also I created a view of joining those two views, making it ready for the final query join. 
```sql
create view articleCount as 
select * 
from newSlug left join articleView 
on newSlug.slug = articleView.path;
```
Finally, I left joined the last view with authors, summing up the number of visits and get the direct answer.

3. For the third question, I created a view of counting the number of 'OK' visits and '404' visits on each day. 
```sql
create view statusDay as 
select time::date, status, count(*) 
from log 
group by time::date, status;
```
Then I use python to calculate the percent of errornous visits and print out the result.   
// Note that the way I calculate the percentage is not very general, because I only expect the result to have only two status codes.