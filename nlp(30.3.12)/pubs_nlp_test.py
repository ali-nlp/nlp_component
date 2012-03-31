from pubs_nlp_functions import *
from pdfreader import *


#create a File object in write and read mode, and read name of journals into str obeject.
fp = open('jrnl.txt','r+')
str = fp.read()
journal_list=LineTokenizer(blanklines='discard').tokenize(str)

#create a File object in write and read mode, and read keywords of journals and conferences into str obeject.
fp = open('hdw.txt','r+')
str = fp.read() 
headword_list=LineTokenizer(blanklines='discard').tokenize(str)

pblcn0 = raw_input("Enter your reference to parse: ")




#applying our defined functions on the intended publications section text 

pblcn= removepagenumber(pblcn0)    
    
pblcn_list = divide_pubs_bynumber(pblcn)    

pblcn_sent = divide_pubs_intosents(pblcn_list) 

authors_list,authors_list_str= authors_pubs(pblcn_list)
      
editor_list,editor_list_str= editor_pubs(pblcn_list)

article_journal,article_journal_list= article_journal_pubs(pblcn_list,authors_list)    
    
journals_list = journal_pubs(article_journal_list,headword_list) 

article_list_str= article_pubs(pblcn_list,article_journal,journals_list)




#displays some infomation about publications on the terminal
for i in range(len(pblcn_list)): 
    print '\n\nNext Publication:',i,'\n\n', pblcn_list[i],'\n','Index of authors in this biblography:', pblcn_list[i].find(authors_list_str[i]),'\t','Authors:',  authors_list_str[i] ,'\n\n','article and journal:',article_journal[i],'\n\n','journal:', journals_list[i] ,'\n\n article:   ', article_list_str[i]    



