# spin2vesta
Converts a [CASTEP](https://www.castep.org/) ```.cell``` file into a [VESTA](https://jp-minerals.org/vesta/en/) ```.vesta``` file with spin arrows.
### Using the command line
```
python3 spin2vesta.py -s [SEED] -o [OUTPUT]
```
- ```-s``` specifies the seed of the input ```.cell``` file (required)
- ```-o``` specifies the seed of the output ```.vesta``` file (optional)
    - if not specified the output file will be named ```[SEED]_vectors.vesta```
### From within another python file
```
import spin2vesta as sv

sv.convert([SEED],[OUTPUT])
```