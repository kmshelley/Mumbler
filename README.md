# Mumbler
Random sentence generator from Google ngram data set.

To run the mumbler:

1. Run the get_ngrams script by calling the def get_2_grams. This process can be distributed accross several nodes by passing the 2gramfile number count range and a machine count. I.e "python -c 'import get_ngrams; get_ngrams.get_2_grams(0,30,1)' would be run to collect 2gram files 0 through 29 on machine 1.

2. If the data collection occurs on multiple nodes, run the secondary data processing step, preprocess_letters.py. This will combine 2gram word counts by the first letter of the first word.

3. Run the mumbler: 'python mumbler.py <word> <count>' passing the starting word and sentence length.
 
*Data Collection Preprocessing*: The ngram data is preprocessed at collection time and is stored in zipped files located on different nodes. The preprocessing involves aggregating the word pair occurrence counts per collection machine (each node collects a subset of the data separately) into key-value pairs: {word1: {word2.1: count1, word2.2: count2,...}} The dictionaries are stored in files by the first letter of word1, and the local machine where the data is stored. i.e. all words that start with the letter “A” that were in ngram files downloaded by node2 will be saved in the file a_2.zip. The original downloaded zipped files are removed after preprocessing.

*Post-Collection Preprocessing*: The ngram data is put through an additional preprocessing step after collection. Each of the individual letter bigram count dictionaries are combined into a single file to be solely located on a single node to speed up the runtime and reduce the network traffic of the mumbler. Each node houses a single zipped file for each letter for a portion of the alphabet (for example in a 3 node system node1 houses A – I, node2 houses J – R, and node3 houses S – Z.). The index file contains the location of each letter dictionary.  


*The Mumbler*: The mumbler checks the index file to find the location of the aggregated bigram word count file for the first letter of the current word. The script uses python's subprocess library to ssh into the remote machine and return the next word by utilizing a locally saved script get_next_word.py.
