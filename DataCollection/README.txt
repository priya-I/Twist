-This program is used for tweet collection for specific categories.

-The names of the categories are saved in categories.txt file, to add more categories add it to this file in a new line.

-There is a file corresponding to each category and that file contains the list of handles from which tweets are to be collected. e.g. if the category is called sports in the category.txt file we will have a file called sports.txt which will contain a list of all handles in that category.

-File pagelimit.txt contains the start and end page. Tweets are collected page wise and in breaks to ensure rate limit is not hit. When collecting data for multiple categories its is advisable to keep the number of pages to 5, hence define startPage and endPage from 1 to 6 and then keep changing it to the next set of 5 values e.g. startPage=6 , endPage = 10 and so on