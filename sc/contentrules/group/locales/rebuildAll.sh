#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot sc.contentrules.group.pot --create sc.contentrules.group --merge manual.pot ..

# finally, update the po files
i18ndude sync --pot sc.contentrules.group.pot  `find . -iregex '.*sc.contentrules.group\.po$'|grep -v plone`

