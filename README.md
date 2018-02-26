# PyBump

A simple semantic versioning script.

This will update the version in your ./resources/version.txt file according to
semantic versioning.

### Prerequisites

 - python 3.6.4 or later

### Running

 - `python pybump.py` into your terminal. Make it an alias, if you wish...
 - Arguments:
	- version (use this if you just wish to print the current version)
	- major (to bump the x in x.4.5)
	- minor (to bump the x in 6.x.5)
	- patch (to bump the x in 6.4.x)

### Note:

This is just a snippet taken from a previous project (and thus is quite
specific). Future dev might include updating a changelog file instead of a
version file, and committing said version changes to git. Maybe even cleaner
xml handling.
