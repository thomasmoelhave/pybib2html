#!/usr/bin/python

import sys
import re
import os.path

publication_counter=1
output_file=sys.stdout
author_data = dict()

def sort_by_year(y, x):
	xyear = int(x[1].fields['year']) 
	yyear = int(y[1].fields['year'])
	if xyear != yyear:
		return xyear - yyear
	
	#same year, sort by month if possible
	if 'month' in x[1].fields and 'month' in y[1].fields:
		xmonth = int(x[1].fields['month']) 
		ymonth = int(y[1].fields['month'])
		if xmonth != ymonth:
			return xmonth - ymonth

	return x[0] < y[0]

def print_output(s):
	global output_file
	output_file.write(s)


def replace_all(text, dic):
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text

def print_tag(t,extra_args=""):
	if extra_args == "":
		print_output("<"+t+">")
	else:
		print_output("<"+t+" " + extra_args+">")

def put_header():
	open_tag("head");
	print_output("<script src=\"http://code.jquery.com/jquery-1.5.1.js\"></script>\n")
	print_output("<script type=\"text/javascript\" src=\"showhide.js\"> </script>")
	print_output("<link href=\"style.css\" type=text/css rel=stylesheet>\n")
	close_tag("head");


def open_tag(t, args=""):
	print_tag(t,args) 

def close_tag(t):
	print_tag('/'+t)

def html_intag(t,x,args=""):
	open_tag(t,args)
	printtex(x)
	close_tag(t)

def html_strong(x):
	html_intag("strong",x)

def html_h3(x):
	html_intag("h3",x)

def html_i(x):
	html_intag("em",x)

def html_br():
	print_tag("br/")

def html_a(target,text):
	open_tag("a","href=\""+target+"\"")
	printtex(text)
	close_tag("a")

def open_div():
	open_tag("div")

def open_div(classname=None):
	if classname is None:
		open_tag("div")
	else:
		open_tag("div","class=\""+classname+"\"")

def open_span(classname):
	open_tag("span","class=\""+classname+"\"")

def close_span():
	close_tag("span")


def close_div():
	close_tag("div")
	print_output("\n\n")


def printtex_replace_command(t,command,newtext,argc,commandprefix="\\\\"):
	#e.g. t="bla blac \frac{x}{y}", command=frac arg_map=\\1 / \\2
	parseargs=""
	
	for i in range(0,argc):
		parseargs+="{([^{]*)}"
	
	pattern=commandprefix+command+parseargs

	return re.sub(pattern,newtext,t)



def printtex_text(t):
	### remove comments
	t=t.replace("\\%","&#37;") #first get rid of actual %'s in the input
	t=re.sub("%.*","",t) #the remaining %'s are comments

	t=printtex_replace_command(t,"emph","<em>\\1</em>",1)
	
	t=t.replace("\\&","&amp;") #first get rid of actual %'s in the input
	t=t.replace("\\o{}","&oslash;")
	t=t.replace("\\o{}","&oslash;")
	t=t.replace("\\ae{}","&aelig;")
	t=t.replace("\\aa{}","&aring;")
	t=t.replace("\\begin{itemize}","<ul>")
	t=t.replace("\\end{itemize}","</ul>")
	t=t.replace("\\item","<li>")
	t=t.replace("{","")
	t=t.replace("~"," ")
	t=t.replace("}","")
	t=t.replace("\\-","-")
	t=t.replace("---","&mdash;")
	#print_output(t)
	return t


def printtex_math(t):
	t=t.replace("<","&lt;")
	t=t.replace(">","&gt;")
	t=t.replace("\delta","&delta;")
	t=t.replace("\dots","...")
	t=t.replace("\Theta","&Theta;")
	t=t.replace("\Omega","&Omega;")
	t=t.replace("\log","</em>log<em>")
	t=t.replace("\ell","l")
	t=printtex_replace_command(t,"mathitbf","<strong>\\1</strong>",1)
	t=printtex_replace_command(t,"mathbf","<strong>\\1</strong>",1)
	t=printtex_replace_command(t,"mathrm","</em>\\1<em>",1)
	t=printtex_replace_command(t,"frac","\\1/\\2",2)
	t=printtex_replace_command(t,"_","<sub>\\1</sub>",1,"")
	open_tag("em")
	print_output(t)
	close_tag("em")

def printtex(t):
	tokens=t.split('$')
	math=False
	for tok in tokens:
			if math:
				printtex_math(tok)
			else:
				print_output(printtex_text(tok) )
			math=not math

def put_title(value):
	print_output("\n\n<!-- - - - - - - NEW PAPER - - - - - - - - -->\n\n\n")
	open_span("papertitle")
	if 'note' in value.fields:
		open_span('paper-note')
		print_output(value.fields['note'])
		close_span()
	printtex(value.fields['title'])
	close_span() 
	html_br()
	print_output("\n")

def put_image(key):
	#Look for fig/key.{png,jpg}
	prefix="paper_figs/"

	key_underscore=key.replace(':','_')

	png_path=prefix+key_underscore+".png"
	jpg_path=prefix+key_underscore+".jpg"
	
	path=""

	if os.path.isfile(png_path):
		path=png_path
	if os.path.isfile(jpg_path):
		path=jpg_path

	if path != "":
		open_tag("img","src=\""+path+"\" alt=\"Figure for"+key_underscore+"\""+"width=\"80\" height=\"80\"")
		close_tag("img")
		print "Image for " + key + ": " + path
	else:
		print "Image for " + key + " not found."


def put_title_author(value,key):
	put_title(value)
	put_image(key)
	print_authors(value)



def new_entry_end(key,value):
	print_output("\n<!-- END ENTRY -->\n")


def new_entry_begin(key,value):
	print_output("\n<!-- NEW ENTRY -->\n")


def put_data_line(value,f,f2=""):
	open_div("paper-data")
	if f in value.fields:
		html_i(value.fields[f]+"")
		print_output(",")
	print_output(" "+value.fields['year']+".")
	close_div()

def put_details(value):
	
	if 'abstract' not in value.fields and 'doi' not in value.fields:
		return

	open_hidden_div()
	if 'abstract' in value.fields:
		print_abstract(value)
	print_doi(value)
	close_hidden_div()

def print_authors(value):
	global author_data

	open_div("paper-authors")
	firstPerson=True
	for p in value.persons.items()[0][1]:
		if not firstPerson:
			print_output(", ")
		else:
			firstPerson=False
		name=""
		first=True
		for f in p.first():
			name+=f+" "
		for f in p.middle():
			name+=f+" "
		for f in p.last():
			name+=f+" "

		link=None
		for pattern in author_data:
			link_=author_data[pattern]
			if re.search(pattern,name) != None:
				link=link_

		if link==None:
			print_output(printtex_text(name[0:len(name)-1]))
			sys.stderr.write("No link for: " + name + "\n")
		else:
			print_output('<a href=\"'+link+'\">')
			print_output(printtex_text(name[0:len(name)-1]))
			print_output('</a>')

	print_output(".")
	close_div()

def print_doi(value):
	if 'doi' in value.fields:
		html_intag("strong","DOI: ")
		doi=value.fields['doi']
		print_output(" ")
		html_a("http://dx.doi.org/"+doi, "["+doi+"]")

def read_author_data(filename):
	f=open(filename)
	global author_data
	for l in f:
		test=l.split('=') # format is "author pattern"="email"
		if len(test)!=2:
			if (l != ""):
				sys.stderr.write("Skipping author data line: " + l + "\n")
			continue
		name=test[0]
		url=test[1]
			
		url=url.rstrip('\n')
		author_data[name]=url

def open_hidden_div():
	global publication_counter
	p=str(publication_counter)
	open_div()
	print_output("<div class=\"module-det mod" + p + "\" style=\"display:none;\">")

def close_hidden_div():
	global publication_counter
	p=str(publication_counter)
	close_div()
	close_div()
	print_output("<a class=\"details-less detl" + p +"\" href=\"javascript:;\" onClick=\"details("+p+")\" id=\"hide_mod"+p+"\" style=\"display:none;\">hide details</a> <a class=\"details-more detm"+p+"\" href=\"javascript:;\" onClick=\"details("+p+")\" id=\"show_mod"+p+"\">read details</a>")

	
def handle_default(key,value):
	new_entry_begin(key,value)

	put_title_author(value,key)
	if 'journal' in value.fields:
		html_i(value.fields['journal'])
	if 'howpublished' in value.fields:
		html_i(value.fields['howpublished'])
	print_output(",")
	print_output(value.fields['year']+".")

	put_details(value)

	new_entry_end(key,value)

def handle_article(key,value):
	new_entry_begin(key,value)
	put_title_author(value,key)
	put_data_line(value,"journal")
	put_details(value)
	new_entry_end(key,value)

def print_abstract(value):
	html_intag("strong","Abstract:")
	open_div("paper-abstract")
	printtex(value.fields['abstract'])
	close_div()

def handle_phdthesis(key,value):
	new_entry_begin(key,value)
	put_title_author(value,key)
	put_data_line(value,"school")
	put_details(value)
	new_entry_end(key,value)

def handle_inproceedings(key,value):
	new_entry_begin(key,value)
	put_title_author(value,key)
	put_data_line(value,"booktitle")
	put_details(value)
	new_entry_end(key,value)

def handle_techreport(key,value):
	new_entry_begin(key,value)
	put_title_author(value,key)
	put_data_line(value,"institution","number")
	put_details(value)
	new_entry_end(key,value)

def handle_values(l,use_key_only):
	global publication_counter
	l_sorted = sorted(l, cmp=sort_by_year)
	handlers = {'article':handle_article,'inproceedings':handle_inproceedings,'techreport':handle_techreport,'phdthesis':handle_phdthesis}
	for key, value in l_sorted:
		if use_key_only=="" or ("key" in value.fields and value.fields["key"]==use_key_only):
			bibtex_class = value.type
			open_tag("li")
			if (bibtex_class in handlers):
				handlers[bibtex_class](key,value)
			else:
				sys.stderr.write("No handler for: " + bibtex_class+", using default\n")
				handle_default(key,value)
			close_tag("li")
			publication_counter+=1

def handle_types(list_of_types,typemaps, description,use_key_only=""):
	print_output("<h3>"+description+"</h3>")
	open_tag("ol","start=\""+str(publication_counter)+"\"")
	for l in list_of_types:
		handle_values(typemaps[l],use_key_only)
	close_tag("ol")
	
def main():
	import getopt
	options,remainder=getopt.getopt(sys.argv[1:], 'i:o:a:',['input=','output=',"authors="])


	from pybtex.database.input import bibtex
	from operator import itemgetter, attrgetter
	import pprint

	parser = bibtex.Parser()
	#bib_data = parser.parse_file('mypapers.bib')
	global output_file
	for opt,arg in options:
		if opt in ('-o', '--output'):
			output_file = open(arg,'w')
		if opt in ('-i', '--input'):
			input_filename = arg
		if opt in ('-a', '--authors'):
			author_filename = arg
			read_author_data(author_filename)

	bib_data = parser.parse_file(input_filename)

	from collections import defaultdict
	typemaps=defaultdict(list)

	for key, value in bib_data.entries.items():
		bibtex_class = value.type
		typemaps[bibtex_class].append((key,value))


	open_div("paper")
	handle_types(["phdthesis"],typemaps,"Dissertation")
	handle_types(["inproceedings"],typemaps,"Conference Papers")
	handle_types(["article"],typemaps,"Journal Papers","journal")
	handle_types(["article","techreport"],typemaps,"Other Papers","other")
	handle_types(["misc"],typemaps,"Abstracts")
	close_div()


	print_output("<script>$(\".details-more\").click(details); $(\".details-less\").click(details)</script>")
	# html_br()
	# print_output("<small>Generated by ")
	# html_a("https://github.com/thomasmoelhave/pybib2html","pybib2html")
	# print_output("</small>")

main()

