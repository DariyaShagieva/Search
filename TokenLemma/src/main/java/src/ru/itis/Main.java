package src.ru.itis;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.StringTokenizer;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.ru.RussianAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;

public class Main {

    public static String path = "files/";


    public static List<String> files = new LinkedList<>();

    public static  String split = " '\\n', '\\t', '\\r', ':', ';', '(', ')', '.', ',', '[', ']', '—', '∅', '~', '%', ' ', '-', '\"', '{', '}', '!', '?',\n" +
            "            '@', '$', '=', '^', '/', '\\\\', '°', '#', '*', '|', '§', '\\'',.";

    public static String readFileAsString(String fileName) throws IOException {
        BufferedReader reader = new BufferedReader( new FileReader (fileName));

        StringBuilder stringBuilder = new StringBuilder();

        String line = reader.readLine();
        while (line != null) {
            stringBuilder.append(line);
            line = reader.readLine();
        }
        return stringBuilder.toString();
    }

    public static void getToken() throws IOException {

        for (int i = 0; i < 100; i ++) {
            files.add("выкачка_" + (i + 1) + ".txt");
        }

        StringTokenizer st;
        String token;
        FileWriter fileWriter = new FileWriter("token.txt");
        FileWriter lemmaWriter = new FileWriter("lemma.txt");

        for (int i = 0; i < 100; i ++) {
             st = null;
             st = new StringTokenizer(readFileAsString(path + files.get(i)), split );
            while (st.hasMoreTokens()) {
                token = st.nextToken();
                fileWriter.write(token + '\n');
                getLemma(token.toLowerCase(), lemmaWriter);
            }
        }
        fileWriter.flush();
        lemmaWriter.flush();
    }

    public static void getLemma(String token, FileWriter lemmaWriter) throws IOException {
        Analyzer analyzer = new RussianAnalyzer();
        TokenStream tokenStream = analyzer.tokenStream("token", token);
        CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
        tokenStream.reset();
        while (tokenStream.incrementToken()) {
            String lemma = charTermAttribute.toString();
            lemmaWriter.write(token + " " + lemma + " ");
        }


    }


    public static void main(String[] args) throws IOException {

        getToken();
    }
}
