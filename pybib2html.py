#!/usr/bin/python

import sys
import re

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
#	print_output("<link href=\"http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css\" rel=\"stylesheet\" type=\"text/css\"/>"
#	print_output("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js\"></script>"
#	print_output("<script src=\"http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js\"></script>"
  
	#print_output("  <script>"
	#print_output("  $(document).ready(function() {"
	#print_output("    $(\"#accordion\").accordion();"
	#print_output("  });"
	#print_output("  </script>"
	print_output("<script src=\"http://code.jquery.com/jquery-1.4.4.js\"></script>\n")
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
	open_tag("strong")
#	open_tag("a","href=\"#\"")
	printtex(value.fields['title'])
	if 'note' in value.fields:
		print_output(' <small><font color=\"red\">' + value.fields['note'] + "</font></small>")
#	close_tag("a")
	close_tag("strong")


def put_title_author(value):
	put_title(value)
	html_br()
	print_authors(value)

def new_entry_end(key,value):
	print value.fields["year"]
	print value.fields.items()

	#print "@"+value.fields['type']+" {" + key +","

	if	"abstract" in value.fields:
		key=key.replace(":","__")
		print_output("<small><a href=\"#"+key+"\" id=\"hide_"+key+"\">Hide Details</a> / \n")
		print_output("<a href=\"#"+key+"\" id=\"show_"+key+"\">Show Details</a></small>\n")
		print_output("<script>\n")
		print_output("$(\"#hide_"+key+"\").click(function () {\n")
		print_output("  $(\"."+key+"\").hide(\"fast\", function () {\n")
		print_output("    // use callee so don't have to name the function\n")
		print_output("    $(this).prev().hide(\"normal\", arguments.callee); \n")
		print_output("  });\n")
		print_output("});\n")
		print_output("$(\"#show_"+key+"\").click(function () {\n")
		print_output("  $(\"."+key+"\").show(200);\n")
		print_output(" });\n")
		print_output("</script>\n")

def new_entry_begin(key,value):
	print_output("")


def put_data_line(value,f,f2=""):
	if f in value.fields:
		html_br()
		html_i(value.fields[f])
		print_output(",")
		if f2 in value.fields:
			html_i(" "+value.fields[f2])
			print_output(",")
	print_output(" "+value.fields['year']+".")

def print_authors(value):
	global author_data

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

def print_doi(value):
	if 'doi' in value.fields:
		html_intag("strong","DOI: ")
		html_br()
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
	
def handle_default(key,value):
	new_entry_begin(key,value)

	put_title_author(value)
	if 'journal' in value.fields:
		html_br()
		html_i(value.fields['journal'])
	if 'howpublished' in value.fields:
		html_br()
		html_i(value.fields['howpublished'])
	print_output(",")
	print_output(value.fields['year']+".")

	open_tag("div")
	open_tag("div","class=\""+key.replace(":","__")+"\" style=\"display:none;\"")
	if 'abstract' in value.fields:
		print_abstract(value)
	close_tag("div")
	close_tag("div")

	
	new_entry_end(key,value)

def handle_article(key,value):
	new_entry_begin(key,value)
	put_title_author(value)
	put_data_line(value,"journal")
	print_doi(value)
	new_entry_end(key,value)

def print_abstract(value):
	html_intag("strong","Abstract:")
	html_br()
	printtex(value.fields['abstract'])
	html_br()


def handle_phdthesis(key,value):
	new_entry_begin(key,value)
	put_title_author(value)
	put_data_line(value,"school")
	open_tag("div")
	open_tag("div","class=\""+key.replace(":","__")+"\" style=\"display:none;\"")
	if 'abstract' in value.fields:
		print_abstract(value)
	close_tag("div")
	close_tag("div")
	new_entry_end(key,value)

def handle_inproceedings(key,value):
	new_entry_begin(key,value)
	put_title_author(value)
	put_data_line(value,"booktitle")
	open_tag("div")
	open_tag("div","class=\""+key.replace(":","__")+"\" style=\"display:none;\"")
	if 'abstract' in value.fields:
		print_abstract(value)
	print_doi(value)
	close_tag("div")
	close_tag("div")
	new_entry_end(key,value)

def handle_techreport(key,value):
	new_entry_begin(key,value)
	put_title_author(value)
	put_data_line(value,"institution","number")
	open_tag("div")
	open_tag("div","class=\""+key.replace(":","__")+"\" style=\"display:none;\"")
	if 'abstract' in value.fields:
		print_abstract(value)
	print_doi(value)
	close_tag("div")
	close_tag("div")
	new_entry_end(key,value)

def handle_values(l):
	global publication_counter
	l_sorted = sorted(l, cmp=sort_by_year)
	handlers = {'article':handle_article,'inproceedings':handle_inproceedings,'techreport':handle_techreport,'phdthesis':handle_phdthesis}
	for key, value in l_sorted:
		bibtex_class = value.type
		open_tag("li")
		if (bibtex_class in handlers):
			handlers[bibtex_class](key,value)
		else:
			sys.stderr.write("No handler for: " + bibtex_class+", using default\n")
			handle_default(key,value)
		close_tag("li")
		html_br()
		publication_counter+=1

def handle_types(list_of_types,typemaps, description):
	print_output("<strong>"+description+"</strong>")
#	open_tag("div","id=\"accordion\"")
	open_tag("ol","start=\""+str(publication_counter)+"\"")
	for l in list_of_types:
		handle_values(typemaps[l])
	close_tag("ol")

#	close_tag("div")


	
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

	open_tag("html")
	put_header()
	open_tag("body")

	from collections import defaultdict
	typemaps=defaultdict(list)

	for key, value in bib_data.entries.items():
		bibtex_class = value.type
		typemaps[bibtex_class].append((key,value))

	
	handle_types(["phdthesis"],typemaps,"Dissertation")
	handle_types(["inproceedings"],typemaps,"Conference Papers")
	handle_types(["article","techreport"],typemaps,"Other Papers")
	handle_types(["misc"],typemaps,"Abstracts")


	html_br()
	print_output("<small>Generated by ")
	html_a("https://github.com/thomasmoelhave/pybib2html","pybib2html")
	print_output("</small>")

	close_tag("body")
	close_tag("html")

main()

