# README
This pipeline can be used to analyze the results of a MaxQuant analysis.

## Requirements
It is recommended to use this pipeline with git and anaconda, which need to be installed if they aren't
already. Proxies need to be set for these tools if they are set up (like in the DKFZ).
The repository can be downloaded for example via
`git clone https://github.com/siheming/klingmueller_maxquantpipeline.git` or other ways.

## Usage
This pipeline can be used via the command line and needs a python
installation with certain packages. A virtual environment is recommended
with all packages specified in the `environment.yml` file. This can be
done for example via:
```bash
conda env create python=3.7 -f environment.yml
```
which can then be activated and deactivated via:
```bash
conda activate mqpipeline # activation
conda deactivate  # deactivation
```
When the environment is activated or the default python installation
satisfies the requirements the script can be used via:
```bash
python3 MQPipeline.py
```
or
```bash
python MQPipeline.py
```
If the script is started with no further arguments the first prompt will ask for the directory,
the second promp for the yml config file. If the second prompt is cancelled the default yml file is used
To see help for the command line support type:
```bash
python3 MQPipeline.py --help
```
The arguments that can be specified when using the pipeline are:
- `--dir` the path to the directory that should be analyzed.
When this is not specified a window will open and ask to select a directory
- `--yml-file` the path to a yml file which should be used for analysis.
If the directory contains a config dir with a yml file it will be used
for analysis. Otherwise the user will be asked to select a yml file.
When this is skipped the default yml file will be used instead.
Using the default yml file can also be forced via `--yml-file default`
- `--loglevel` Logging level used during run. Should be from options 
(lowest to highest): DEBUG < INFO < WARNING < ERROR.
- `--has_replicates` does the max quant result file contain replicates.
Should be y or n (yes or no).

## Dependencies
The pipeline required multiple input files to perform the analysis. They
should be stored in a config dir on the same level as the pipeline script.
The requirements are:
- `ms_analysis_default.yml` a file which contains all defaults for the 
analysis pipeline.
- `important_protein_names.xlsx` a file which contains proteins which
should be analyzed. These impact descriptive plots and the score calculation.
- `important_receptor_names.xlsx` a file with receptors.
- `go_analysis_gene_names.xlsx` a file which contains GO annotations for the
enrichment analysis.

## Support
If additional support is required try googleing, asking a programmer or
contact me via `Simon.Heming@gmx.de`.