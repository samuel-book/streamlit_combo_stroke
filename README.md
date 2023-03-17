# Stroke combined app

Combined the existing stroke streamlit apps into one multipage app.

| **Combined** |     **Outcome**                  | **Economics**               | **Predict**                     |**Pathway**                      |
|:--------------------------------|:--------------------------------|:--------------------------------|:--------------------------------|:------------------------------|
| [![][github-img]][combo-github] | [![][github-img]][outcome-github] | [![][github-img]][economics-github] | [![][github-img]][predict-github] | [![][github-img]][pathway-github] |
| [![][streamlit-img]][combo-streamlit] | [![][streamlit-img]][outcome-streamlit] | [![][streamlit-img]][economics-streamlit] | [![][streamlit-img]][predict-streamlit] | -- |
| [![][combo-qr]][combo-streamlit] |  [![][outcome-qr]][outcome-streamlit] | [![][economics-qr]][economics-streamlit] | [![][predict-qr]][predict-streamlit] | -- |

[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg

[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white


[combo-github]: https://github.com/samuel-book/streamlit_combo_stroke
[combo-streamlit]: https://stroke-predictions.streamlit.app/
[combo-qr]: ./info/qrcode_streamlit_combo.png

[pathway-github]: https://github.com/samuel-book/streamlit_pathway_improvement
[pathway-streamlit]: --
[pathway-qr]: --

[outcome-github]: https://github.com/samuel-book/stroke_outcome_app
[outcome-streamlit]: https://samuel2-stroke-outcome.streamlit.app/
[outcome-qr]: ./info/qrcode_streamlit_outcomes.png

[economics-github]: https://github.com/stroke-optimist/streamlit_lifetime_stroke
[economics-streamlit]: https://lifetime-stroke-outcome.streamlit.app/
[economics-qr]: ./info/qrcode_streamlit_lifetime.png

[predict-github]: https://github.com/samuel-book/streamlit_stroke_treatment_ml
[predict-streamlit]: https://samuel2-stroke-predict.streamlit.app/
[predict-qr]: ./info/qrcode_streamlit_predictions.png


### Run this app locally

To download this whole app and run it on your local machine,
use either of the following two options.

__🐍 Python users__

[![][github-img]][combo-github]

+ Clone the GitHub repository 
+ Check your packages match those in `requirements.txt` (I recommend using a conda environment for this).
+ Run the app with `streamlit run Introduction.py`

If you're only interested in one of the demo pages, you can follow
these same instructions with one of the other GitHub repositories
linked to above.

[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[combo-github]: https://github.com/samuel-book/streamlit_combo_stroke


__🐳 Docker users__

[![][docker-img]][combo-dockerhub]

[docker-img]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[combo-dockerhub]: https://hub.docker.com/r/aselaws/streamlit_combo_stroke

+ Download the Docker image: `docker pull aselaws/streamlit_combo_stroke`
+ Run the image: `docker run -p 8501:8501 aselaws/streamlit_combo_stroke`

This should display a Local URL that can be copy and pasted into your favourite browser to see the app.
''')
