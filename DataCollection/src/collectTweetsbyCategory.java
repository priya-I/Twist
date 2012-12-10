
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import twitter4j.IDs;
import twitter4j.Paging;
import twitter4j.Status;

import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;


public class collectTweetsbyCategory {
	public static void main(String[] args)  throws TwitterException, IOException {
		String line;
		String handle;
		Twitter twitter = new TwitterFactory().getInstance();
		
		/* Read the categories from categories.txt file 
		for each category read the corresponding file which consists of a list of influential handles under
		these categories e.g. if the category is called sports in the category.txt file
		we will have a file called sports.txt which will contain a list of all handles in that category */
		BufferedReader rcat = new BufferedReader(new FileReader("categories.txt"));
		
		/*Tweets are collected page by page with 200 tweets collected per-page, user should define the start 
		and end page limits in this file, ideally five pages should be taken at a time hence in the file the 
		start and end page should be defined as
		StartPage:1
		EndPage:5*/
		BufferedReader pages = new BufferedReader(new FileReader("pagelimit.txt"));
		String pageline="";
		String startpage="";
		String endPage="";
		
		//Read first line for start page
		line=pages.readLine();
		startpage = line.substring(line.indexOf(":")+1);
		
		//Read next line for end page
		line=pages.readLine();
		endPage = line.substring(line.indexOf(":")+1);
		
		while ((line = rcat.readLine()) != null) {
			
			//Reading handles for each category.
			BufferedReader br = new BufferedReader(new FileReader(line+".txt"));
			
			while ((handle = br.readLine()) != null) {
				String userID = handle;
				long lCursor = -1;

			    BufferedWriter w = new BufferedWriter(new FileWriter(line+"tweets1.txt",true));
			    /*User to define the start page a */
			    
			    	for (int l=Integer.parseInt(startpage);l<=Integer.parseInt(endPage);l++){
			    	
			    	//Read the timeline page by page
					  Paging paging = new Paging(l, 200);
					  List<Status> statuses = twitter.getUserTimeline(handle,paging);
				
					  for(int i=0 ;i< statuses.size();i++)
						{
						  w.write("Page:"+l+" : line "+i+"--->"+statuses.get(i).getText()+"\n");

						    
						}
			    	}
				w.close();
				
    
			}	
			br.close();
		}
		rcat.close();	
		
	}

}
