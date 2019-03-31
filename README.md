## For processing links and searching for nouns


The following scripts are included in this repository:

*google_links.py* - extracts a total of 1000 links from Google search API using 10 search terms

You cat can all the output files from google_lniks output into one file to process at once and de-dupe e.g.

```
cd data
cat *.txt > combined_output.txt
```

Examples of data can be found in the data directory. 


*remove_dupes.py* - removes any duplicate links returned by the google_links.py output.

*key_word_compare.py* - searches the the extracted links for the 18 chosen keywords 

*frequency_extractor.py* - returns the most common 50 nouns in each link

*trigram_tagger.py* - support class used by frequency_extractor.py within noun extraction



