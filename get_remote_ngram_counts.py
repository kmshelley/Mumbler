import sys
import os
import zipfile
import ast



def get_counts(word,i):
        #returns 2-gram counts dictionary from gpfs machine i
        #my_dir = os.path.join(os.getcwd(),'letters')
        my_dir = '/gpfs/gpfsfpo/letters'
        word = word.lower()
        letter = word[0] #first letter of word
        words = {}
        #compile word pair counts across blocks
        try:
                z = zipfile.ZipFile(os.path.join(my_dir,'%s_%s.zip' % (letter,i)), mode='r',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                words = ast.literal_eval(z.read('%s' % letter ))[word]
                z.close()
        except Exception as e:
                pass
        sys.stdout.write(str(words))

if __name__ == '__main__':
        try:
                word,i = sys.argv[1],int(sys.argv[2])
                get_counts(word,i)
        except Exception as e:
                print "Error! %s" % e
