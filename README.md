Relevance Graph
=============
Put related nodes together by given gravitation between related nodes.


Dependencies
-----------

* python 3.4
* numpy
* scipy
* scikit-learn
* matplotlib
* kivy (for GUI, support Windows, Mac OS, Linux)

Run Demo
--------

6 node demo:

    $ kivy examples/demo_6_nodes.py

beers:

    $ kivy examples/beers.py

beers' clustering by K means:

    $ python examples/beers_with_kmeans.py

Screen Shots
------------

beers:

![graph of beers](https://raw.githubusercontent.com/Xorcerer/relevance-graph/master/screenshots/screenshot-1-beers.png)


Plan
----

* Clustering by Persistance Homology.
* Replace kivy entirely by matplotlib, including the animation part.
