#!/usr/bin/python

import sys

def sort_by_year(y, x):
	return int(x[1].fields['year']) - int(y[1].fields['year'])

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
	sys.stdout.write(t)

def print_tag(t,extra_args=""):
	if extra_args == "":
		sys.stdout.write("<"+t+">")
	else:
		sys.stdout.write("<"+t+" " + extra_args+">")

def open_tag(t, args=""):
	print_tag(t,args)

def close_tag(t):
	print_tag('/'+t)

def html_intag(t,x):
	open_tag(t)
	printtex(x)
	close_tag(t)

def html_strong(x):
	html_intag("strong",x)

def html_i(x):
	html_intag("i",x)

def html_br():
	close_tag("br")
	print ""

def html_a(target,text):
	open_tag("a","href=\""+target+"\"")
	printtex(text)
	close_tag("a")

def put_title_author(value):
	html_strong(value.fields['title'])

	if 'doi' in value.fields:
		html_a("http://dx.doi.org/"+value.fields['doi']," <strong>[DOI]</strong>")

	html_br()

	printtex(value.fields['author'])

def new_entry_begin():
	open_tag("li")

def new_entry_end():
	close_tag("li")

def put_data_line(value,f):
	if f in value.fields:
		html_br()
		html_i(value.fields[f])
		sys.stdout.write(",")
	sys.stdout.write(" "+value.fields['year'])



def handle_default(value):
	new_entry_begin()

	put_title_author(value)

	if 'journal' in value.fields:
		html_br()
		html_i(value.fields['journal'])
		print ","
	if 'howpublished' in value.fields:
		html_br()
		html_i(value.fields['howpublished'])
		print ","
	print value.fields['year']
	new_entry_end()

def handle_article(value):
	new_entry_begin()
	put_title_author(value)
	put_data_line(value,"journal")
	new_entry_end()


def handle_inproceedings(value):
	new_entry_begin()
	put_title_author(value)
	put_data_line(value,"booktitle")
	new_entry_end()

def handle_techreport(value):
	new_entry_begin()
	put_title_author(value)
	put_data_line(value,"institution")
	new_entry_end()




	
def main():
	from pybtex.database.input import bibtex
	from operator import itemgetter, attrgetter
	import pprint
	parser = bibtex.Parser()
	bib_data = parser.parse_file('mypapers.bib')
	bib_sorted = sorted(bib_data.entries.items(), cmp=sort_by_year)

	print "<ul>"

	handlers = {'article':handle_article,'inproceedings':handle_inproceedings,'techreport':handle_techreport}
	
	for key, value in bib_sorted:
		bibtex_class = value.type
		if (bibtex_class in handlers):
			handlers[bibtex_class](value)
		else:
			sys.stderr.write("No handler for: " + bibtex_class+", using default\n")
			handle_default(value)

	print "</ul>"

	print "<small>Generated by "
	html_a("https://github.com/thomasmoelhave/pybib2html","pybib2html")


main()
