# Report
## Project 1 - COMP 479
#### Bryce Hamilton 40050171
#### Due: October 8, 2021

### Files

#### `output` directory
Output files for each of the 5 steps of pipeline for the first 5 documents present in the first reuters file, generated by running `python run_pipeline.py`

#### `reuters21578` directory
Input Reuters files  
Reuter’s Corpus Reuters-21578  
Source: http://www.daviddlewis.com/resources/testcollections/reuters21578/

#### `helpers` directory
Contains helpers for writing to file, either a string or list

#### `demo` directory
Contains demo file notebook as well as pdf demonstracting each of the steps of the pipeline and tests

#### `pipeline.py`
Core module containing the 5 core steps of the pipeline, along with extra steps and a `run()` function to run the pipeline

#### `run_pipeline.py`
As discussed above, used to run the pipeline and generate output files  
Run pipeline with default arguments: `python run_pipeline.py`  
Run pipeline with file limit (3) and doc limit (4): `python run_pipeline.py 3 4`  
This will write output files for the first 4 documents in the first 3 reuters files

#### `asserts.py`
File to test each step in the pipeline

#### `report.pdf`
File containing report of project