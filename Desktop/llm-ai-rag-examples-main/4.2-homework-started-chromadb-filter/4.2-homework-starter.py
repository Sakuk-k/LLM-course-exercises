"""
ChromaDB Search & Filter Exercises
===================================
Starter code — shared knowledge base for all four exercises.

Install dependency:
    pip install chromadb

Run:
    python chroma_exercises_starter.py
"""

import chromadb

documents = [
    "To connect to the university VPN, install the GlobalProtect client from software.uni.fi and authenticate with your student credentials.",
    "The VPN service is maintained every Tuesday between 06:00 and 07:00. Connections will be interrupted during this window.",
    "If the VPN disconnects repeatedly, try switching the server region from 'EU-West' to 'EU-North' in GlobalProtect settings.",
    "Student email accounts are hosted on Microsoft 365. Your address is firstname.lastname@student.uni.fi.",
    "Email accounts are deactivated 12 months after graduation. Export your data before that deadline using the IT portal.",
    "The maximum email attachment size is 25 MB. Use OneDrive to share larger files.",
    "MATLAB is available for all students via the campus licence. Download it from software.uni.fi using your student ID.",
    "Microsoft Office 365 is included in your student account at no cost. Install up to five devices.",
    "Adobe Creative Cloud is available for ICT and Design students only. Request access through the IT helpdesk portal.",
    "The campus Wi-Fi network is called UniNet. Use your student credentials to authenticate via the captive portal.",
    "Eduroam is available on campus and at partner universities worldwide. Configure it with your full student email address.",
    "Wired ethernet ports in library study rooms operate at 1 Gbps. Contact IT if a port is inactive.",
    "Passwords must be at least 12 characters and include uppercase, lowercase, a digit, and a special character.",
    "Your student account is created within 24 hours of enrolment confirmation. Check your personal email for the activation link.",
    "Multi-factor authentication (MFA) is mandatory for all student accounts from September 2025 onwards.",
    "Campus printers accept UniPrint credits. Load credits at any campus info desk or online at print.uni.fi.",
    "The default print quota is 200 pages per semester. ICT students receive an additional 100 pages.",
    "Colour printing costs 0.15 EUR per page. Black-and-white printing costs 0.04 EUR per page.",
]

metadatas = [
    {"category": "vpn", "priority": "high", "year": 2025, "verified": True},
    {"category": "vpn", "priority": "medium", "year": 2025, "verified": True},
    {"category": "vpn", "priority": "low", "year": 2024, "verified": True},
    {"category": "email", "priority": "high", "year": 2025, "verified": True},
    {"category": "email", "priority": "medium", "year": 2024, "verified": True},
    {"category": "email", "priority": "low", "year": 2025, "verified": False},
    {"category": "software", "priority": "medium", "year": 2025, "verified": True},
    {"category": "software", "priority": "low", "year": 2025, "verified": True},
    {"category": "software", "priority": "low", "year": 2024, "verified": False},
    {"category": "network", "priority": "high", "year": 2025, "verified": True},
    {"category": "network", "priority": "high", "year": 2025, "verified": True},
    {"category": "network", "priority": "low", "year": 2024, "verified": True},
    {"category": "accounts", "priority": "high", "year": 2025, "verified": True},
    {"category": "accounts", "priority": "high", "year": 2025, "verified": True},
    {"category": "accounts", "priority": "high", "year": 2025, "verified": True},
    {"category": "printing", "priority": "medium", "year": 2025, "verified": True},
    {"category": "printing", "priority": "low", "year": 2025, "verified": True},
    {"category": "printing", "priority": "low", "year": 2025, "verified": True},
]

ids = [f"doc-{i:03d}" for i in range(len(documents))]

client = chromadb.EphemeralClient()
collection = client.get_or_create_collection("it_helpdesk")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

print(f"Collection ready — {collection.count()} documents loaded.\n")
print("=" * 60)


def print_results(label, results, show_distances=False):
    print(f"\n>>> {label}")

    is_query = isinstance(results["ids"][0], list)

    ids_list = results["ids"][0] if is_query else results["ids"]
    docs_list = results["documents"][0] if is_query else results["documents"]
    metas_list = results["metadatas"][0] if is_query else results["metadatas"]
    dists_list = results.get("distances", [[]])[0] if is_query else []

    if not ids_list:
        print("  (no results)")
        return

    for i, (doc_id, doc, meta) in enumerate(zip(ids_list, docs_list, metas_list)):
        dist_str = f"  distance={dists_list[i]:.4f}" if show_distances and dists_list else ""
        print(f"  [{doc_id}] [{meta['category']}] [{meta['priority']}]{dist_str}")
        print(f"    {doc[:90]}{'...' if len(doc) > 90 else ''}")


print("\n--- EXERCISE 1: Basic metadata filter ---")

results = collection.get(
    where={"category": "vpn"}
)

print_results("VPN documents", results)


print("\n--- EXERCISE 2: Combined metadata filters ---")

results = collection.get(
    where={
        "$and": [
            {"priority": "high"},
            {"year": 2025},
            {"verified": True}
        ]
    }
)

print_results("High priority 2025 verified docs", results)

results = collection.get(
    where={
        "$or": [
            {"category": "software"},
            {"category": "printing"}
        ]
    }
)

print_results("Software OR Printing docs", results)


print("\n--- EXERCISE 3: Full text search ---")

results = collection.get(
    where_document={"$contains": "student"}
)

print_results("Documents containing 'student'", results)

results = collection.get(
    where_document={
        "$and": [
            {"$contains": "student"},
            {"$not_contains": "password"}
        ]
    }
)

print_results("Contains 'student' but NOT 'password'", results)


print("\n--- EXERCISE 4: Semantic query + metadata filter + text filter ---")

results = collection.query(
    query_texts=["how do I print documents on campus"],
    n_results=5,
    where={"category": "printing"},
    where_document={"$contains": "page"},
    include=["documents", "metadatas", "distances"]
)

print_results("Filtered semantic search", results, show_distances=True)