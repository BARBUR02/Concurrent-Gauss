# Concurrent Gauss
## Jakub Barber

### Description
Project creates graphs of Dependencies D, graph of Independencies I and computes Foata Normal Form for Gauss elimination problem driven by data from input file.
After all the computations, algorithm prepares and renders Dekiert Graph for a problem specified matrix.
First phase includes calculations of Dekiert Grpah and graphs I,D as well as Foata groups. It ends with a summary of results of format:
```
RESULTS:
        D = [list of Edges in D graph]
        I = [list of Edges in I graph]
        FNF = [list of FNF groups, each in its own '()']
```
Foata Normal Forms calculated in this step drive the parallel computing separate tasks in each Foata group.
The result of a program, is a matrix after gauss elimination processing. 

### Requirements
In order to run the project create virtual environment and inside run:
```
pip install -r requirements.txt
```
In order to run the visualization of Dekiert graph you have to have `Graphviz` installed on your machine.

### Instructions
* Prepare a text file following format:
```
n 
row_1
row_2
...
row_n
transposed_result_vector
```
where `n` represents size of `A` matrix and  each row is in format where every next value is separated with space
Example file is prepared in `input.txt` file.
* In `concurrent_gauss.py` file change value of `CONFIGURATION_FILE` macro according to the name of your file.
* Run 
```
python concurrent_gauss.py
```

### 
