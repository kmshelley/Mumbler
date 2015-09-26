import sys
import os
import zipfile
import ast
import random
import bisect

def weighted_choice(weights):
    totals = []
    cum_sum = 0

    for w in weights:
        cum_sum += w
        totals.append(cum_sum)

    random_int = random.random()*cum_sum
    return bisect.bisect_right(totals,random_int)




def OLDweighted_choice(words,counts):
        #chooses randomly from a list of words, weighted by counts
        new_list = []
        #for word,count in zip(words,counts):new_list = new_list + [word]*count
        return random.choice(sum(([word]*count for word,count in zip(words,counts)),[]))


def get_next_word(word):
        #my_dir = os.path.join(os.getcwd(),'letters')
        my_dir = '/gpfs/gpfsfpo/letters'
        word = word.lower()
        letter = word[0] #first letter of word
        words = {}
        #compile word pair counts across blocks
        try:
                z = zipfile.ZipFile(os.path.join(my_dir,'%s.zip' % letter), mode='r',allowZip64=True, compression=zipfile.ZIP_DEFLATED)
                words = ast.literal_eval(z.read('%s' % letter ))[word]
                
        except Exception as e:
                pass

        try:
                z.close()
        except:
                pass
        
        if words <> {}:
                #if the word is the start of a 2gram,
                #use random choice to pick the next
                #word based on 2gram weights
                weights,word_list = (list(x) for x in zip(*sorted(zip(words.values(),words.keys()))))
                next_word = word_list[weighted_choice(weights)]
                #next_word = random.choice(word_list)
                sys.stdout.write(next_word)
        else:
                sys.stdout.write("No more words")

if __name__ == '__main__':
        try:
                word = sys.argv[1]
                get_next_word(word)
        except Exception as e:
                print "Error! %s" % e
