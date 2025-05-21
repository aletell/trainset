# TRAINSET

TRAINSET is a graphical tool for labeling time series data. You can upload multiple series and apply one or many labels. In the GIF below, `series_a` is being labled with `bar` and `biz` labels while `series_b` is serving as a reference.

![TRAINSET labeling GIF](https://user-images.githubusercontent.com/8713574/112393077-b1832d80-8cb7-11eb-811b-0a7200be658d.gif)


## Hosted Version

If you just want to use TRAINSET and don't want to mess with deploying it, head to the [hosted version](https://trainset.geocene.com)

## Build Setup

``` bash
# install dependencies
uv install

# serve with hot reload at localhost:8050
uv run

# build for production with minification
uv build

# testing script for serving prod build locally
uv start

# build for production and view the bundle analyzer report
uv build --report

# pushing to heroku

git push heroku master
```
see [here](https://devcenter.heroku.com/articles/git#deploying-code).

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Funding Support

The development of TRAINSET was funded by the [NIH Clean Cooking Implementation Science Network](https://www.fic.nih.gov/About/Staff/Policy-Planning-Evaluation/Pages/clean-cooking-implementation-science-network.aspx) with funding from the [NIH Common Fund for Global Health](https://commonfund.nih.gov/globalhealth). The development team and cookstove community are grateful for this support.

## Python Version

The repository now includes a Python version of the graphical tool for labeling time series data. The main functionality is implemented in Python using Flask for the web interface.

## CSV File Format

The CSV file should have four comma-delimited columns with the header: `series, timestamp, value, label`. The `series` column should contain unique names for the time series. The `timestamp` column should contain timestamps in ISO8601 format. The `value` column should contain numeric scalar values. The `label` column should contain integer representations of booleans or other valid labels. The CSV data should be correctly formatted before processing it further.

## Hotkeys and Keyboard Shortcuts

The application supports the following hotkeys and keyboard shortcuts:

* Click a point to toggle it as labeled
* Click & Drag over a selection of points to label them
* SHIFT + Click & Drag over a selection of points to unlabel them
* → or ← : pan
* SHIFT + → or ← : fast pan
* ↑ or ↓: zoom
* Click & Drag the bottom context bar to adjust focus region
