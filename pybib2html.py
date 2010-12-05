#!/usr/bin/python
from pybtex.database.input import bibtex
from operator import itemgetter, attrgetter
import pprint
parser = bibtex.Parser()
bib_data = parser.parse_file('mypapers.bib')

def sort_by_year(y, x):
	return int(x[1].fields['year']) - int(y[1].fields['year'])

bib_sorted = sorted(bib_data.entries.items(), cmp=sort_by_year)

print "<ul>"

def replace_all(text, dic):
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text


def printtex(t):
	t=t.replace("\\o{}","&oslash;")
	t=t.replace("\\ae{}","&aelig;")
	t=t.replace("\\aa{}","&aring;")
	t=t.replace("{","")
	t=t.replace("}","")
	print t

def opentag(t, args=""):
	print "<"+t+" " + args+" >"
def closetag(t):
	print "</"+t+">"

def html_intag(t,x):
	opentag(t)
	printtex(x)
	closetag(t)

def html_strong(x):
	html_intag("strong",x)

def html_i(x):
	html_intag("i",x)

def html_br():
	closetag("br")

def html_a(target,text):
	opentag("a","href=\""+target+"\"")
	printtex(text)
	closetag("a")
	

for key, value in bib_sorted:
	print "<li>"
#	print key
	html_strong(value.fields['title'])
	html_br()
	printtex(value.fields['author'])

	if 'booktitle' in value.fields:
		html_br()
		html_i(value.fields['booktitle'])
		print ","
	if 'journal' in value.fields:
		html_br()
		html_i(value.fields['journal'])
		print ","
	
	print value.fields['year']

	if 'doi' in value.fields:
		html_a("http://dx.doi.org/"+value.fields['doi'],"DOI")


	#if 'abstract' in value.fields:
	#	print value.fields['abstract']

print "</li>"

print "</ul>"
