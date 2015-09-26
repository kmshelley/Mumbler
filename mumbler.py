import sys
import os
import zipfile
import contextlib
import ast
import random
import subprocess

def mumbler(word,n):
        #my_dir = os.path.join(os.getcwd(),'letters')
        my_dir = '/gpfs/gpfsfpo/letters/'
        index_file = '/gpfs/gpfsfpo/letters/index'
        with open(index_file,'r') as locs:
                #find which node contains bigram counts file
                index = ast.literal_eval(locs.read())
        word = word.lower()
        
        for i in range(n):
                print '%s ' % word
                if i < n-1:
                        letter = word[0] #first letter of word
                        node = index[letter]
                        try:
                                p = subprocess.Popen(["ssh", "%s" % node, "python /root/mumbler_code/get_next_word.py %s" % word], stdout=subprocess.PIPE)
                                next_word = p.communicate()[0]
                        except Exception as e:
                                print "Error: %s" % e
                        if next_word <> "No more words":
                                word=next_word
                        else:
                                return
        return

if __name__ == '__main__':
        try:
                word,n = sys.argv[1],int(sys.argv[2])
                mumbler(word,n)
        except Exception as e:
                print "Error! %s" % e
