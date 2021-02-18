# Preconditions module
This python module checks the necessary preconditions to be able to use the anomaly detection and prediction services 
with a given dataset
## Developer notes
**TODO**

## Testing notes
Two types of test for each module: unit and integration. This is still a work in progress
To execute the test:
Whithout parameters use all datasets by default
```sh
pytest 
```
With parameters
```sh
pytest --datasets=["all"|"internal"|"external"|"robotnik"|"emalcsa"]
```
## Deployment notes
This project can be install as a python library by executing:
```sh
sudo python setup.py install
```