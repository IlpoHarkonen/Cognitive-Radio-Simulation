# Cognitive-Radio-Simulation

## How to run

Get [Python3](https://www.python.org/downloads/)

Create and activate virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

If you are on Windows

```
venv\Scripts\activate
```

Install needed packages

```
pip install -r requirements.txt
```

See help 

```
python main.py -h
```

And run the simulation with default values set in settings.py. You can 
use the command line parameters to change conditions.

```
python main.py
```


## Soft To Do
* PEP8 everything [Guide](https://www.python.org/dev/peps/pep-0008/])
* More informative plots, e.g. bts switch cost against gained throughput
