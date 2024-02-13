# Colorfy-API
Uses the [original Colorfy project](https://github.com/davidkrantz/Colorfy)'s algorithm to analyze the album artwork and compute the background color that would be set by Spotify (in about 80 % of cases) and then return this over a REST API.

The program uses k-means clustering to find distinct colors in the artwork and then computes a colorfulness index as defined by [Hasler and Süsstrunk (2003)](https://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf) for each of the colors.