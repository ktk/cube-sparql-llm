import re

import SPARQLWrapper
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


def run_query(query: str, return_format: str = SPARQLWrapper.JSON):
    sparql = SPARQLWrapper.SPARQLWrapper(endpoint="https://ld.stadt-zuerich.ch/query") 
    sparql.setReturnFormat(return_format)
    sparql.setHTTPAuth(SPARQLWrapper.DIGEST)
    sparql.setMethod(SPARQLWrapper.POST)
    sparql.setQuery(query)
    return sparql.queryAndConvert()


def fetch_cubes_descriptions() -> str:
    cubes_query = """
        PREFIX cube: <https://cube.link/>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX qudt: <http://qudt.org/schema/qudt/>
        PREFIX dct: <http://purl.org/dc/terms/>

        CONSTRUCT {
        ?cube a cube:Cube;
                schema:name ?label;
                schema:description ?description.
        } 
        WHERE {
            ?cube a cube:Cube ;
                    schema:name ?label ;
                    schema:description ?description ;
                    dct:creator <https://register.ld.admin.ch/opendataswiss/org/bundesamt-fur-umwelt-bafu> .


            FILTER(lang(?label) = 'en')
            FILTER(lang(?description) = 'en')

            MINUS {
                ?cube schema:expires ?date .
            }
        }
    """

    raw_result = run_query(cubes_query, return_format=SPARQLWrapper.N3)
    return raw_result.decode()


def create_cube_selection_chain(api_key: str, handler: BaseCallbackHandler, temperature: float = 0.5, top_p: float = 0.5) -> LLMChain:
    cube_selection_model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-16k", temperature=temperature, top_p=top_p)

    cubes_description = """
    Given following data cubes with its labels and description:
    {cubes}
    """

    human_template = "Select a cube, which would be best to answer following question: {question}. Return cube ID."

    cube_selection_prompt = ChatPromptTemplate.from_messages([
        ("system", cubes_description),
        ("human", human_template),
    ])

    cube_selection_chain = LLMChain(prompt=cube_selection_prompt, llm=cube_selection_model, callbacks=[handler])

    return cube_selection_chain
    

def create_query_generation_chain(api_key: str, handler: BaseCallbackHandler, temperature: float = 0.2, top_p: float = 0.1) -> LLMChain:
    model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=temperature, top_p=top_p)

    sample_description = """
    Given cube and its sample observation::
    {cube_and_sample}
    """

    structure_description = """
    Dimensions labels:
    {dimensions_triplets}
    """

    query_template = """
    PREFIX cube: <https://cube.link/>
    PREFIX schema: <http://schema.org/>
    PREFIX qudt: <http://qudt.org/schema/qudt/>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT *
    WHERE {{
    {cube} a cube:Cube;
        cube:observationSet ?observationSet.

    ?observationSet a cube:ObservationSet;
        cube:observation ?observation.
    
    ?observation a cube:Observation.
    }}
    """
    human_template = f"Modify this query: {query_template}\n to get {{question}} for this cube {{cube}}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", sample_description),
        ("system", structure_description),
        ("human", human_template),
    ])

    chain = LLMChain(prompt=prompt, llm=model, callbacks=[handler])

    return chain



def parse_all_cubes(ai_response: str) -> list[str]:
    words = ai_response.split()
    cube_pattern = r'<.+>'
    groups_of_cubes = map(lambda s: re.findall(cube_pattern, s), words)

    return [cube for group in groups_of_cubes for cube in group]


def fetch_cube_sample(cube: str) -> str:
    query = f"""
        PREFIX cube: <https://cube.link/>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX qudt: <http://qudt.org/schema/qudt/>

        CONSTRUCT {{
        ?cube a cube:Cube;
            cube:observationSet ?observationSet.
        ?observationSet a cube:observationSet;
            cube:observation ?s.
        ?s ?p ?o.
        }}
        WHERE {{
        {{
            SELECT (SAMPLE(?observation) AS ?s)
            WHERE {{
            VALUES ?cube {{ {cube} }}
            ?cube a cube:Cube ;
                    cube:observationSet ?observationSet.
            ?observationSet cube:observation ?observation.
            }}
        }}
        ?cube a cube:Cube;
            cube:observationSet ?observationSet.
        ?observationSet a cube:ObservationSet;
            cube:observation ?s.
        ?s ?p ?o .
        }}
    """

    raw_result = run_query(query, return_format=SPARQLWrapper.N3)
    return raw_result.decode()


def fetch_dimensions_triplets(cube: str) -> str:
    query = f"""
        PREFIX cube: <https://cube.link/>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX qudt: <http://qudt.org/schema/qudt/>

        CONSTRUCT {{
        ?values schema:name ?label.
        }}
        WHERE {{
            SELECT ?values ?label
            WHERE {{
                VALUES ?cube {{ {cube} }}
                
                ?cube a cube:Cube ;
                    cube:observationConstraint ?shape .
                
                ?shape a cube:Constraint;
                    sh:property ?property .
                    
                ?property sh:path ?dimensions ;
                sh:in ?list .

                ?list rdf:rest*/rdf:first ?values .

                ?values schema:name ?label .

                FILTER( lang(?label) = 'en')
            }}
        }} 
    """

    raw_result = run_query(query, return_format=SPARQLWrapper.N3)
    return raw_result.decode()
