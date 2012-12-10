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
public class hometimeline {

	/**
	 * @param args
	 * @throws TwitterException 
	 * @throws IOException 
	 */
	public static void main(String[] args) throws TwitterException, IOException {
		// TODO Auto-generated method stub
		
		 Twitter twitter = TwitterFactory.getSingleton();
		  
		    int i=1;
		    System.out.println("Showing home timeline.");
		    BufferedWriter w = new BufferedWriter(new FileWriter("HometimelineSports.txt",true));
		    for (int l=1;l<26;l++){
				  Paging paging = new Paging(l, 200);
				  List<Status> statuses = twitter.getHomeTimeline(paging);
				  for (Status status : statuses) {
			        /*System.out.println(status.getUser().getName() + ":" +
			                           status.getText()); */
			        w.write(status.getText()+"\n");
		
			        
			    }
		    }
		    w.close();

	}

}
