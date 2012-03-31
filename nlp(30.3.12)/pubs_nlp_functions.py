""" this module proposes regular exparessions and key words matching techniques in parsing publications to authors, journals, and articles."""

#Package nltk :: Package tokenize 
#nltk.tokenize.regexp: Tokenizers that divide strings into substrings using regular expressions that can match either tokens or separators between tokens
from nltk.tokenize import *

#Package nltk :: Package tokenize :: Module punkt :: Class PunktSentenceTokenizer A sentence tokenizer which uses an unsupervised algorithm to build a model for abbreviation words, collocations, and words that start sentences; and then uses that model to find sentence boundaries. This approach has been shown to work well for many European languages.
#The NLTK data package includes a pre-trained Punkt tokenizer for English.
import nltk.data

#nltk.tree: Class for representing hierarchical language structures, such as syntax trees and morphological trees.
from nltk import tree 
 
#The nltk.tokenize.regexp module contains several subclasses of RegexpTokenizer that use pre-defined regular expressions: Uses '\w+|[^\w\s]+' 
from nltk import word_tokenize,wordpunct_tokenize


#This module provides regular expression matching operations similar to those found in Perl. Both patterns and strings to be searched can be Unicode strings as well as 8-bit strings.Regular expressions use the backslash character ('\') to indicate special forms or to allow special characters to be used without invoking their special meaning. 
import re 

from string import *

def removepagenumber(x):
    """ this function takes a  string of publications and removes the footerpage string of our given sample CV"""
    update_pageNum_footerpage_tk=RegexpTokenizer('Update\W\s*\d*/\d*/\d*\s*Page\s\d{2}\sof\s\d{2}',gaps=True) 
    pblc_token_footpage_removed= update_pageNum_footerpage_tk.tokenize(x)
    pblcn=''
    for x in range(len(pblc_token_footpage_removed)):
        pblcn+=pblc_token_footpage_removed[x].strip()
    return pblcn 


    
def divide_pubs_bynumber(x):
    """this function divides the string of publications into an array of publications using their numbering"""
    token = RegexpTokenizer('^\n\d+\.\s|^\d+\.\s',gaps=True)
    pblcn_list = token.tokenize(x)
  
    pops=[]
    #remove arrary cells of publication arrary that are empty using pop method of array
    for i in range(len(pblcn_list)):
        if pblcn_list[i] in  '   \n  \n                                                                     ' or pblcn_list[i]=='' or pblcn_list[i]=='  ':
            pops.append(i)
            #print 'to pop',i
    for i in pops:
        pblcn_list.pop(i)
        #print len(pblcn_list)     
    return pblcn_list    




def divide_pubs_intosents(x):
    """this function takes  a list of publications and divide each publication into sentences"""
    pblcn_sent =[]
    #The NLTK data package includes a pre-trained Punkt tokenizer for English.
    sent_detector= nltk.data.load('tokenizers/punkt/english.pickle')

    # divide each publication into its sentences and append them into pblcn_sent
    for i in range(len(x)):
        pblcn_sent.append(sent_detector.tokenize(x[i],realign_boundaries=True))    
    return pblcn_sent



def authors_pubs(x):
    """this function takes a list of publications and extracts authors from publication using regular expressions"""
    #regular expressiong to unify authors in publication
    athr_tk = RegexpTokenizer('(,|;)*[A-Z]{1}\w+\s*[A-Z]{1}\s*\.+(,)+\s+|((,|;)*\s*[A-Z]{1}\w*\s*(,)+\s*([A-Z]{1}\.)+)|(,|;)*\s*[A-Z]{1}\w*\s*(,)+\s*[A-Z]{1}\.*[A-Z]*\.+\s*')  
    startIndex=0
    authors_list=[]
    authors_list_str=[]
    for i in range(len(x)):
        authors_list.append(athr_tk.tokenize(x[i]))
        authors_list_str.append(''.join(authors_list[i]))
    return authors_list,authors_list_str 


def editor_pubs(x):    
    "This function takes a list of publications and extracts editors from publications using regular expressions"
    #regular expressions to unify editors in publication
    edt_tk = RegexpTokenizer('(,|;)*[A-Z]{1}\w+\s*[A-Z]{1}\s*\.+(,)+\s+\(+Eds\.\)+|((,|;)*\s*[A-Z]{1}\w*\s*(,)+\s*([A-Z]{1}\.)+)\(+Eds\.\)+|(,|;)*\s*[A-Z]{1}\w*\s*(,)+\s*[A-Z]{1}\.*[A-Z]*\.+\s*\(+Eds\.\)+')
    editor_list = []
    editor_list_str=[]
    for i in range(len(x)):
        editor_list.append(edt_tk.tokenize(x[i]))
        editor_list_str.append(''.join(editor_list[i]))
    return editor_list,editor_list_str 




def journal_pubs(article_journal_list,headword_list):
    """ this function takes a list of article and journal parts of publications and and a list of keywords and extracts journal parts of the publications by matching the publiications senenteces against a list of common words used in journal parts of publications"""
     
    journal_list=[]
    isHeadword=''
    for i in range(len(article_journal_list)):
        isHeadword='no'
        for j in range(len(article_journal_list[i])):
            if isHeadword=='yes':
                break  
            for k in range(len(headword_list)):    
            
                if headword_list[k].lower() in (article_journal_list[i][j]).lower():
                
                    journal_list.append(' '.join(article_journal_list[i][j:]))
                    #print ''.join(article_journal_list[i][j:])   
                    #print 'the headword is:', headword_list[k], '\n\n'                       
                    isHeadword='yes'
                    break 
                                  
        if isHeadword =='no':
            journal_list.append('Not identified by headwords list')
    return journal_list




def  article_journal_pubs(x,authors_list):
    "this function takes a list of publications and a list of their authors and  extracts the article and journal parts of each publications"
    
    #The NLTK data package includes a pre-trained Punkt tokenizer for English.
    sent_detector= nltk.data.load('tokenizers/punkt/english.pickle')

    article_journal=[]
    article_journal_list= []
    pblcn_withoutAuthor=''
    for i in range(len(x)):
        pblcn_withoutAuthor = x[i]    
        for j in range(len(authors_list[i])):
            pblcn_withoutAuthor=pblcn_withoutAuthor.replace(authors_list[i][j],'')
        article_journal.append(pblcn_withoutAuthor)    
        article_journal_list.append(sent_detector.tokenize(article_journal[i],realign_boundaries=True)) 
    return article_journal,article_journal_list


def article_pubs(x,article_journal,journals_list_str):
    """this function takes a list of publications, a list of their article and journal part, and  a list of their journal part. This function extracts article part of publications by removing authors and journal part of publication"""
    article_list=[]
    article_list_str=[]
    
    for i in range(len(x)):
        findIndex=-1
        findIndex= find( article_journal[i] ,journals_list_str[i])
        if findIndex >= 0:
            article_list_str.append(article_journal[i][:findIndex])
        else: 
            article_list_str.append('not found')                                 
    
    return article_list_str



