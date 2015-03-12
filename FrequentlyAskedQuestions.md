_disclaimer_: None of these questions have really been frequently asked. I'm just making it up. If you have a real question then please ask it; either directly to me (dr.scottgriffiths@gmail.com) or in the comment section below.


---


### How well optimised is the code? Are you planning to port to C? ###

The module is pure Python at the moment, and I've got no plans to move it to C quite yet.

If you've worried about speed then one thing to watch out for it to make sure you use the -O option when running Python so that it strips out the debug asserts from the module. I know it's obvious but people often seem to forget it and the -O option has a significant effect for the bitstring module.

To get a bit more speed you could probably compile it using Cython without too much trouble. I've found this gives a bit less than a 2x speedup (of course much more could be done by optimizing it properly in Cython). It's not officially supported but the rough instructions right now are:

1) Uncomment the Cython stuff in setup.py.

2) Rename bitstring.py to bitstring.pyx

3) Make sure you have Cython installed! (maybe that should be the first instruction)

4) Run 'python setup.py build\_ext --inplace'.

That works for me for version 3.1.2 and Python 2.7.

If you have a particular case that you think is unreasonably slow then please tell me about it and I'll see what I can do.


---


### Will Python 2.4 and 2.5 continue to be supported? ###

It's quite unlikely that any versions after 1.0 will support anything earlier than Python 2.6. The work needed to make a new release is considerable (and perhaps more importantly not a lot of fun) and as I estimate over 90% of people are using the newer Python versions I'm not convinced it is time well spent.

So if you need any features that were introduced after bitstring 1.0, or you want the many optimisations in later versions, then I'm afraid you'll have to get a newer version of Python.

The versions after 1.0 have been for Python 2.6 or later only. This has allowed a number of simplifications, including having just one code-base for Python 2.6 and 3.x.


---


### Are you going to introduce feature X? ###

That depends. If you have any feature requests then please take a look at the Issues tab, and if it's already there add a comment to say you want it, and if it's not then add a new issue. I am open to suggestions.


---


### Do you have a feature roadmap? ###

Not really, but you can get a good idea of the future direction by looking through the open enhancement requests on the Issues tab.


---
