"""
ChromaDB Sailing Knowledge Base - Vector Database Intro

This script demonstrates the core concepts of a vector database using ChromaDB.
It builds a small sailing knowledge base by storing text documents as vector
embeddings, then performs semantic similarity searches against them.

Key concepts covered:
  - Creating and persisting a ChromaDB collection
  - Using ChromaDB's built-in embedding model (all-MiniLM-L6-v2 via onnxruntime)
    to automatically convert text into vector embeddings on insert and query
  - Performing a similarity search using natural language and interpreting
    the distance scores returned (lower = more similar)
"""

import chromadb

DATABASE_FILE_PATH = "./chroma_db_data"  # Path where ChromaDB will store its data


def initVectorDb():
    print("Initializing vector database...")
    exampleSourceDocuments = [
        "DOC-001: The 2026 Emerald Bay Championship is scheduled for June 12-14. The Regatta Office is temporarily relocated to the 'Rusty Anchor Tavern' due to pier renovations.",
        "DOC-002: SPECIAL RULE: The 'Obsidian Reach' channel is designated a 'No-Tack Zone' this year. Boats found tacking within the channel markers will receive a 20% scoring penalty (Rule 14.2).",
        "DOC-003: 2026 COURSE UPDATE: The traditional 'Buoy Alpha' has been replaced by a floating solar barge named 'Sun-Ray 1'. All competitors must leave Sun-Ray 1 to starboard.",
        "DOC-004: FLAG SIGNALS: A unique 'checkered purple flag' displayed on the Committee Boat signifies an immediate shark-sighting suspension. Return to the Rusty Anchor Tavern immediately.",
        "DOC-005: 2025 PODIUM RECAP: Last year's winner was the yacht 'Silver Wake' skippered by Captain Elias Thorne. Second place went to 'Blue Mist' (Sarah Chen) and third to 'Wind-Dancer' (Markus Vane).",
        "DOC-006: HISTORICAL DISQUALIFICATION: In 2025, the yacht 'Storm-Petrel' was disqualified for using an unauthorized experimental hydrofoil in the 'No-Lift' division.",
        "DOC-007: THE 'WHISPERING REEF' HAZARD: Due to shifting sands in early 2026, the Whispering Reef now has a minimum depth of only 1.2 meters at low tide. This is 0.5m shallower than listed on official charts.",
        "DOC-008: SCORING SYSTEM: The 2026 Regatta uses the 'Low-Point-Plus' system. A first-place finish earns 0.7 points (instead of the standard 1.0) to reward dominant performance.",
        "DOC-009: CREW REQUIREMENTS: All boats in the 'Masters' division must have at least one crew member over the age of 65 and one under the age of 18, to promote 'intergenerational mentorship'.",
        "DOC-010: WEATHER PROTOCOL: If wind speeds exceed 28 knots, the race is moved to 'Sector 7' (The Sheltered Lagoon). If it drops below 4 knots, a 'Paddle-Off' tiebreaker is held at the docks."
    ]

    # PersistentClient stores the database on disk so data survives between runs
    client = chromadb.PersistentClient(path=DATABASE_FILE_PATH)

    # get_or_create_collection avoids errors if the collection already exists
    # ChromaDB uses its built-in embedding model (all-MiniLM-L6-v2 via onnxruntime) by default
    collection = client.get_or_create_collection(name="sailing_knowledge_base")

    # Assume the collection is already initialized if it contains the same number of documents as our example set
    if(collection.count() == exampleSourceDocuments.__len__()):
        print("Collection already initialized with example documents.")
        return  
    
    # Add documents - ChromaDB automatically generates embeddings for them
    collection.add(
        documents=exampleSourceDocuments,
        ids=[str(i) for i in range(len(exampleSourceDocuments))]
    )

    print(f"Inserted {len(exampleSourceDocuments)} documents into the collection.")
    print("Vector database initialized successfully.")


def queryVectorDb(query):
    print(f"Querying vector database for: {query}")

    client = chromadb.PersistentClient(path=DATABASE_FILE_PATH)
    collection = client.get_collection(name="sailing_knowledge_base")

    # ChromaDB automatically embeds the query text using the same built-in model
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    print(f"Found {len(results['documents'][0])} results for the query.")
    return results


initVectorDb()  # Initialize the vector database and insert example documents

##
## Now we can perform a similarity search on the collection.
##

# Here is our example search query in plain text.
search_query = "Who won the regatta last year"

# To search, we can now use the queryVectorDb function.
results = queryVectorDb(search_query)
print("Results and scores (smaller distance is better)\n###########################################################")

# Print the results, zip documentation here: https://www.w3schools.com/python/ref_func_zip.asp
# In short the zip function allows us to iterate over two lists in parallel, in this case the list of result documents and their corresponding distance scores.
for doc, distance in zip(results['documents'][0], results['distances'][0]):
    print(f"Result document: {doc}")
    print(f"Score: {distance:.4f}\n")
