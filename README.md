whiskeybot
==========

A simple IRC bot to interface with OLCC's liquor sales API

# Whiskeybot requirements list

## Primary features
- return the (geographically) closest available source to buy the requested liquor, with price.
- return the lowest price for the requested liquor within the region. (by zip code, distance, or however else we can manage it).
- return the operating hours of a requested liquor store (and if it's currently open).

## Possible additional features
- Return a random mixed drink recipe that uses a specified ingredient, if we can figure out how to query a recipe database.
- Return a random mixed drink recipe.
- Return a random drinking song.
- Return a random drinking game.
- Return the most-requested liquor name by a specified irc user.

## Dependencies ##

* [python2](http://www.python.org/)
* [PyOLP](https://github.com/cameronbwhite/PyOLP)
* [kitnirc](https://github.com/ayust/kitnirc)
