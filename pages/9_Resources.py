import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file

page_setup()

st.markdown('''

# Resources 

For more detail on each of the methods, follow the links below.

The code behind our models can be found in the GitHub repositories for each demo.

''')

     
cols = st.columns(2)
with cols[0]:
    st.info(
        '''
**Thrombolysis decisions**

[Summary of the machine learning model and SHAP waterfall plots](https://samuel-book.github.io/samuel-2/samuel_shap_paper_1/introduction/intro.html).

[![][github-img]][predict-github]

[![][streamlit-img]][predict-streamlit] 


[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[predict-github]: https://github.com/samuel-book/streamlit_stroke_treatment_ml
[predict-streamlit]: https://samuel2-stroke-predict.streamlit.app/


''', icon='🔮')

with cols[1]:
    st.error(
        '''
**Pathway improvement**

[Online book on generating the results](https://samuel-book.github.io/samuel-1/pathway_sim/outline_scenarios.html), in particular [this analysis](https://samuel-book.github.io/samuel-1/pathway_sim/scenario_analysis.html).

[![][github-img]][pathway-github]

(no separate Streamlit page)

[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[pathway-github]: https://github.com/samuel-book/streamlit_pathway_improvement
[pathway-streamlit]: --
''', icon='⏱️')

with cols[0]:
    st.error(
        '''
**Population outcomes**

[Summary of the data sources and methodology](https://samuel-book.github.io/stroke_outcome/intro.html).

[![][github-img]][outcome-github]

[![][streamlit-img]][outcome-streamlit]


[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[outcome-github]: https://github.com/samuel-book/stroke_outcome_app
[outcome-streamlit]: https://samuel2-stroke-outcome.streamlit.app/
''', icon='📋')

with cols[1]:
    st.info(
        '''
**Lifetime mortality**

Academic paper in prep.: _"A lifetime economic stroke outcome model: A model for predicting mortality and lifetime secondary care use by patients who have been discharged from hospital following a stroke"_, Peter McMeekin, Stephen McCarthy, Andrew McCarthy, Jennifer Porteous, Michael Allen, Anna Laws, Phil White, Martin James, Gary Ford, Christopher Price.

A link will be added here when available.

[![][github-img]][economics-github]

[![][streamlit-img]][economics-streamlit]

[streamlit-img]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[github-img]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[economics-github]: https://github.com/stroke-optimist/streamlit_lifetime_stroke
[economics-streamlit]: https://lifetime-stroke-outcome.streamlit.app/
''', icon='💷')



st.markdown('''

## About the app  

The code behind this app is written in `python3` and the app itself is deployed using `streamlit`, which is a free service for hosting [python web apps](https://streamlit.io/). 

''')
            
# write_text_from_file('pages/text_for_pages/6_Resources.txt',
#                      head_lines_to_skip=2)
