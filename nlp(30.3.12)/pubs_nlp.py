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

#create a File object in write and read mode, and read CV
fp = open('cv1.txt','r+')
cv1 =fp.read()

# convert pdf to string by pdfminer library.
#cv1 = convert_pdf('OCGS CV, Nov 2011_long.pdf')


#find the section of inteneded publications, and it's starting and finishing index, and slice that paricular part from the whole CV 
lindex = cv1.find('Papers in Refereed Conference Proceedings');
uindex = cv1.find('Papers in refereed journals (submitted):');
llen= len('Papers in Refereed Conference Proceedings');
ulen= len('Papers in refereed journals (submitted):');
lindex = lindex+ llen
uindex = uindex- ulen
pblcn0= cv1[lindex:uindex]



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



