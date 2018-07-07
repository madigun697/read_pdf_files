import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.PDFTextStripperByArea;

public class readPdf {

    private static String ROOT_DIR = "/Users/madigun/Google Drive/Grace&Kyle/Football/football_pdfreader/src/main/java";

    public static void main(String[] args) throws IOException {

        System.out.println("Start read PDFs");

        // Read files' path in directory
        ArrayList<String> pdfList = getFileList();

        // Each pdf file read
        for (int i = 0; i < pdfList.size(); i++) {
            try (PDDocument document = PDDocument.load(new File(pdfList.get(i)))) {
                document.getClass();
                if (!document.isEncrypted()) {
                    PDFTextStripperByArea stripper = new PDFTextStripperByArea();
                    stripper.setSortByPosition(true);

                    PDFTextStripper tStripper = new PDFTextStripper();
                    String pdfFileInText = tStripper.getText(document);

                    String lines[] = pdfFileInText.split("\\r?\\n");
                    // Write text file
                    writeText(i, lines);
                }
            }
        }

        System.out.println("Finish read PDFs");
    }

    private static ArrayList<String> getFileList() {
        // Select directory including pdf files
        File dir = new File(ROOT_DIR + "/pdfs");
        File[] fileList = dir.listFiles();

        // Initiate pdf file path list
        ArrayList<String> pdfList = new ArrayList<>();
        for (int i = 0; i < fileList.length-1; i++) {
            pdfList.add("");
        }

        // Each file insert in the list by index
        for (File file : fileList) {
            if (file.isFile() && !file.getName().equals(".DS_Store")) {
                String idx_str = file.getName().split("속보포함")[1].split("\\.")[0];
                if (idx_str.isEmpty()) {
                    idx_str = "1";
                }
                int idx = Integer.parseInt(idx_str) - 1;
                pdfList.set(idx, ROOT_DIR + "/pdfs/" + file.getName());
            }
        }

        return pdfList;
    }

    private static void writeText(int idx, String[] lines) throws IOException {
        BufferedWriter out = new BufferedWriter(new FileWriter(ROOT_DIR + "/txts/record" + idx + ".txt"));
        for (String line: lines) {
            out.write(line);
            out.newLine();
        }
        out.close();
    }

}
