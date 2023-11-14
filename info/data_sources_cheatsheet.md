# Data sources for the Streamlit apps

This notebook shows which data gets used where across the Streamlit apps.

1. 📊 Descriptive statistics
2. ⏱️ Pathway improvement
3. 🔮 Thrombolysis decisions
4. 📋 Population outcomes
5. 💷 Lifetime outcomes
6. 🔎 Details: 🔮 Thrombolysis decisions
## 📊 Descriptive statistics


## Data

+ __SSNAP Subset 📊 DS1__ - ~280,000 patients

| | |
| --- | --- |
| ✨ Cleaned | 🏥 Grouped by stroke team |
| 🚑 Ambulance arrivals | 📅 Grouped by calendar year |
| 👥 Teams with over 250 admissions |  |
| 💉 Teams with at least 10 thrombolysis |  |


+ __SSNAP Subset 📊 DS2__ - ~120,000 patients

| | |
| --- | --- |
| ✨ Cleaned | 🏥 Grouped by stroke team |
| 🚑 Ambulance arrivals | 📅 Grouped by calendar year |
| 👥 Teams with over 250 admissions | ⏰ Onset time known |
| 💉 Teams with at least 10 thrombolysis | ⏳🏥 Onset to arrival at hospital no more than 4 hours |

The calculations are repeated with exactly the same method for two data sets. Both are subsets of the original SSNAP data. The data set 📊 DS2 first does the same filtering as 📊 DS1, and then also restricts the subset to patients with known onset time and whose onset to arrival time is no more than 4 hours.

Groups considered:
+ Each of the 119 stroke teams in SSNAP Subset 📊 DS1 or 📊 DS2 separately
+ Combined data for all stroke teams in each region of England and Wales
+ Combined data for all 119 stroke teams

The regions are defined by matching each hospital's postcode to its longitude and latitude, then finding which LSOA it falls in and finally matching the ONS data for LSOA11NM (LSOA 2011 name) with the ONS data for RGN11NM (region 2011 name).

Year categories considered:
+ Each calendar year from 2016 to 2021 inclusive.
+ Data from all years combined into "2016 to 2021" category.


### Method

For each group and each year category:
+ Take that subset of patients.
+ Calculate total admissions, the number of entries in the subset.
+ Calculate average pathway times. Take the _median_ of:
    + onset-to-arrival time
    + arrival-to-scan time
    + scan-to-thrombolysis time 
+ Calculate average patient scores. Take the _mean_ of:
    + age
    + stroke severity
    + prior disability
    + discharge disability
    + increased disability due to stroke
+ Calculate proportions of patients that fall into the following categories:
    + male
    + infarction
    + onset known
    + onset-to-arrival time below 4 hours
    + precise onset known
    + onset during sleep
    + afib anticoagulants
    + pre-stroke disability 0-2
    + thrombolysis
    + death
    + mRS 5-6
    + mRS 0-2
 
### Outputs

+ 📊 Descriptive statistics for each group and each year category.
## 🔮 Thrombolysis decisions

### Data

+ __SSNAP Subset 🔮 Training data__ - ~110,000 patients

| | |
| --- | --- |
| ✨ Cleaned | ⏰ Onset time known |
| 🚑 Ambulance arrivals | ⏳🩻 Onset to scan under 4 hours |
| 👥 Teams with over 250 admissions | 🪚 Only 10 features |
| 💉 Teams with at least 10 thrombolysis |  |


+ __SSNAP Subset 🔮 Testing data__ - 10,000 patients

| | |
| --- | --- |
| ✨ Cleaned | ⏰ Onset time known |
| 🚑 Ambulance arrivals | ⏳🩻 Onset to scan under 4 hours |
| 👥 Teams with over 250 admissions | 🪚 Only 10 features |
| 💉 Teams with at least 10 thrombolysis |  |

### Method

1. The 🔮 Training data is used to create the 🔮 ML model.
1. The 🔮 ML model is used to create the ⚖️ SHAP model (log-odds).
2. The 🔮 ML model and the 🔮 Testing data are used to create the ⚖️ SHAP model (probability).

### Outputs

| Output | Uses |
| --- | --- |
| 🔮 ML model | App page _🔮 Thrombolysis decisions_, creation of 🎯 Benchmark scenario. |
| ⚖️ SHAP model (log-odds) | Creation of 🎯 Benchmark rankings. |
| ⚖️ SHAP model (probability) | App page _🔎 Details: 🔮 Thrombolysis decisions_ |
## 🎯 Benchmark rankings

The list of benchmark teams is used to highlight the higher-performing teams in the _🔮 Thrombolysis decisions_ and _⏱️ Pathway improvement_ apps. It is also used to select the teams that will be used to calculate the benchmark scenario parameters for the 📈 Hospital performance data.

### Data

+ __⚖️ SHAP model (log-odds)__

+ __SSNAP Subset 🔮 Testing data__ - 10,000 patients

| | |
| --- | --- |
| ✨ Cleaned | ⏰ Onset time known |
| 🚑 Ambulance arrivals | ⏳🩻 Onset to scan under 4 hours |
| 👥 Teams with over 250 admissions | 🪚 Only 10 features |
| 💉 Teams with at least 10 thrombolysis |  |

### Method

1. Group the 🔮 Testing data patients by stroke team.
2. For each stroke team:
    1. For each 🔮 Testing data patient, use the ⚖️ SHAP model to calculate one SHAP value per feature.
    2. Take the SHAP values for the "attended this stroke team" feature. Discard the other 127 SHAP values.
    3. Calculate the mean SHAP value for "attended this stroke team".
3. Take all mean SHAP values for all teams. Sort them in order of largest positive effect to largest negative effect.
4. Add a "rank" to this ordered list so the first team is rank 1 and the final is rank 120.
5. Select the top 25 teams from the list. These are the benchmark teams.

### Outputs

+ List of 🎯 Benchmark ranking for each team.
## 📈 Hospital performance

We want to see the effect on the thrombolysis rate when we change certain parts of the patient pathway. This notebook sets up the numbers needed to perform those calculations.

The scenario before we change anything is called "base". The hospital performance for this scenario was found in the previous notebook.

The three other scenario types we will consider are:

+ onset
+ speed
+ benchmark

In addition, any of the three scenario types can be considered simultaneously. The complete list of scenario combinations is as follows:

+ base
+ onset
+ speed
+ benchmark
+ onset + speed
+ onset + benchmark
+ speed + benchmark
+ onset + speed + benchmark

To set up the scenarios, we take the base hospital performance data and overwrite certain values to achieve some target results.

+ In the onset scenario, the proportion of patients with a known onset time is the greater of the current proportion and the national upper quartile.
+ In the speed scenario, 95% of patients have a scan within 4 hours of arrival, and all patients have 15 minutes arrival-to-scan time and 15 minutes scan-to-needle time.
+ In the benchmark scenario, the proportion of patients thrombolysed matches the benchmark rate found in the previous notebook. This rate is different for each hospital.

### Data

### Method

This notebook calculates the pathway statistics for each stroke team. The patients that attended each stroke team are first split into groups for each stroke type. Then a series of tests are performed. The proportion of patients passing each test is recorded, and for certain subgroups of patients passing particular tests, the distribution of times taken at that point in the hospital pathway are measured.

The tests are:
1. Is onset time known?
2. Is onset to arrival within the time limit?
3. Is arrival to scan wtihin the time limit?
4. Is onset to scan within the time limit?
5. Is there enough time left for thrombolysis?
6. Did the patient receive thrombolysis?

And the time distributions measured are:
1. Onset to arrival time for those passing Test 2.
2. Arrival to scan time for those passing Test 3.
3. Scan to treatment time for those passing Test 6.

sigma, mu

also record mean number of admissions per calendar year, proportion receiving IVT, prop receibing MT, prop of MT who also receive IVT.



### Outputs
## 📈 Hospital performance: ⏰ "onset" scenario parameters

### Data

+ __SSNAP Subset 📈 HP1__ - ~119,000 patients

| | |
| --- | --- |
| ✨ Cleaned | 📅 Calendar years 2019 and 2020 |
| 🚑 Ambulance arrivals | 🏥 Grouped by stroke team |
| 👥 Teams with over 250 admissions | 🧠 Grouped by stroke type |
| 💉 Teams with at least 10 thrombolysis |  |

### Method

1. For each stroke team:
    1. Take the subset of patients in this team. Keep all stroke types in this same group. 
    2. For the subset, find the proportion of patients who have a known onset time.
    3. Store the proportion in a list.
3. Find the quartiles of the list of proportions.
4. Use the upper quartile as a target "onset known" proportion for the onset scenario.

### Outputs

+ One number. This is the target "onset known" proportion for the onset scenario.
## 📈 Hospital performance: 🎯 "benchmark" scenario parameters

### Data

+ __SSNAP Subset 📈 HP2__ - ??? patients

| | |
| --- | --- |
| ✨ Cleaned | 📅 Calendar years 2019 and 2020 |
| 🚑 Ambulance arrivals | ⏰ Onset time known |
| 👥 Teams with over 250 admissions | ⏳💉 Patients on time for thrombolysis |
| 💉 Teams with at least 10 thrombolysis | 🪚 Only 10 features |
| | 🏥 Grouped by stroke team |
| | 🧠 Grouped by stroke type |

+ _🧠 Grouped by stroke type_:
Label whether each patient has an LVO, nLVO, or "other" stroke type. All non-infarction patients are designated "other". All patients with infarctions and a stroke severity of at least 11 are designated LVO, and everyone else is nLVO.

The number of patients in the dataset is calculated as the method goes along so currently I haven't recorded it.

### Method


We want to take all of the patients who pass the first five masks (onset known and ... and enough time to treat) and see whether the benchmark stroke teams would have chosen to thrombolyse them.

sigma, mu

also record mean number of admissions per calendar year, proportion receiving IVT, prop receibing MT, prop of MT who also receive IVT.

We want to compare the decisions made by each stroke team with the decisions that we expect the benchmark teams to make.

To do this, we use the prediction model to send all of one hospital's patients to all of the benchmark hospitals instead, changing no patient details except the stroke team ID. We take the 25 separate thrombolysis decisions from the 25 benchmark hospitals. If at least half of the benchmark hospitals would have thrombolysed the patient, the majority benchmark decision is to thrombolyse. Otherwise, the decision is to not thrombolyse. The benchmark thrombolysis rate is the percentage of patients for whom the majority benchmark decision is to thrombolyse.

### Outputs
## 📈 Hospital performance: "base" scenario

### Data

+ __SSNAP Subset 📈 HP1__ - ~119,000 patients

| | |
| --- | --- |
| ✨ Cleaned | 📅 Calendar years 2019 and 2020 |
| 🚑 Ambulance arrivals | 🏥 Grouped by stroke team |
| 👥 Teams with over 250 admissions | 🧠 Grouped by stroke type |
| 💉 Teams with at least 10 thrombolysis |  |


### Method


### Outputs
## ⏱️ Pathway improvement

📈 Hospital performance
| | |
| --- | --- |
| ? | ? | 
