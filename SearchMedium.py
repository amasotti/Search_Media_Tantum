'''

Search all the forms in all files of a chosen directory which have middle endings
Once found, the script takes from Perseus the translation and the morphological parsing

The results are print in a txt file in the form:
    "file_id-verbal_form-translation-morpho_parsing-medium_tantum"
The last parameter (medium_tantum) is a bool (1 for medium tantum, 0 if not)

The scripts also creates a report with the statistics of the forms found is printed
together with the forms which were false positives or not in the Perseus Dictionary

GNU License v.3.0 -  20.09.2018 - Antonio Masotti, University of Göttingen

'''
#import necessary packages
import os
from tkinter import filedialog as tkFileDialog
import re
import requests
from bs4 import BeautifulSoup
import Auxialiary as aux

# general middle endings
M_ENDUNGEN = ["(μαί|μαι|μαῖ|μᾶι)",
              "(άι|αι|αί|αῖ|ᾶι)",
              "(ῃ|ῇ|ῄ|ει|εί|εῖ)",
              "(τάι|ται|ταί|ταῖ|τᾶι)",
              "(το|τό)",
              "(μεθα|μεθα|μέθα|μεθά)",
              "(σθέ|σθε|σθ)",
              "(νταί|νται|ντάι|νταῖ|ντ|ντο|ντό)",
              "(σθαί|σθάι|σθαι|σθ)",
              "(μήν|μην|μῆν)",
              "(σο|σό)",
              "(ω|ώ|ῶ)",
              "(ου|ού|οῦ)",
              "(ἱό|ιό|ιο)",
              "(σθω|σθώ|σθῶ)",
              "(σθων|σθών|σθῶν)",
              "(σθωσαν|σθώσαν|σθῶσαν|σθωσαν|σθωσάν)",
              "(μέν\w{1,3}|μεν\w{1,3})"]

print('Choose where to save the output file: ')
os.system("pause")
OUTPUT_DIRECTORY = tkFileDialog.askdirectory()
os.chdir(OUTPUT_DIRECTORY)

NAME_OUTPUT = input("How do you want to name the output file: ")
OUTPUT_FILE = str(NAME_OUTPUT)+".txt"
OUTPUT_STATISTICS = str(NAME_OUTPUT)+"_Stat.txt"
with open(OUTPUT_FILE, "a", encoding="UTF-8") as table:
    table.truncate(0)
    table.write("id_testo-forma-verbo-traduzione-morpho_parsing-medium_tantum\n")

    while True:
        VERBAL_FORMS = []

        print('Scegli la directory dei testi: ')
        os.system("pause")
        TEXT_DIRECTORY = tkFileDialog.askdirectory()
        os.chdir(TEXT_DIRECTORY)
        FILE_LIST = [os.path.abspath(x) for x in os.listdir(TEXT_DIRECTORY)]

        for element in FILE_LIST:
            lista_non_trovati = []
            lista_tantum = []
            lista_active = []

        #file_path = tkFileDialog.askopenfilename()
            with open(element, "r", encoding="UTF-8") as text_file:
                raw_text = text_file.read()
                id_text = os.path.basename(os.path.splitext(element)[0])

            # prepare the text deleting the verse number
            def delete_number(text_to_analyze):
                '''

                 DOC: Deletes the verse number from the raw text

                '''
                number = r"(\d{1,}\.?\d{1,}?)"
                number_subst = ""
                find_number = re.sub(number, number_subst, text_to_analyze, 0, re.MULTILINE | re.DOTALL)

                if find_number:
                    raw_text = find_number

                return raw_text
            # new text = text without verse number
            text = delete_number(raw_text)

                    #search for the ending patterns in the text
            for endung in M_ENDUNGEN:
                regex = "\\b(\\w+"+endung+")\\b"
                #print(regex)
                matches = re.findall(regex, text, re.MULTILINE)
                VERBAL_FORMS.append(matches)

            # prepare results and get list of verbal forms
            trasformati = aux.trasforma_result(VERBAL_FORMS)
            transformed = trasformati[0]

            # iterate through the verb forms founded
            counter = 0
            for form in transformed:
                counter += 1
                print("-------------------------------------")
                print("PROGRESS: "+str(counter)+
                      " of "+str(len(transformed))+
                      " file currently analyzed: "+str(id_text))
                print("-------------------------------------")
                link = "http://www.perseus.tufts.edu/hopper/morph?l="+form+"&la=greek"

                get_source = requests.get(link)
                source = get_source.text

                parsed = BeautifulSoup(source, 'lxml')
                morpho_check = parsed.select('td')

                # iterate through the <td> css classes of Perseus
                i = 0
                while i < len(morpho_check):
                    check2 = re.search(r"(<td>((verb|part)(.*))<\/td>)", str(morpho_check[i]), 0)

                    if check2 is None:
                        i += 1
                        continue
                    else:
                        morpho_parsing = str(check2.group(2))
                        break

                if check2 == [] or check2 is None:
                    lista_non_trovati.append(form)
                    continue
                else:
                    # set the regex to find the lemma
                    lemma = parsed.select('h4.greek')[0].text.strip()

                if lemma == '':
                    lista_non_trovati.append(form)
                    continue
                else:
                    # get the translation from Perseus
                    translation = parsed.select('span.lemma_definition')[0].text.strip()

                    check_regex = r"(\w*(μάι|μαι|μαί|μαῖ|μᾶι)\b)"
                    subst = "\g<1>"
                    check = re.search(check_regex, lemma, re.MULTILINE)

                    if check != None:
                        mtantum = 1
                        lista_tantum.append(lemma)
                    else:
                        mtantum = 0
                        lista_active.append(lemma)

                    table.write(str(id_text)+
                                "-"+str(form)+"-"+str(lemma)+
                                "-"+str(translation)+
                                "-"+str(morpho_parsing)+
                                "-"+str(mtantum)+
                                "\n")
            os.chdir(OUTPUT_DIRECTORY)
            with open(OUTPUT_STATISTICS, "a", encoding="UTF-8") as stat:
                stat.write("----STATISTICS OF "+str(id_text)+"----\n")
                stat.write("-------------------------------\n---NOT-FOUND or NOT-VERB---")
                voci_non_trovate = ",".join(e for e in lista_non_trovati)
                stat.write("\n"+str(voci_non_trovate)+"\n")
                stat.write("--------------------------------------------------------\n")
                stat.write("Total verbal forms found: "+str(len(transformed))+
                        "\n"+"Media_tantum: "+str(len(lista_tantum))+"\n"+
                        "Not-Media_tantum:"+str(len(lista_active))+"\n"+
                        "Forms not found on Perseus or not verbs: "
                        +str(len(lista_non_trovati))+
                        "\n--------------------------------------------------------\n\n")
# ask the user if the another directory should be scanned
        if aux.again():
            continue
        else:
            break
