import sys
import os
import zipfile
import ast

def combine_letters(letter):
        my_dir = '/gpfs/gpfsfpo/letters'
        words={}
        for i in range(1,4):
                try:
                        z = zipfile.ZipFile(os.path.join(my_dir,'%s_%s.zip' % (letter,i)), mode='r',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                        words.update(ast.literal_eval(z.read('%s' % letter )))
                        z.close()
                except Exception as e:
                        pass
        z = zipfile.ZipFile(os.path.join(my_dir,'%s.zip' % letter),mode='w',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
        z.writestr('%s' % letter, str(words))                                                                        
        words = {}


if __name__ == '__main__':
        try:
                letters = sys.argv[1].split(',')
                for letter in letters:
                        combine_letters(letter)
        except Exception as e:
                print "Error! %s" % e
