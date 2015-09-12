album: a simple web app for browsing experiments
================================================

Rough Plan
----------

This is a read-only view of experiments and their data.

* `/runs` -> list of recent runs
* `/run/<uid>` -> detailed view of the metadata and data from an experiment

I image that one basic run view will branch into a rich catalog of view's customized to different kinds of experiment. The server can inspect the contents of a run to decide how to represent it in HTML.

Implementation
--------------

For now, Flask, but we can use django if we outgrow Flask. Also, let's use Bootstrap to keep the style bikeshedding to a minimum (and get good mobile support for free!)
