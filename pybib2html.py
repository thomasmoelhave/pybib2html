#!/usr/bin/python

import sys
import re

def sort_by_year(y, x):
	return int(x[1].fields['year']) - int(y[1].fields['year'])

def replace_all(text, dic):
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text


	

def print_tag(t,extra_args=""):
	if extra_args == "":
		sys.stdout.write("<"+t+">")
	else:
		sys.stdout.write("<"+t+" " + extra_args+">")

def put_header():
	open_tag("head");
	print "<link href=\"http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css\" rel=\"stylesheet\" type=\"text/css\"/>"
	print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js\"></script>"
	print "<script src=\"http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js\"></script>"
  
	print "  <script>"
	print "  $(document).ready(function() {"
	print "    $(\"#accordion\").accordion();"
	print "  });"
	print "  </script>"
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
	html_intag("i",x)

def html_br():
	close_tag("br")
	print ""

def html_a(target,text):
	open_tag("a","href=\""+target+"\"")
	printtex(text)
	close_tag("a")

def printtex_text(t):
	t=re.sub("\\\emph{([a-zA-Z ]*)}","<i>\\1</i>",t)
	t=t.replace("\\o{}","&oslash;")
	t=t.replace("\\ae{}","&aelig;")
	t=t.replace("\\aa{}","&aring;")
	t=t.replace("\\begin{itemize}","<ul>")
	t=t.replace("\\end{itemize}","</ul>")
	t=t.replace("\\item","<li>")
	t=t.replace("{","")
	t=t.replace("}","")
	sys.stdout.write(t)

def printtex_math_cmd_handle_frac(args):
#	sys.stderr.write(args[0])
	sys.stderr.write("\t\t\t\\frac{"+args[0]+"}{"+args[1]+"}\n")
	return	""+args[0]+"/"+args[1]+""

def printtex_math_cmd_handle_mathibf(args):
	sys.stderr.write("\t\t\t\\mathibf{"+args[0]+"}\n")
	return "<strong>"+args[0]+"</strong>"

def printtex_math_cmd_handle_mathrm(args):
	sys.stderr.write("\t\t\t\\mathrm{"+args[0]+"}\n")
	return "</i>"+args[0]+"<i>"

def printtex_math_cmd_handle_sub(args):
	sys.stderr.write("\t\t\t_{"+args[0]+"}\n")
	return "<sub>"+args[0]+"</sub>"

def printtex_math_handlecommand(c,rest):
	commands = {
		"log" : (0,"</i>log<i>"),
		"ell" : (0,"l"),
		"delta" : (0,"&delta;"),
		"sum" : (0,"&sum;"),
		"Theta" : (0,"&Theta;"),
		"Omega" : (0,"&Omega;"),
		"dots" : (0,"..."),
		"mathitbf" : (1,printtex_math_cmd_handle_mathibf),
		"mathbf" : (1,printtex_math_cmd_handle_mathibf),
		"mathrm" : (1,printtex_math_cmd_handle_mathrm),
		"mathop" : (0,""),
		"frac" : (2,printtex_math_cmd_handle_frac),
		"" : (1,printtex_math_cmd_handle_sub), #corresponds to _
	}

	sys.stderr.write("\t\tHANDLING: \"" + c +"\" rest: " + rest + "\n")

	if c in commands:
		(argc,handler)=commands[c]
		if argc==0:
			return (handler,len(c))
		args=[]
		
		#read argc arguments, MUST be enclosed in { }
		args=re.findall(r'{([^{]*)}',rest)[0:argc]
		skip=0
		for a in args:
			skip+=len(a)+2
		return (handler(args),skip+len(c))
	else:
		sys.stderr.write("\t\tunknown function: "+c+"\n")
		return ("",len(c))

		
	


def printtex_math_readcommand(t,i):
	for j in range(i,len(t)):
		if not (t[j].isalpha()):
			return (t[i:j],j)
	return (t[i:len(t)],len(t))
	

def printtex_math(t):
	t=t.replace("<","&lt;")
	t=t.replace(">","&gt;")
	open_tag("i")
#	printtex_math_work(t)
	sys.stderr.write("Handling: \"" +t+"\"\n")
	i=0
	while i < len(t):
		c=t[i]
		sys.stderr.write("\tNext char: t["+str(i)+"]=\""+c+"\"\n")
		if c == "\\" or c == "_":
			(command,unused)=printtex_math_readcommand(t,i+1)
			(result,skip)=	printtex_math_handlecommand(command,t[i:len(t)])
			sys.stderr.write("\thandled \""+t+"\" with command \""+command+"\" and skip " + str(skip)+"\n")
			i+=skip+1 
			sys.stdout.write(result)
			continue
		i+=1
		sys.stdout.write(c)
			
	close_tag("i")


def printtex(t):
	tokens=t.split('$')
	math=False
	for tok in tokens:
			if math:
				printtex_math(tok)
			else:
				printtex_text(tok)
			math=not math

def put_title(value):
	open_tag("h3")
	open_tag("a","href=\"#\"")
	printtex(value.fields['title'])
	close_tag("a")
	close_tag("h3")


def put_title_author(value):
	put_title(value)
	html_br()
	printtex(value.fields['author'])

def new_entry_begin():
	print ""

def new_entry_end():
	print ""


def put_data_line(value,f):
	if f in value.fields:
		html_br()
		html_i(value.fields[f])
		sys.stdout.write(",")
	sys.stdout.write(" "+value.fields['year'])



def handle_default(value):
	new_entry_begin()

	put_title(value)
	open_tag("div")
	printtex(value.fields['author'])

	if 'journal' in value.fields:
		html_br()
		html_i(value.fields['journal'])
		print ","
	if 'howpublished' in value.fields:
		html_br()
		html_i(value.fields['howpublished'])
		print ","
	print value.fields['year']
	close_tag("div")
	new_entry_end()

def handle_article(value):
	new_entry_begin()
	put_title(value)
	open_tag("div")
	printtex(value.fields['author'])
	put_data_line(value,"journal")

	if 'doi' in value.fields:
		html_a("http://dx.doi.org/"+value.fields['doi']," <strong>[DOI]</strong>")

	close_tag("div")
	new_entry_end()


def handle_inproceedings(value):
	new_entry_begin()
	put_title(value)
	open_tag("div")
	printtex(value.fields['author'])
	put_data_line(value,"booktitle")
	if 'doi' in value.fields:
		html_a("http://dx.doi.org/"+value.fields['doi']," <strong>[DOI]</strong>")
	if 'abstract' in value.fields:
		html_br()
		printtex(value.fields['abstract'])

	close_tag("div")
	new_entry_end()

def handle_techreport(value):
	new_entry_begin()
	put_title(value)
	open_tag("div")
	printtex(value.fields['author'])
	put_data_line(value,"institution")
	if 'doi' in value.fields:
		html_a("http://dx.doi.org/"+value.fields['doi']," <strong>[DOI]</strong>")
	close_tag("div")
	new_entry_end()




	
def main():
	from pybtex.database.input import bibtex
	from operator import itemgetter, attrgetter
	import pprint

	parser = bibtex.Parser()
	bib_data = parser.parse_file('mypapers.bib')
	bib_sorted = sorted(bib_data.entries.items(), cmp=sort_by_year)

#	print "<ul>"
	open_tag("html")
	put_header()
	open_tag("body")
	handlers = {'article':handle_article,'inproceedings':handle_inproceedings,'techreport':handle_techreport}
	
	open_tag("div","id=\"accordion\"")
	for key, value in bib_sorted:
		bibtex_class = value.type
		if (bibtex_class in handlers):
			handlers[bibtex_class](value)
		else:
			sys.stderr.write("No handler for: " + bibtex_class+", using default\n")
			handle_default(value)

	close_tag("div")
	#print "</ul>"


	html_br()
	print "<small>Generated by "
	html_a("https://github.com/thomasmoelhave/pybib2html","pybib2html")

	close_tag("body")
	close_tag("html")

main()
