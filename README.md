### Original paper: *Learning Patient Representations from Text* by Dimitriy Dligach and Timothy Miller

This code builds on authors original code available here https://github.com/dmitriydligach/starsem2018-patient-representations

### Environment setup:
1. Install Anaconda or any virtual environment management software and create a new environment.
2. Install Python 2.7
    * `conda create --name py2 python=2.7`
    * `conda activate py2`
3. Use following package dependencies.
    * `python -m pip install numpy==1.13.0`
    * `python -m pip install scikit-learn==0.19.1`
    * `python -m pip install keras==2.0.4`
    * `python -m pip install theano==0.9.0`
    * `python -m pip install tensorflow==1.0.0`
    * `python -m pip install pandas==0.24.2`
    * `python -m pip install h5py==2.10.0`
    * `python -m pip install nltk==3.4.5`
    * `python -m pip install gensim==3.8.0`
    * `python -m pip install psycopg2==2.9.3`

### Data Preprocessing:
1. Register for an account for PhysioNet by completing training for handling healthcare patient data. 
2. MIMIC III data is available here: https://physionet.org/content/eicu-crd/2.0/
3. Install postgress db and use the queries available here (https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii/buildmimic/postgres) 
   to load the csv data in the db. 
4. `Noteevents`, `procedures_icd`, `diagnoses_icd`, `cptevents` are the more important tables. We used following queries to extract data
`select subject_id, icd9_code from procedures_icd order by subject_id;`
`select subject_id, icd9_code from diagnoses_icd order by subject_id;`
`select subject_id, cpt_number from cptevents order by subject_id;`
`select subject_id, string_agg(text, ' ') from noteevents group by subject_id having subject_id = 000;`
5. Each patient notes were saved to separate files using `ExtractNotesPerPatient.py`
6. These files events were then used into cTakes CPE software for CUI extractions.
7. Resulting files from cTakes were then processed using `ParseForCUI.py` and saved to `data/MimicIII/Patients/Cuis` folder.
8. Then run `GetUniqueListOfCuis.py` to get a unique list of CUIs for every patient and save it to `data/MimicIII/Patients/mimic-cuis.txt`

### Runing the code:
1. Data that we extracted is already loaded in this repo under the "data" folder. All paths to run the scripts are 
   relative to that folder. 
2. If choosing to store data elsewhere, modify the line `os.environ['DATA_ROOT'] = ...` in the main function of the 
   running class to point to the data folder location.

### Commandline parameters to run
#### Training
`Codes/ft.py cuis.cfg`
#### Evalution
`Comorbidity/svm.py sparse.cfg`
`Comorbidity/svm.py dense.cfg`

### Results
|                      | P       | R      | F1      | Train_Example | Test_Example |
|:---------------------|:-------:|:------:|:-------:|:----------:|:--------:|
| Asthma               |   0.543 |   0.516 |   0.510 |      453   |     318  |
| CAD                  |   0.587 |   0.565 |   0.549 |      440   |     308  |
| CHF                  |   0.415 |   0.339 |   0.221 |      219   |     294  |
| Depression           |   0.505 |   0.502 |   0.478 |      460   |     319  |
| Diabetes             |   0.414 |   0.461 |   0.417 |      448   |     322  |
| GERD                 |   0.332 |   0.335 |   0.313 |      387   |     281  |
| Gallstones           |   0.507 |   0.501 |   0.473 |      468   |     329  |
| Gout                 |   0.443 |   0.497 |   0.468 |      472   |     333  |
| Hypercholesterolemia |   0.479 |   0.479 |   0.478 |      392   |     289  |
| Hypertension         |   0.507 |   0.503 |   0.487 |      431   |     302  |
| Hypertriglyceridemia |   0.475 |   0.500 |   0.487 |      462   |     325  |
| OA                   |   0.373 |   0.343 |   0.325 |      440   |     308  |
| OSA                  |   0.437 |   0.500 |   0.466 |      474   |     334  |
| Obesity              |   0.473 |   0.476 |   0.470 |      446   |     306  |
| PVD                  |   0.493 |   0.499 |   0.477 |      443   |     311  |
| Venous Insufficiency |   0.465 |   0.496 |   0.480 |      419   |     284  |
| Average              |   0.465 |   0.469 |   0.444 |            |          |

