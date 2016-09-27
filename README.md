# biogridpy

biogridpy is a Python client for the [BioGRID](http://wiki.thebiogrid.org/doku.php/biogridrest) webservice.

## Installation

To install, clone the repository
```bash
$ git clone https://github.com/arvkevi/biogridpy.git
$ cd biogridpy
$ python setup.py
```

## Usage 


**Before using the client, get a *free* access key [here](http://webservice.thebiogrid.org/) or if you alread have one, see below:**

Copy and Paste the access key to the **biogridpyrc** file:

```bash
$ vi biogridpyrc
```

```bash
[BioGRID_ak]
access_key = YourAccessKeyHere
```
---
Instantiate the BioGRID client:
```python
>>> from biogridpy.biogrid_client import BioGRID
>>> BG = BioGRID()
```

The **interactions** endpoint is the most commonly utilized.  The first and only positional argument is a string that describes the type of result format.  Valid keyword arguments are the same parameters from the [parameter list](http://wiki.thebiogrid.org/doku.php/biogridrest#list_of_parameters).  Any parameter that accepts a list of ```|``` separated identifiers can be a Python list type object or a file with one identifier per line.

```python
>>> results = BG.interactions('tab2', geneList=['RB1', 'E2F1'],
                                      evidenceList='examples/evidenceList.list',
                                      includeEvidence='true',
                                      taxId=9606)
```

There are several attributes to describe and work with the result object:
```python
>>> results.count
	11
>>> results.output_format
	'tab2'
>>> results.endpoint
	'interactions'
>>> results.result #formatted result for downstream use
>>> results.raw_result #unformatted result
```

Available methods are meant to facilitate downstream analyses or for pipeline development.
The export method will save the result object as a file in the proper format according to the format specified previously.  The toDataFrame method simply formats the data for easy transformation to a [pandas](http://pandas.pydata.org/) DataFrame object.

```python
>>> results.export(outdir='../examples/example_results', 
                  filename='E2F1_RB1_9606')
>>> import pandas as pd
>>> #you could use the following to transform the results regardless of type
	try: #tab2, extendedTab2, tab1
    	df = pd.read_csv(bg_results.toDataFrame(), sep='\t')
	except IOError as e: #json, jsonExtended
    	df = pd.read_json(bg_results.toDataFrame(), orient='index')
```

---
The following **non-interaction** endpoints are also available:
1. evidence
2. identifiers
3. organisms
4. version

Use the **result** attribute to view the response.
```python
>>> evid = BG.evidence()
>>> evid.result[:5] #first 5 elements
	['AFFINITY CAPTURE-LUMINESCENCE',
 	'AFFINITY CAPTURE-MS',
 	'AFFINITY CAPTURE-RNA',
 	'AFFINITY CAPTURE-WESTERN',
 	'BIOCHEMICAL ACTIVITY']
```

### walkthrough

The IPython notebook **walkthrough.ipynb** provides in-depth examples of how to use each method.

```bash
$ cd biogridpy
$ jupyter notebook notebooks/walkthrough.ipynb
```
or
```bash
$ cd biogridpy
$ ipython notebook notebooks/walkthrough.ipynb
```

## Citation
Winter AG, Wildenhain J, Tyers M. BioGRID REST Service, BiogridPlugin2 and BioGRID WebGraph: new tools for access to interaction data at BioGRID. Bioinformatics, 2011 Apr 1.

[serval other BioGRID publications](http://wiki.thebiogrid.org/doku.php/aboutus)
