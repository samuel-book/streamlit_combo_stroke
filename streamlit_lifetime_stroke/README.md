# Lifetime stroke outcome model


[![Open in Streamlit][streamlit-img]][streamlit-link] [![DOI][doi-img]][doi-link]

This repository contains the code behind the Streamlit app for the lifetime stroke model.

+ __Streamlit app:__ https://lifetime-stroke-outcome.streamlit.app/
+ __DOI:__ https://doi.org/10.5281/zenodo.8269389

The model is described in this paper:

_(the paper is not yet published. Link and proper citation will be added when available)_

> _"A lifetime economic model of mortality and secondary care use for patients discharged from hospital following acute stroke."_  
> Peter McMeekin, Stephen McCarthy, Andrew McCarthy, Jennifer Porteous, Michael Allen, Anna Laws, Phil White, Martin James, Gary A. Ford, Christopher I. Price  
> (details to be added once published)  
> (link to be added once published)  
> 2024

<a href="https://lifetime-stroke-outcome.streamlit.app/"><img align="right" src="https://raw.githubusercontent.com/stroke-optimist/stroke-lifetime/main/docs/streamlit_lifetime_preview_rotated_smaller.gif" alt="Animated preview of the Streamlit app."></a>

The app takes user inputs to select the age, sex, and Modified Rankin Scale (mRS) score on discharge from hospital following a stroke, and these are used to calculate the following quantities across the remainder of that patient's lifespan:
+ The probability of survival of the patient in each year.
+ The number of Quality-Adjusted Life Years (QALYs).
+ The expected use of resources (e.g. number of admissions to A&E and number of years spent in residential care) and the cost of those resources.
+ The discounted total net benefit by change in mRS score. 

The topics of the pages in the app follow the recommendations of ["Improving the usability of open health service delivery simulation models using Python and web apps"](https://openresearch.nihr.ac.uk/articles/3-48/v1).

## 📦 Use this code

[![GitHub Badge][github-img]][github-link] [![PyPI][pypi-img]][pypi-link]

The code behind all of the calculations in the app is available as a python package, `stroke-lifetime`. Instructions to install the package and a demo of the main calculations are available on GitHub:

+ https://github.com/stroke-optimist/stroke-lifetime
+ https://pypi.org/project/stroke-lifetime/




[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[streamlit-link]: https://lifetime-stroke-outcome.streamlit.app/

[doi-img]: https://zenodo.org/badge/575076706.svg
[doi-link]: https://doi.org/10.5281/zenodo.8269389

[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[github-link]: https://github.com/stroke-optimist/stroke-lifetime

[pypi-img]: https://img.shields.io/pypi/v/stroke-lifetime?label=pypi%20package
[pypi-link]: https://pypi.org/project/stroke-lifetime/