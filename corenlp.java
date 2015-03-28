import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.util.Properties;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

public class corenlp {

    static StanfordCoreNLP pipeline;

	private static void readFile(File fin) throws Exception {
		FileInputStream fis = new FileInputStream(fin);
	 
		BufferedReader br = new BufferedReader(new InputStreamReader(fis));
	 
		String line = null;
		while ((line = br.readLine()) != null) {
			readJSON(line);
		}
	 
		br.close();
	}

	private static void readJSON(String str) throws Exception{
		JSONParser jsonParser = new JSONParser();
		JSONObject jsonObject = (JSONObject) jsonParser.parse(str);

		String reviewText = (String) jsonObject.get("text");
		System.out.println("Text: " + reviewText);
		System.out.println("Rating: " + findSentiment(reviewText));
	}
	
	public static int findSentiment(String text) {
		int mainSentiment = 0;

		if (text != null && text.length() > 0) {
			int longest = 0;
			Annotation annotation = pipeline.process(text);

			for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
				Tree tree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
				int sentiment = RNNCoreAnnotations.getPredictedClass(tree);
				String partText = sentence.toString();

				if (partText.length() > longest) {
					mainSentiment = sentiment;
					longest = partText.length();
				}

			}
		}
		return mainSentiment;
	}

	public static void main(String[] args) {

		String category = "restaurants";
		String quantity = "500";
		String clss = "neg";
		String filePath = new String("yelp_" + category + "_reviews_" + quantity + "_" + clss + ".json");
		File fin = new File(filePath);

		// The CoreNLP pipeline
		Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
	    pipeline = new StanfordCoreNLP(props);

		try {
			readFile(fin);	
		} catch (Exception ex) {
			System.out.println("There was a problem: ");
			ex.printStackTrace();
		}
	}
}