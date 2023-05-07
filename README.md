### Code for Dligach and Miller, 2018 *SEM paper *Learning Patient Representations from Text*

To train a billing code prediction model:

* extract CUIs from MIMIC III patient data
* cd Codes
* ft.py cuis.cfg.

To run the experiments with i2b2 data:

* cd Comorbidity
* svm.py sparse.cfg
* svm.py dense.cfg

For the experiments described in the paper, we used NumPy 1.13.0, scikit-learn 0.19.1, and Keras 2.0.4 with Theano 0.9.0 backend. Titan X GPU we used for training neural network models was provided by NVIDIA.


conda remove -n py2 --all



To setup environment
1. Install Anaconda
2. Install Python 2.7 (In terminal run these commands)
    conda create --name py2 python=2.7
    conda activate py2
3. I installed python, keras, scikit the latest package so had to downgrade to match what author used.
    python -m pip install numpy==1.13.0
    python -m pip install scikit-learn==0.19.1
    python -m pip install keras==2.0.4
    python -m pip install theano==0.9.0
    python -m pip install tensorflow==1.0.0
    pip install pandas
    PyCharm install nltk
    PyCharm install word2vec
    python -m pip install numpy==1.13.0 (some complains but code works)
    pip install h5py
4. Modify the line 'os.environ['DATA_ROOT'] = ...' in the main of every class to point it to the data folder locally on your machine.
5. 