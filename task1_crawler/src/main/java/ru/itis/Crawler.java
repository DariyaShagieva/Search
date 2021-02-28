package ru.itis;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;

public class Crawler {
    private static final Logger logger = LogManager.getLogger(Crawler.class.getName());

    public static void crawling(String fileName) {
        List<URL> sitesURL = getUrlsFromFile(fileName);
        writeSiteOnFile(sitesURL);
    }

    /**
     * Получение списка урлов из файла
     * @param fileName название файла
     * @return список урлов
     */
    private static List<URL> getUrlsFromFile(String fileName) {
        List<URL> sitesURL = new LinkedList<>();
        try (BufferedReader bufferedReader = new BufferedReader(new FileReader(fileName))) {
            String line = bufferedReader.readLine();
            while (line != null) {
                sitesURL.add(new URL(line));
                line = bufferedReader.readLine();
            }
        } catch (IOException e) {
            logger.warn(e);
        }
        return sitesURL;
    }

    /**
     * Получение страницы по урлу и запись ее содержимого в файл
     * @param urls список урлов
     */
    private static void writeSiteOnFile(List<URL> urls) {
        try(FileWriter indexFileWriter = new FileWriter("index.txt")) {
            for (URL url : urls) {
                try (FileWriter fileWriter = new FileWriter("files/выкачка_" + (urls.indexOf(url) + 1) + ".txt")) {
                    logger.info(url);
                    Document doc = Jsoup.connect(url.toString()).get();
                    fileWriter.write(doc.body().text());
                    fileWriter.flush();
                    addInIndexFile(url, urls.indexOf(url), indexFileWriter);
                } catch (IOException e) {
                    logger.warn(e);
                }
            }
        } catch (IOException e) {
            logger.warn(e);
        }

    }

    /**
     * Добавить запись в index.txt
     *
     * @param url   урл сайта
     * @param index номер сайта в файле
     */
    private static void addInIndexFile(URL url, int index, FileWriter fileWriter) throws IOException {
            fileWriter.write((index + 1) + " " + url + "\n");
            fileWriter.flush();
    }

}
