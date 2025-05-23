import re
import os
import shutil

# helper for writing the changes into the files
def write_modified(func,path):
    with open(path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        # Replace characters between # symbols
        modified_content = func(html_content)
        # Write the modified content back to the file
        with open(path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        file.close()
            
# redact the wiki text between pairs of #
def redact(og_content):
    def replace_between_symbols(html_content):
        pattern = r"#([\w\.\,\:\;\s\'\/\"\-\’\[\]\<\>\=\@\!\$\%\^\&\*\(\)\/]*)#"
        replaced_content = re.sub(pattern, repl, html_content)
        return replaced_content

    def repl(match):
        def find(s, ch):
            return [i for i, ltr in enumerate(s) if ltr == ch]
        indecies = find(match.group(0)," ")
        rtn = '█' * len(match.group(0))
        for i in indecies:
            rtn = rtn[:i] + " " + rtn[i + 1:]
        return rtn

    return replace_between_symbols(og_content)

# put the block content tags and prepare for template insertion
def django_template_blockify(og_content):
    repl1 = "{% extends \"wiki/wiki-base.html\" %}{% block content %}" + "\n"
    pattern1 = r"<([\w\.\,\:\;\s\'\/\"\-\’\[\]\<\>\=\@\!\$\%\^\&\*\(\)\/]*)(<body class=\"wikidpad\">)"
    
    repl2 = "{% endblock content %}"
    pattern2 = r"(<\/body>)\s\S*(<\/html>)"
    def replace_between_symbols(pattern, repl, html_content):
        replaced_content = re.sub(pattern, repl, html_content)
        return replaced_content
    decapitated = replace_between_symbols(pattern1,repl1,og_content)
    return replace_between_symbols(pattern2, repl2, decapitated)


   
def rename_and_relocate(file):
   os.replace(file,os.getcwd()+"\\"+file.name.replace("%27",""))



dir = r"C:\\Users\\Myles\\Documents\\Ethos Project\\Ethos-Project\\Wiki\\Seven Spheres\\HTML"
#dir = os.getcwd()
curr_dir = os.getcwd()
for file in os.scandir(dir):
    
    if file.name == "WikiSettings.html":
        os.remove(file)
    elif file.name == "ScratchPad.html":
        os.remove(file)
    elif "Template" in file.name:
        os.remove(file)
    elif file.name.endswith(".html"):
        write_modified(redact, file)
        rename_and_relocate(file)
try:
    shutil.rmtree(os.getcwd()+"\\files")
except:
    pass
shutil.move(dir+"\\files",os.getcwd())