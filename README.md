# Analysing *Vellum* and *Ink*

This is a bit of tomfoolery, about which you can read more 
[if the fancy takes you](https://tikitu.github.io/vellum_and_ink).

The outcome of this project will be annotated editions of *Vellum* and *Ink*.
But there's a problem: we don't have rights to reproduce those texts! Never 
fear, we have a clever (?) workaround.

If *you* own an electronic copy of *Vellum* (and eventually *Ink*, I hope), 
you can add our annotations (if everything works as it should) by running it
through a little Python program. You'll need to spend some time on the 
commandline; I *hope* the instructions are comprehensive, but so far I've only
tested them on one (1) machine with one (1) edition of *Vellum* so Your 
Mileage May Vary.

For completeness sake: these instructions have been verified to work

* on a Macbook pro with Python 2.7, working with the Amazon ebook edition
    of *Vellum*, listed as published by Tor, &ldquo;Unabridged edition 
    (August 11, 2011)&rdquo;.
* ... nowhere else, actually.

Here goes:

1. You need to extract the raw html from the ebook edition you've got. A good
    option is [Calibre](http://calibre-ebook.com/). If your edition is
    DRM-locked, [some Calibre extensions can help](https://apprenticealf.wordpress.com/2012/09/10/calibre-plugins-the-simplest-option-for-removing-most-ebook-drm/).
    Note that it is *entirely your responsibility* to ensure that this is 
    legal in your jurisdiction.
2. Get the html into one file. Any way you like. A Calibre export to 
    &ldquo;htmlz&rdquo; format worked quite nicely for me: this is a zip
    archive, and the file you want inside it is `index.html`.
3. Now check out this very repository (the instructions are for a 
    linux/unix/mac commandline, I have no idea how this would look for 
    Windows):
    
        $ git clone https://github.com/tikitu/vellum_and_ink.git
    
4. Go into the directory this gives you and install the Python tools. (If you
   don't have `virtualenv` yet, start by installing that: 
   `pip install virtualenv`. If you don't have `pip`, 
   [get that first](https://pip.pypa.io/en/latest/installing.html). I know, 
   I'm sorry, Python packaging is a mess.) Right, where were we?

        $ cd vellum_and_ink
        $ virtualenv .
        $ bin/python setup.py install
    
5. Now you've got a tool that (if all goes well) will reformat your ebook to
    add in our annotations:
    
        $ bin/vellum <ebook-html-file> <output-filename>
    
If you see any commandline output, it means this process has gone wrong 
somewhere. [Email me](mailto:tikitu+vellum@logophile.org) the details and I'll
see if I can help.
    
For the styling of the resulting file to work properly it needs to stay in the 
same directory as your git clone (i.e. `vellum_and_ink`). (It will look for 
some css files in a directory called `resources`; if it doesn't find them, no
styling.) If it's already there, opening the output file in your web browser
*should* (fingers crossed) show you *Vellum* 
[in funny pastel colours](https://tikitu.github.io/vellum_and_ink/fonts.html).
    