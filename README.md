# Search_Media_Tantum

Python scripts to search verbal forms in Ancient Greek texts and compare them with them morphological parsing on Perseus.
The script then extracts forms beloging to middle verbs (LSJ lemmata entry ending in -μαι)

The results are print in a txt file in the form:

        "file_id-verbal_form-translation-morpho_parsing-medium_tantum"

The last parameter (medium_tantum) is a bool (1 for medium tantum, 0 if not)

After each file a report with the statistics of the forms found is printed together with the forms which were false positives or not in the Perseus Dictionary
