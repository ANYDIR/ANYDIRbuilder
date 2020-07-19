import markdown2
from slugify import slugify
import os

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input", default="input",
                    help="Folder to use as the input")
parser.add_argument("-o", "--output", dest="output", default="output",
                    help="Folder to use as the output")
parser.add_argument("-repo", "--repourl", dest="repo", default="https://github.com/anydir/anydir.github.io/blob/wiki/",
                    help="URL to use for repos")
parser.add_argument("-crumbs", "--crumburl", dest="link", default="https://anydir.github.io/",
                    help="URL to use for crumbs and page links")

args = parser.parse_args()

config = {
    "titleprefix": "ANYDIR - ",
    "linkprefix": args.repo,
    "crumbprefix": args.link, # for the crumb links,
    "contentsformat": "\n<br>\n<a href=\"#{}\"><div class=\"djh-item{}\">{}</div></a>", # first is the slug link, second is how many sublevels, third is what the title is
    "breadcrumb": " <div class=\"breadcrumb\">></div> ",
    "inputfolder": args.input,
    "outputfolder": args.output,
    "bottomlevelfancy": "Index"
}

sublevels = ['', ' djh-subitem1', ' djh-subitem2', ' djh-subitem3', ' djh-subitem4', ' djh-subitem5', ' djh-subitem6']

for subdir, dirs, files in os.walk(config["inputfolder"]):
    for file in files:
        if file.endswith(".md") and not subdir.startswith("{}/.git".format(config["inputfolder"])):
            filepath = os.path.join(subdir, file)
            print("Processing {}...".format(filepath))
            # contents header
            contents = "<br>\n<b>CONTENTS</b>"

            # Get the template to use for writing
            with open("template/base.html", "r") as currentfile:
                htmlshell = currentfile.read()

            # placeholder page name
            pagetitle = "{}{}".format(config["titleprefix"], "Unnamed Page")

            # placeholder breadcrumbs
            breadcrumbs = ""

            # Get the markdown file to put into the template, and convert that to html
            with open("{}".format(filepath), "r") as currentfile:
                # Generate the content
                pagecontent = markdown2.markdown(currentfile.read(), extras=["header-ids"])

                # Find the pagetitle
                currentfile.seek(0)

                for line in currentfile:
                    if line.startswith("# "):
                        pagetitle = "{}{}".format(config["titleprefix"], line[2:])
                        break

                # Create contents sidebar
                currentfile.seek(0)

                for line in currentfile:

                    # yes I know this code is awful but it works for now
                    if line.startswith("## "):
                        contents += config["contentsformat"].format(slugify(line[3:]), sublevels[1], line[3:])
                    if line.startswith("### "):
                        contents += config["contentsformat"].format(slugify(line[4:]), sublevels[2], line[4:])
                    if line.startswith("#### "):
                        contents += config["contentsformat"].format(slugify(line[5:]), sublevels[3], line[5:])
                    if line.startswith("##### "):
                        contents += config["contentsformat"].format(slugify(line[6:]), sublevels[4], line[6:])
                    if line.startswith("###### "):
                        contents += config["contentsformat"].format(slugify(line[7:]), sublevels[5], line[7:])


            # create breadcrumbs
            if os.path.split(filepath)[0] != "":
                print(" ")
                print("Making breadcrumbs for {}...".format(filepath))
                tempfilepath = os.path.split(filepath)[0].split("/")

                for index, folder in enumerate(tempfilepath):
                    print(" ")
                    print("index: {}/{}".format(index, len(tempfilepath)))
                    print("IndexName: {}".format(filepath[-8:]))

                    print(filepath[-8:] == "index.md" and index != len(tempfilepath) - 1)


                    if index != 0:
                        breadcrumbs += config["breadcrumb"]
                    print("Crumb link: {}{}".format(config["crumbprefix"], "/".join(tempfilepath[1:(index + 1)])))
                    print("Crumb folder: {}{}".format(config["inputfolder"] ,"/".join(tempfilepath[1:(index + 1)])))


                    # Get the fancy name for a breadcrumb
                    fancycrumb = "ERR_NOINDEX"
                    if "/".join(tempfilepath[1:(index + 1)]) == "":
                        crumbindexpath = "{}/index.md".format(config["inputfolder"])
                    else:
                        crumbindexpath = "{}/{}/index.md".format(config["inputfolder"] ,"/".join(tempfilepath[1:(index + 1)]))

                    print("Crumb path: {}".format(crumbindexpath))

                    with open(crumbindexpath, "r") as currentfile:
                        for line in currentfile:
                            if line.startswith("# "):
                                fancycrumb = line[2:]
                                print("Crumb name: {}".format(fancycrumb))
                                break

                    if filepath[-8:] == "index.md": #prevent category index documenting themselves
                        if index != len(tempfilepath) - 1:
                            breadcrumbs += "<a href=\"{crumbprefix}{link}\">{foldername}</a>".format(crumbprefix = config["crumbprefix"], link = "/".join(tempfilepath[1:(index + 1)]).lower(), foldername = fancycrumb)

                    else:
                        breadcrumbs += "<a href=\"{crumbprefix}{link}\">{foldername}</a>".format(crumbprefix = config["crumbprefix"], link = "/".join(tempfilepath[1:(index + 1)]).lower(), foldername = fancycrumb)

            print(pagetitle)
            print("filepath: " + filepath)
            # Write to a file
            print("Indexname: {}".format(filepath[-8:]))

            if filepath[-8:].lower() == "index.md":
                print("This is an index file...")
                outputfilename = "{outputfolder}/{filepath}{extension}".format(outputfolder = config["outputfolder"], filepath = filepath[len(args.input) + 1:-3],extension = ".html").lower()
            else:
                outputfilename = "{outputfolder}/{filepath}/index{extension}".format(outputfolder = config["outputfolder"], filepath = filepath[len(args.input) + 1:-3],extension = ".html").lower()


            print("Checking if {directory} exists...".format(directory = os.path.dirname(outputfilename)))

            if not os.path.exists(os.path.dirname(outputfilename)):
                try:
                    os.makedirs(os.path.dirname(outputfilename))
                    print("{directory} doesn't exist, creating...".format(directory = os.path.dirname(outputfilename)))

                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(outputfilename, "w+") as outputfile:

                # TODO: clean up this
                outputfile.write(htmlshell.format(
                    iconfilepath = config["crumbprefix"], 
                    htmlpagetitle = pagetitle, 
                    githubpath = config["crumbprefix"], 
                    pagebreadcrumbs = breadcrumbs, 
                    githublinktopage = "{}{}".format(config["linkprefix"], filepath), 
                    sidebar = contents, 
                    mainpage = pagecontent
                ))
                print("File written! {filename}".format(filename = outputfilename))