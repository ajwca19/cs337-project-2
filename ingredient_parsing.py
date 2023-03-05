import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import spacy
import unicodedata
nlp = spacy.load("en_core_web_sm")

#define ingredient class for use with other procedures
class Ingredient:
    #parses raw text: THE CORE IMPORTANT THING HERE!    
    def parse_ingredient(self, text):
        text = re.sub("⁄", "/", unicodedata.normalize("NFKC", text))
        #parse = nlp(text)
        #print([token.dep_ for token in parse])
        #(fix me!)
        extra_info = ""
        info_re = re.search("\(.*\)", text)
        if info_re:
            #there's extra information in the text
            extra_info = info_re.group()
            re.sub("\(.*\)", "", text)
        #start with extra preparation because it's easiest: assume everything after comma is additional prep
        prep = ""
        if "," in text:
            phrase_list = text.split(",")
            for i in range(len(phrase_list)):
                phrase_parse = nlp(phrase_list[i].lstrip())
                if i == 0:
                    last_pos = phrase_parse[-1].pos_
                elif phrase_parse[0].pos_ != last_pos:
                    #identify phrase as start of preparation
                    print("I think " + phrase_parse[0].pos_ + " is different from " + last_pos)
                    prep = ",".join(phrase_list[i:]).lstrip()
                    text = ",".join(phrase_list[:i])
                    print(text)
                    break
                else:
                    last_pos = phrase_parse[-1].pos_
        amount = ""
        if text[0].pos_ == "NUM":
            #there's an amount listed
            amount = text[0].text
            #for i in range(len(text)):
                #DEAL WITH ME LATER!
        name = ""
        
        return (amount, name, prep, extra_info)
    
    def get_amount(self):
        return self.amount
    
    
    def get_name(self):
        return self.name
    
    def get_prep(self):
        return self.prep
    
    def get_extra(self):
        return self.extra
    
    def get_text(self):
        return self.text
    

    def __init__(self, text):
        self.text = text
        self.amount, self.name, self.prep, self.extra = self.parse_ingredient(text)
        
#take in raw text
def parse_ingredient_list(ingredients):
    return list(map(lambda t: Ingredient(t), ingredients))