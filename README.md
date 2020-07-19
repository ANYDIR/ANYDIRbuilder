# ⇌ANYDIR Builder

ANYDIR builder, or simply just ANYDIR, is a tool to generate sites in a similar fashion to documentation generators or the Osu wiki. It takes in a bunch of markdown files and throws them out as nicely formatted HTML files ready to be uploaded as a static website.

## Running ANYDIR

ANYDIR's build script requires the following:
- Python3
    - The following libraries
        - ``pip install python-slugify``
        - ``pip install markdown2``

ANYDIR by default looks in a subdirectory called ``Index`` for MD files, MD files can be called anything but to preserve compatibility it's recommended to call md files ``index.md``.

Run ANYDIR in your terminal of choice with Python and you should eventually get a directory outputted at ``output/`` which is ready to be uploaded as a static site.

## ANYDIR format

ANYDIR does a multitude of things to provide a smooth generation experience, these are the following:

- Turn H2 to H6 headers into content subheadings in the sidebar.
- Use the first H1 header as the page title.
- Turn subdirectories into clickable breadcrumbs at the top of the page.
    - It is recommended for cleanliness sake to have an ``index.html`` in every directory, generally with links to the subdirectories of that page.

## Configuring ANYDIR

ANYDIR has somewhat limited customisability. These can be found at the top of the python file.

- Title prefix - Page title prefix that is used for tabs.
- Link prefix - Prefix for edit links, should point to where MD files are hosted.
- Crumb prefix - Prefix for crumb links, should point to the root of the site.
- Contents format - Format for contents entries. Has several format inputs explained in the code.
- Bread crumb - HTML for the breadcrumb icon.
- Input folder - Folder from which the root crumb is named and from which MD files are pulled.
- Output folder - Where files are outputted to.

## Notes

⇌ANYDIR builder **is extremely quick and dirty**. It was made to serve a purpose of which it does. Current issues include ``./`` breaking the input path.

## Current ANYDIR projects

- Better ``format`` calls
    - The ``format`` calls require IDs that are descriptive. STATUS: IMPORTANT