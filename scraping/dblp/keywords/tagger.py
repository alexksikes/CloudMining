# Author Alex Ksikes

import sets
import string
import re

class StopListTagger:
    def __init__(self, stop_words='./stopwords.txt', freq_list=''):
        self.stop_words = sets.Set([word.lower().strip() for word in open(stop_words)])
        self.min_length = 3
        
        self.freq_list = {}
        if freq_list:
            for line in open(freq_list):
                word, count = line.split('\t')
                self.freq_list[word] = int(count)

    def tag(self, txt):
        tags = []
        for word in re.findall('[\w/+-]+', txt):
        #for word in re.findall('[^\s;,:\.\'"()!?`]+', txt):
            tag = self.get_tag(word)
            if tag and tag not in tags:
                tags.append(tag)
        return tags

    def get_tag(self, word):
        if self.is_stop_word(word) or self.is_digit(word):
            return ''
        
        if not self.is_special_form(word):
            word = word.lower()
        
        if self.freq_list:
            word = self.singular_or_plurial(word)
        
        return word
        
    def singular_or_plurial(self, word):
        if word[-1] == 's':
            if self.freq_list.get(word[:-1], 0) > self.freq_list.get(word, 1):
                word = word[:-1]
        elif self.freq_list.get(word + 's', 0) >= self.freq_list.get(word, 1):
            word = word + 's'
        return word
    
    def is_digit(self, word):
        return re.match('^[\d-]+(st|nd|rd|th)?$', word, re.I)
    
    def is_stop_word(self, word):
        word = word.lower().strip()
        return len(word) < self.min_length or word in self.stop_words
           
    def is_abbreviation(self, word):
        if word[-1] == 's':
            word = word[:-1]
        
        return re.match('\w{2,}', word) and word.upper() == word
        
    def is_special_form(self, word):
        return re.match('[^\s-]*?[A-Z][^\s-]*?[A-Z][^\s-]*', word)
        
def usage():
    print "Usage: python tagger.py stop_list text"
    print
    print "Description:" 
    print "Print a list tags given the text."
    print
    print "Options:" 
    print "-p, --plurial <frequency_list>        : decide to choose singular or plurial form using a freqency list."
    print
    print "Email bugs/suggestions to Alex Ksikes (alex.ksikes@gmail.com)" 

import sys, getopt
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:h", 
            ["plurial", "help"])
    except getopt.GetoptError:
        usage(); sys.exit(2)
    
    stop_list = './stop_words.txt'; freq_list = ''
    for o, a in opts:
        if o in ("-p", "--plurial"):
            freq_list = a
        elif o in ("-h", "--help"):
            usage(); sys.exit()
    
    if len(args) < 2:
        usage()
    else:
        print ' '.join(StopListTagger(args[0], freq_list).tag(args[1]))
        
if __name__ == '__main__':
    main()