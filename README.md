# HashCodeCI
Continuous submission upload and result checking in the Google Hashcode coding competition.


## Dependencies
- python 3
- python libraries: requests, polling, configparser

This can easily be installed with pipenv: ```pipenv install```

(How to install pipenv: ```pip install pipenv``` or ```pip3 install pipenv```)


## How to use

### Configurations
in settings.cfg, update the following info:

##### Authentication
A token that is valid for 1 hour can be extracted when analysing the contents of a packet in google chrome, when submittig a solution via the hashcode-judge page or when loading the page.

The token can be found in the **authorization** field of the **request header** of calls to *https://hashcode-judge.appspot.com/api/judge/v1/*

(TODO: use *oauthclient* library for acquiring token )

##### Round-specific
Edit the ```round_id``` field in accordance to the round ID in the url bar.
(Test round = https://hashcodejudge.withgoogle.com/#/rounds/5736842779426816)

The datasets also will have to be acquired by analyzing the packets once in the Google Chrome inspector.

##### Project specific:
- Give the files that are solutions for each dataset. (generation of these might be included in a more advanced CI flow)
- And the source directory. (this will get zipped and attached to the submission)

#### Example settings.cfg file
```
[authentication]
token = ya29.Gl1sBbXF0URfCmVleRfTXrgsfzTtfStNyO139L8KFUdia7bvuHcQaxdhJX7XqVoAKf33jM9T0mhKrbA0RyAgj7Gg8BPxTLTBxbtbL-ChGBtDFkeGkbpLGejwn_ngLxQ
round_id = 5736842779426816

[project]
source_dir = ./source
solutions0 = README.md
solutions1 = README.md
solutions2 = README.md
solutions3 = README.md

[datasets]
dataset0 = 5167684987650048
dataset1 = 5739156827275264
dataset2 = 5726181865291776
dataset3 = 5690701543112704
```
### Usage
```python sync.py [datasetID] [--solution=solutionfile_path]```


Example: ```python submit.py 1 --solution=README.md```
This submits the README.md file as solution for dataset 1.

### Future improvements
Possible improvements:
- use oauth for acquiring the token, instead of manually retrieving it
- integrate some git workflow for succesfull (label/ commit-message & push?)
- integrate the generation of solution-files in the workflow (python or bash?)
