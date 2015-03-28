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
	// For the next variables the index is the mode of text's class
	// estimation which can be: [averaged, weighted, counted]
	static int[] pos = {0, 0, 0};
	static int[] neg = {0, 0, 0};
	static int[] unknown = {0, 0, 0};
	static final double[] NEUTRAL = {2.0, 2.0, 0.0};

	private static void readFile(File fin) throws Exception {
		FileInputStream fis = new FileInputStream(fin);
	 
		BufferedReader br = new BufferedReader(new InputStreamReader(fis));
	 
		String line = null;
		String reviewText;
		while ((line = br.readLine()) != null) {
			reviewText = readJSON(line);
			findSentiment(reviewText);
			// System.out.println("Text: " + reviewText);
			// System.out.println("Final Rating: " + findSentiment(reviewText) + "\n");
		}
	 
		br.close();
	}

	/**
	 * Takes the scores for average, weighted and counted sentiment estimates
	 * and updates the positive, negative and unknown counters accordingly
	**/
	private static void updateCounts(int[] scores) {
		// The splitting point is NEUTRAL which is different in each case
		for(int i = 0; i < len; i++) {
			if(scores[i] > NEUTRAL[i]) {
				pos[i]++;
			} else if (scores[i] < NEUTRAL[i]) {
				neg[i]++;
			} else {
				unknown[i] ++;
			}
		}
	}

	// Parses the JSON line and extracts the  review text
	private static String readJSON(String str) throws Exception{
		JSONParser jsonParser = new JSONParser();
		JSONObject jsonObject = (JSONObject) jsonParser.parse(str);

		return (String) jsonObject.get("text");
	}
	
	/**
	 * Computes the sentiment estimation of the whole text.
	 * It iterates over all the sentences and gets a sentiment for each one.
	 * A sentiment score of 0 or 1 is negative, 2 neutral and 3 or 4 positive.
	 * The aggregation is being doe with three different modes.
	 * The first is the average of all the sentences. The second uses the 
	 * each sentence's length as weight and the third counts the number of 
	 * positive/negative sentences.
	**/
	public static int[] findSentiment(String text) {
		double sentimentAvg = 0; // Average sentiment of all sentences.
		double sentimentWeight = 0; // Weight each sentence by length.
		double sentimentCount = 0; // Count pos/neg sentences, ignoring neutral.

		if (text != null && text.length() > 0) {
			int count = 0;
			int weight = 0;
			int clss = 0;

			Annotation annotation = pipeline.process(text);

			for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
				Tree tree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
				int sentiment = RNNCoreAnnotations.getPredictedClass(tree);
				String sentenceText = sentence.toString();

				// System.out.println(sentence + " | length " +
				// 	sentenceText.length() + " | score " + sentiment);

				count++;
				weight += sentenceText.length();
				sentimentAvg += sentiment;
				sentimentWeight += (double)sentiment * sentenceText.length();
				if (sentiment > 2) 
					sentimentCount++;
				else if (sentiment < 2)
					sentimentCount--;
			}

			System.out.println("Avg: " + ((sentimentAvg / count)));
			System.out.println("Weighted: " + ((sentimentWeight / weight)));
			System.out.println("Count: " + (sentimentCount));
			System.out.println("\n");
			return new int[]{1,1,1};
		} else {
			return new int[]{0, 0, 0};
		}
	}

	public static void main(String[] args) {

		String category = "restaurants";
		String quantity = "500";
		String clss = "pos";
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