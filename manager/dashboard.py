from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime

app = FastAPI(title="Monad Shield Fleet Command")

# Simple in-memory storage for fleet status
fleet_health = {}

@app.post("/heartbeat")
async def receive_heartbeat(request: Request):
    data = await request.json()
    bot_id = data.get("bot_id")
    
    # Store the latest status from the worker bot
    fleet_health[bot_id] = {
        "status": data.get("status"),
        "last_block": data.get("block"),
        "balance": data.get("balance"),
        "timestamp": datetime.now().isoformat()
    }
    return {"status": "recorded"}

@app.get("/status")
async def get_fleet_status():
    # Returns the overview of all 700 bots
    return fleet_health

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
