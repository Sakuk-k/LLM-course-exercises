import sys
import os
import sqlite3
import time
import re
import requests
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class ProcurementState(TypedDict):
    request: str
    vendors: list[dict]
    quotes: list[dict]
    best_quote: dict
    approval_status: str
    po_number: str
    notification: str


api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key
)


def extract_quantity(request: str) -> int:
    match = re.search(r"\d+", request)
    if match:
        return int(match.group())
    return 1


@tool
def get_unit_price(vendor: str) -> float:
    """Return the laptop unit price for a given vendor."""
    url = "https://dummyjson.com/products/category/laptops"
    try:
        r = requests.get(url)
        products = r.json()["products"]
        cheapest = min(products, key=lambda p: p["price"])
        return float(cheapest["price"])
    except Exception:
        fallback = {
            "Dell": 248,
            "Lenovo": 235,
            "HP": 259
        }
        return fallback.get(vendor, 250)


def lookup_vendors(state: ProcurementState) -> dict:
    print("\n[Step 1] Looking up approved vendors...")
    time.sleep(1)
    vendors = [
        {"name": "Dell", "id": "V-001", "category": "laptops", "rating": 4.5},
        {"name": "Lenovo", "id": "V-002", "category": "laptops", "rating": 4.3},
        {"name": "HP", "id": "V-003", "category": "laptops", "rating": 4.1},
    ]
    for v in vendors:
        print(f"   Found vendor: {v['name']} (rating {v['rating']})")
    return {"vendors": vendors}


def fetch_pricing(state: ProcurementState) -> dict:
    print("\n[Step 2] Fetching pricing from suppliers...")

    quantity = extract_quantity(state["request"])
    quotes = []

    for vendor in state["vendors"]:
        name = vendor["name"]
        unit_price = get_unit_price.invoke({"vendor": name})
        total = unit_price * quantity

        quote = {
            "vendor": name,
            "unit_price": unit_price,
            "quantity": quantity,
            "total": total,
            "delivery_days": 5
        }

        print(f"   {name}: €{unit_price}/unit x {quantity} = €{total:,}")
        quotes.append(quote)

    return {"quotes": quotes}


def compare_quotes(state: ProcurementState) -> dict:
    print("\n[Step 3] Comparing quotes...")
    time.sleep(0.5)
    best = min(state["quotes"], key=lambda q: q["total"])
    print(f"   Best quote: {best['vendor']} at €{best['total']:,}")
    print(f"   (Saves €{max(q['total'] for q in state['quotes']) - best['total']:,} "
          f"vs most expensive option)")
    return {"best_quote": best}


def request_approval(state: ProcurementState) -> dict:
    best = state["best_quote"]
    quantity = best.get("quantity", 0)

    print("\n[Step 4] Order exceeds €10,000 — manager approval required!")
    print(f"   Sending approval request to manager...")

    amount_str = f"€{best['total']:,}"
    delivery_str = f"{best['delivery_days']} business days"

    print(f"   ┌─────────────────────────────────────────────┐")
    print(f"   │  APPROVAL NEEDED                            │")
    print(f"   │  Vendor:   {best['vendor']:<33}│")
    print(f"   │  Amount:   {amount_str:<33}│")
    print(f"   │  Items:    {quantity} laptops{' '*(29-len(str(quantity)))}│")
    print(f"   │  Delivery: {delivery_str:<33}│")
    print(f"   └─────────────────────────────────────────────┘")

    decision = interrupt({
        "message": f"Approve purchase of {quantity} laptops from {best['vendor']} for €{best['total']:,}?",
        "vendor": best["vendor"],
        "amount": best["total"],
    })

    print(f"\n[Step 4] Manager responded: {decision}")
    return {"approval_status": decision}


def submit_purchase_order(state: ProcurementState) -> dict:
    print("\n[Step 5] Submitting purchase order to ERP system...")
    time.sleep(1)

    po_number = "PO-2026-00342"

    print(f"   Purchase order created: {po_number}")
    print(f"   Vendor: {state['best_quote']['vendor']}")
    print(f"   Amount: €{state['best_quote']['total']:,}")

    return {"po_number": po_number}


def notify_employee(state: ProcurementState) -> dict:
    print("\n[Step 6] Notifying employee...")

    quantity = state["best_quote"].get("quantity", 0)

    if "reject" in state.get("approval_status", "").lower():
        prompt = (
            f"Write a brief professional message telling the employee that their "
            f"request for {quantity} laptops was rejected by the manager."
        )
    else:
        prompt = (
            f"Write a brief professional message confirming approval of "
            f"{quantity} laptops from {state['best_quote']['vendor']} "
            f"for €{state['best_quote']['total']:,}. "
            f"PO number {state['po_number']}."
        )

    response = llm.invoke(prompt)
    notification = response.content

    print(notification)

    return {"notification": notification}


def approval_router(state: ProcurementState):
    best = state["best_quote"]
    if best["total"] > 10000:
        return "approval"
    else:
        return "skip"


def approval_result_router(state: ProcurementState):
    status = state["approval_status"].lower()
    if "reject" in status:
        return "rejected"
    else:
        return "approved"


builder = StateGraph(ProcurementState)

builder.add_node("lookup_vendors", lookup_vendors)
builder.add_node("fetch_pricing", fetch_pricing)
builder.add_node("compare_quotes", compare_quotes)
builder.add_node("request_approval", request_approval)
builder.add_node("submit_purchase_order", submit_purchase_order)
builder.add_node("notify_employee", notify_employee)

builder.add_edge(START, "lookup_vendors")
builder.add_edge("lookup_vendors", "fetch_pricing")
builder.add_edge("fetch_pricing", "compare_quotes")

builder.add_conditional_edges(
    "compare_quotes",
    approval_router,
    {
        "approval": "request_approval",
        "skip": "submit_purchase_order"
    }
)

builder.add_conditional_edges(
    "request_approval",
    approval_result_router,
    {
        "approved": "submit_purchase_order",
        "rejected": "notify_employee"
    }
)

builder.add_edge("submit_purchase_order", "notify_employee")
builder.add_edge("notify_employee", END)


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "procurement_checkpoints.db")
THREAD_ID = "procurement-thread-1"
config = {"configurable": {"thread_id": THREAD_ID}}


def run_first_invocation(graph):
    print("=" * 60)
    print("FIRST INVOCATION")
    print("=" * 60)

    graph.invoke(
        {"request": "Order 50 laptops for the new engineering team"},
        config,
    )


def run_second_invocation(graph):
    print("=" * 60)
    print("SECOND INVOCATION")
    print("=" * 60)

    graph.invoke(
        Command(resume="Approved — go ahead with the purchase."),
        config,
    )


if __name__ == "__main__":
    resume_mode = "--resume" in sys.argv

    if not resume_mode and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    graph = builder.compile(checkpointer=checkpointer)

    try:
        if resume_mode:
            run_second_invocation(graph)
        else:
            run_first_invocation(graph)
    finally:
        conn.close()