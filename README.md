# rdf-qa

_Explainable complex question answering over RDF files via Llama Index._

## Usage

Install dependencies:

```bash
pip3 install --upgrade llama_index openai
```

Store OpenAI API key:

```bash
export OPENAI_API_KEY=<your-key>
```

Example usage:

```python
from llama_index import GPTSimpleVectorIndex, download_loader

RDFReader = download_loader("RDFReader")
document = RDFReader().load_data(file="./example.nt")
index = GPTSimpleVectorIndex(document)

result = index.query(
  "list all places in a quoted Python array, then explain why")
print(result.response)
# >>> ['Lombardy', 'Milan', 'Piedmont']
# >>>
# >>> The answer is ['Lombardy', 'Milan', 'Piedmont'] because all three 
# >>> of these are listed as types of places in the context information. 
# >>> Lombardy and Piedmont are both listed as types of regions, and 
# >>> Milan is listed as a type of city. All three of these are 
# >>> subclasses of the type 'place', which is a subclass of 'thing'.
```

![Visualisation of the example RDF graph.](https://github.com/mommi84/rdf-qa/raw/main/images/example-nt.png "Visualisation of the example RDF graph.")

## API

```bash
pip3 install flask
```

```bash
python3 server.py
```

The endpoint will be available at `localhost:5050` by default.

### Indexing

Endpoint: `/index` (POST)

Form data:
* `file`: the RDF file to index

This will return the internal ID of the index, to be used for querying.

### Query

Endpoint: `/query` (GET)

Parameters:
* `id`: internal ID of the index
* `query`: url-encoded query

E.g., http://localhost:5050/query?id=5aa30cf341cc0fd1494da302649b04&query=list%20all%20regions

## Webapp

```bash
pip3 install flask streamlit
```

Refresh terminal session or open new terminal.

```bash
streamlit run app.py 
```

![Screenshot of the webapp.](https://github.com/mommi84/rdf-qa/raw/main/images/webapp.png "Screenshot of the webapp.")

