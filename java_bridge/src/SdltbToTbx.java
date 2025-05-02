import com.healthmarketscience.jackcess.*;
import java.io.*;
import java.util.*;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;

public class SdltbToTbx {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Usage: java -jar sdltb_converter.jar input.sdltb output.tbx");
            return;
        }

        String inputFile = args[0];
        String outputFile = args[1];

        Database db = DatabaseBuilder.open(new File(inputFile));
        Table conceptTable = db.getTable("Concept");

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.newDocument();

        Element root = doc.createElement("tbx");
        doc.appendChild(root);

        for (Row row : conceptTable) {
            Element termEntry = doc.createElement("termEntry");

            Element langSet = doc.createElement("langSet");
            langSet.setAttribute("xml:lang", "en-US");

            Element tig = doc.createElement("tig");
            Element term = doc.createElement("term");
            term.setTextContent(row.get("TermText").toString());

            tig.appendChild(term);
            langSet.appendChild(tig);
            termEntry.appendChild(langSet);
            root.appendChild(termEntry);
        }

        Transformer transformer = TransformerFactory.newInstance().newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new File(outputFile));
        transformer.transform(source, result);

        System.out.println("TBX exported successfully to: " + outputFile);
    }
}
