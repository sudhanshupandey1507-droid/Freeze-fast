from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="FreezeFast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    new_payee: bool = False
    unusual_location: bool = False
    urgent_transfer: bool = False
    reported_suspicious: bool = False

@app.get("/")
def home():
    return {"message": "FreezeFast backend is running"}

@app.post("/assess")
def assess(tx: Transaction):
    score = 0
    reasons = []

    if tx.new_payee:
        score += 20
        reasons.append("New recipient")

    if tx.unusual_location:
        score += 25
        reasons.append("Unusual location")

    if tx.urgent_transfer:
        score += 20
        reasons.append("Urgent transfer pressure")

    if tx.reported_suspicious:
        score += 40
        reasons.append("Reported suspicious activity")

    if tx.amount >= 50000:
        score += 15
        reasons.append("High amount in demo rules")

    score = min(score, 100)

    if score >= 60:
        risk = "HIGH"
        action = "Contact your bank immediately using its official channel."
    elif score >= 30:
        risk = "MEDIUM"
        action = "Verify the recipient before proceeding."
    else:
        risk = "LOW"
        action = "No strong demo rule triggered. This does not guarantee safety."

    return {
        "transaction_id": tx.transaction_id,
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons,
        "recommended_action": action,
        "money_frozen": False,
        "mode": "SIMULATION_ONLY"
    }
