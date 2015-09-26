import urllib
import os
import zipfile
import contextlib
import ast


def update_word_dict(old_dict,new_dict):
        #updates a dictionary of word counts
        for key in old_dict:
                if key not in new_dict:
                        new_dict[key] = old_dict[key]
                else:
                        for key2 in old_dict[key]:
                                if key2 in new_dict[key]:
                                        new_dict[key][key2]+=old_dict[key][key2]
                                else:
                                        new_dict[key][key2] = old_dict[key][key2]
        return new_dict

def OLD_update_word_dict(old_dict,new_dict):
        #updates a dictionary of word counts
        for key in old_dict:
                if key not in new_dict:
                        new_dict[key] = old_dict[key]
                else:
                        new_dict[key]+=old_dict[key]
        return new_dict
        
def get_2_grams(m,n,machine):
        for i in range(m,n):
                url = 'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20090715-%s.csv.zip' % str(i)
                #my_dir = '/gpfs/gpfsfpo/letters/'
                my_dir = os.path.join(os.getcwd(),'letters')
                filename = os.path.join(my_dir,'googlebooks-eng-all-2gram-20090715-%s.csv.zip' % str(i))
                urllib.urlretrieve(url,filename)
                z = zipfile.ZipFile(filename,allowZip64=True)
                for doc in z.namelist():
                        if doc.find('googlebooks-eng-all-2gram-20090715-%s.csv' % str(i)) > -1:
                                with contextlib.closing(z.open(doc,'r')) as unzipped:
                                        words = {}
                                        #prev_word = None
                                        prev_letter = None
                                        for line in unzipped:
                                                if len(line.strip().split())==6:
                                                        word1,word2,year,match_count,page_count,volume_count = line.lower().strip().split()
                                                        letter = word1[0]
                                                        
                                                        if word1.isalpha() and word2.isalpha():
                                                                #if word1 <> prev_word and prev_word:
                                                                if letter <> prev_letter and prev_letter:
                                                                        try:
                                                                                #z2 = zipfile.ZipFile('/gpfs/gpfsfpo/letters/%s_%s.zip' % (prev_letter,machine), mode='r',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                                                                                z2 = zipfile.ZipFile(os.path.join(my_dir,'%s_%s.zip' % (prev_letter,machine)),mode='r',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                                                                                old_words = ast.literal_eval(z2.read('%s' % prev_letter ))
                                                                                if old_words <> '': words = update_word_dict(old_words,words)
                                                                                z2.close()
                                                                        except:
                                                                                pass

                                                                        #z2 = zipfile.ZipFile('/gpfs/gpfsfpo/letters/%s_%s.zip' % (prev_letter,machine),mode='w',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                                                                        z2 = zipfile.ZipFile(os.path.join(my_dir,'%s_%s.zip' % (prev_letter,machine)),mode='w',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                                                                        z2.writestr('%s' % prev_letter, str(words))                                                                        
                                                                        words = {}
                                                                        
                                                                #prev_word = word1
                                                                prev_letter = letter
                                                                if word1 not in words: words[word1] = {}
                                                                if word2 not in words[word1]: words[word1][word2] = 0.0
                                                                words[word1][word2]+=float(match_count)
                os.remove(filename)
        print "Done getting 2-grams!"

get_2_grams(0,1,1)
