# Curator

Curator is a migration tool developed to aid The Center for the Study of New Testament Manuscripts in their
back log of data that is not stored in their database.

## Installation
Install the dependencies in the requirements.txt file
```shell
pip install -r requirements.txt
```

## Usage
Run the python script inside the directory with the PDFs.
```shell
python curator.py <filename>.pdf
```
to process a specific PDF, or
```shell
python curator.py
```
to process every PDF in the directory.

Running the script will produce a JSON file containing the data which can be loaded into the database.
Instructions to do that are coming soon.
