
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
		
		BufferedReader rcat = new BufferedReader(new FileReader("categories.txt"));
		while ((line = rcat.readLine()) != null) {
			BufferedReader br = new BufferedReader(new FileReader(line+".txt"));
			
			while ((handle = br.readLine()) != null) {
				String userID = handle;
				long lCursor = -1;

			    BufferedWriter w = new BufferedWriter(new FileWriter(line+"tweets2.txt",true));
			    BufferedWriter w1 = new BufferedWriter(new FileWriter(line+"tweetscount2.txt",true));
			    	for (int l=5;l<7;l++){
					  Paging paging = new Paging(l, 200);
					  List<Status> statuses = twitter.getUserTimeline(handle,paging);
					
					  //twitter.getUserTimeline().s
					  for(int i=0 ;i< statuses.size();i++)
						{
						  w.write(statuses.get(i).getText()+"\n");
						  w1.write("Page:"+l+"*"+"count:"+i+"-->"+statuses.get(i).getText()+"\n");
						  
						  
						}
			    	}
				w.close();
				w1.close();
    
			}	
			br.close();
		}
		rcat.close();
		
		//String[] SportsCat ={"kaka","shaq","nba","espn","ochocinco","lancearmstrong","lakers","sportsnation"};
		
		
		
		
		
		
	}

}
