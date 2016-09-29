import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Set;
import java.util.regex.Pattern;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class MyCrawler extends WebCrawler {
	private int filenumber = 385; 
	public static Set<WebURL> links; 
	
	@Override
	public boolean shouldVisit(Page referringPage, WebURL url) {
		return true;
	}
	
	 @Override
	 public void visit(Page page) {
		 String url = page.getWebURL().getURL();
		 int statusCode = page.getStatusCode();
//		 System.out.println(statusCode);
		 HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
		 links = htmlParseData.getOutgoingUrls();
		 System.out.println(links);
		 System.out.println(links.size());
		 try(
		 	FileWriter fw = new FileWriter("outgoing_links.csv", true);
		 	BufferedWriter bw = new BufferedWriter(fw);
			PrintWriter out = new PrintWriter(bw);
			FileWriter file = new FileWriter("output/"+filenumber+".html");
			BufferedWriter buffer = new BufferedWriter(file);
			PrintWriter output = new PrintWriter(buffer);			
			)
			{
			 	if (url.contains("?tref=category"))
			 	{ 
			 		filenumber++;
			 		out.println(url+ "," + statusCode);
			 		output.println(new String(page.getContentData()));
			 	}
			} catch (IOException e) {
				    e.printStackTrace();
			}		 		 
	 }			
}
