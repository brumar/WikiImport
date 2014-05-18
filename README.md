# Anki plug-in to import wikipedia content
## Note for regular users
You are at the wrong place, to make use of this plug-in go it's dedicated page on [anki addons] (https://ankiweb.net/shared/addons/)
## Notes for developpers
This plug-in makes use of import.io, a tool to extract informations from websites without pain.
### Why ?
It was a lazy move, and not very wikipedia friendly as import.io circumvent the regular way to get datas from wikipedia.
This plug-in won't be used with huge requests to wikipedia as it only read the pages within a single category, thus it's not really evil,but it could be better.
More informations [there] (http://www.mediawiki.org/wiki/Category:MediaWiki_API_Overview) for anyone who has the courage to fork it for the good of wikipedia.
### What are the import.io requests
These two import.io extractors are programmatically used  :
- Get the pages within a category : [link to import.io] (https://import.io/data/mine/?id=68b4b6ac-25ce-434d-923d-7cc9661216ff)
- Get the first first paragraphe and the title of a wikipedia page : [link to import.io] (https://import.io/data/mine/?id=7fc7daa2-25a4-4649-b48c-be1d7fd8756e)
## How to make it work from these sources
- Download all the python files
- Open Anki addons directory
- create a python file named with this line : from
- Create a directory named
- Move all the python files in there
- Create an account on import.io
- Create an API key from [this page] (https://import.io/data/account/)
- With these two informations complete the two lines in useroptions.py
- Open a profile in anki2 and try the plug-in with tools > wipedia import

## Known Issues
- Sometimes the first paragraphe is broken in wikipedia in order to print a mathematical formula or a list.
It's a rare event, but it can produce incomplete anki cards.