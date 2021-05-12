# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:10:00 2021

@author: aw
"""

#from urllib.request import urlopen
import urllib.request
from lxml import etree as ET
import xmltodict
from io import StringIO

after = '20201001' # load date
before = '20201231' # load date
pubyear_after = '2019' #
api_key = 'xxxxxxxx'
view = 'COMPLETE' # COMPLETE shows more

headers = {'Content-Type': 'application/xml'}

## AFFIL(((kth*) OR (roy* AND inst* AND tech*) OR ("Roy. Inst. T") OR (alfven) OR (kung* AND tek* AND hog*) OR (kung* AND tek* AND hög*) OR (kgl AND tek* AND hog*) OR (kung* AND tek* AND hg*) OR (roy* AND tech* AND univ*)) AND (Sweden)) OR AF-ID("The Royal Institute of Technology KTH" 60002014) AND orig-load-date aft 20180930 AND pubyear aft 2008
## https://api.elsevier.com/content/search/scopus?query=AFFIL(((kth*)+OR+(roy*+AND+inst*+AND+tech*)+OR+(%22Roy.+Inst.+T%22)+OR+(alfven)+OR+(kung*+AND+tek*+AND+hog*)+OR+(kung*+AND+tek*+AND+h%C3%B6g*)+OR+(kgl+AND+tek*+AND+hog*)+OR+(kung*+AND+te*k+AND+h%C3%B6g*)+OR+(roy*+AND+tech*+AND+univ*))+AND+(Sweden))+OR+AF-ID(%22The+Royal+Institute+of+Technology+KTH%22+60002014)+AND+orig-load-date+aft+20210110+AND+orig-load-date+bef+20210114+pubyear+aft+2019&apiKey=acbc3cee2bc16c2ff2260a04d8b6a4bd&view=COMPLETE

## add truncation check! kolla ö
url = 'https://api.elsevier.com/content/search/scopus?query=AFFIL%28%28%28kth%2A%29+' \
             + 'OR+%28roy%2A+AND+inst%2A+AND+tech%2A%29+' \
             + 'OR+%28%22Roy.+Inst.+T%22%29+' \
             + 'OR+%28alfven%29+' \
             + 'OR+%28kung%2A+AND+tek%2A+AND+hog%2A%29+' \
             + 'OR+%28kung%2A+AND+tek%2A+AND+h%C3%B6g%2A%29+' \
             + 'OR+%28kgl+AND+tek%2A+AND+hog%2A%29+' \
             + 'OR+%28kung%2A+AND+te%2Ak+AND+h%C3%B6g%2A%29+' \
             + 'OR+%28roy%2A+AND+tech%2A+AND+univ%2A%29%29+' \
             + 'AND+%28Sweden%29%29+' \
             + 'OR+AF-ID%28%22The+Royal+Institute+of+Technology+KTH%22+60002014%29+' \
             + 'AND+orig-load-date+aft+' + after \
             + '+AND+orig-load-date+bef+' + before \
             + '+pubyear+aft+' + pubyear_after \
             + '&apiKey=' + api_key \
             + '&view=' + view

q = urllib.request.Request(url)
q.add_header('Accept', 'application/xml')
r = urllib.request.urlopen(q).read().decode("utf-8")   ###  this is the search, output = type str
## d = xmltodict.parse(r, dict_constructor=dict)   ### change type to dict - optional
print(r)
    
ns = {'prism': 'http://prismstandard.org/namespaces/basic/2.0/', 'opensearch': 'http://a9.com/-/spec/opensearch/1.1/', 'dc': 'http://purl.org/dc/elements/1.1/', 'atom': 'http://www.w3.org/2005/Atom'}
## u = "<search-results>"  ## this is to be put in the top of the concatenated file
u = '<search-results xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/" xmlns:atom="http://www.w3.org/2005/Atom">'
s = r[r.find('<entry>'):] ## removing everything from r before the first <entry> tag
u += s  ## concatenating u and s
print(u)


### STOP READING HERE - BELOW IS GIBBERISH


##### https://www.datacamp.com/community/tutorials/python-xml-elementtree #####

tree = ET.parse(u)
root = tree.getroot()
root.tag  ## gives search-results which is ok
root.attrib ## gives {} which is ok since root has no attributes

for child in root[4]:  ## we look at the fifth child under root
    print(child.tag, child.attrib)
    
[elem.tag for elem in root.iter()]  ## looping over the whole tree
[elem.tag for elem in root.iter('{http://www.w3.org/2005/Atom}surname')]  ## looping over the whole tree

print(ET.tostring(root, encoding='utf8').decode('utf8')) ###

for surname in root.iter('{http://www.w3.org/2005/Atom}surname'):  ## get all surnames
    print(surname.text)

for title in root.iter('{http://purl.org/dc/elements/1.1/}title'):
    print(title.text)
    
###############################################################################################################
###  https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree?rq=1 ###

for title in root.iter('dc:title', ns):
    print(title.text)




## tree = ET.parse(StringIO(u))
tree = ET.parse(u)
root = tree.getroot()
root.tag[0][6]
root.attrib[0][6]

print(tree)

zz = root[0][6]
print(zz).text
    
for item in root.findall('./entry'):
        item.find('dc:title', ns).text
     

for movie in root.findall("./entry/author/movie/[year='1992']"):
        print(movie.attrib)
        
for child in root:
        print(child.tag, child.attrib)
   
for affilname in root.iter('affilname'):
        print(affilname).text

items = root.findall('prism:doi', ns)
type(items)

"""
for child in root:
     print(child.tag, child.attrib)

[elem.tag for elem in root.iter()]

print(ET.tostring(root, encoding='utf8').decode('utf8'))



items = root.findall('prism:doi', namespaces)
type(items)

print(root.findtext('prism:doi', namespaces)) ## why doesn't this work out?

### https://stackabuse.com/introduction-to-the-python-lxml-library/
### https://www.geeksforgeeks.org/xml-parsing-python/

if len(root) > 0:
     print("True")
else:
     print("False")

for i in range(len(root)):
     if (len(root[i]) > 0):
         print("True")
     else:
         print("False")

for i in range(len(root)):
     print(ET.iselement(root[i]))


print(root.getnext())

print(root.findtext('prism:doi', namespaces))
### -------------------------------------------------------------------- ###



w = etree.parse(StringIO(u))

tree = etree.parse(url)

root = tree.getroot()
tree = etree.fromstring(d)

root = ET.parse(r).getroot()
print(root)
print('\n')


print()

###  https://dnmtechs.com/en/python-newbie-parse-xml-from-api-call/
items = root.findall('items')
for item in items:
      item.find('title').text # should print: <![CDATA[Heroes Season 4 Subtitles]]>
      item.find('link').text # Should print: http://www.allsubs.org/subs-download/heroes+season+4/1223435/

items = root.findall('entry')
for entry in items:
      item.find('dc:title', namespaces).text # should print: <![CDATA[Heroes Season 4 Subtitles]]>
      item.find('prism:doi', namespaces).text # Should print: http://www.allsubs.org/subs-download/heroes+season+4/1223435/

print(items)

"""

