
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import twitter4j.IDs;
import twitter4j.Paging;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.UserMentionEntity;


public class collectTweets {
	public static void main(String[] args)  throws TwitterException, IOException {
		Twitter twitter = new TwitterFactory().getInstance();
		
		String userID = "sonali_sh";
		
		long lCursor = -1;
		IDs friendsIDs = twitter.getFriendsIDs(userID, lCursor);
	    BufferedWriter w = new BufferedWriter(new FileWriter(userID+".txt",true));
		do
		{
		  for (long j : friendsIDs.getIDs())
		   {
			 
			 
	        	//UserMentionEntity[] mentions = status.getUserMentionEntities(); 
			  for (int k = 1 ;k<2 ;k++)
			  {
				 Paging paging = new Paging(k, 50);
			  List<Status> statuses = twitter.getUserTimeline(twitter.showUser(j).getScreenName(),paging);
			  
			  for(int i=0 ;i< statuses.size();i++)
				{
				  w.write(statuses.get(i).getText()+"\n");
				  
			  		/*String[] result = statuses.get(i).getText().split(" ");
	        		 
	        		 for(int k=0; k<result.length; k++)
	        		 {
	        			 
	        			 m=TAG_PATTERN.matcher(result[k]);
	        			 if(m.find())
	        			 {  
	        					w.write(twitter.showUser(j).getScreenName()+"->"+result[k].trim()+"\n");	 
	        			 }
	        			 
	        		 } */
				}
			  }
		       
		   }
		}while(friendsIDs.hasNext());
		w.close();
	     
	}

}
