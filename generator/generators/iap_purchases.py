"""Generator for In-App Purchases (IAP)."""
import uuid
import random
from datetime import timedelta
from typing import List, Dict, Any
from generator.utils.dates import parse_datetime

def generate_iap_purchases(installs: List[Dict[str, Any]], game_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate IAP transactions simulating payer behavior and refunds."""
    purchases = []
    
    # Identify payers (e.g., 5% of players)
    player_install_map = {p["player_id"]: p for p in installs}
    
    # Find all sessions to attach purchases to active gameplay
    sessions_by_player = {}
    for evt in game_events:
        if evt["event_name"] == "session_start":
            pid = evt["player_id"]
            if pid not in sessions_by_player:
                sessions_by_player[pid] = []
            sessions_by_player[pid].append(evt)
            
    products = [
        {"id": "starter_pack", "price": 1.99},
        {"id": "gem_pack_small", "price": 4.99},
        {"id": "gem_pack_medium", "price": 9.99},
        {"id": "gem_pack_large", "price": 19.99},
        {"id": "remove_ads", "price": 2.99}
    ]
    
    for player_id, sessions in sessions_by_player.items():
        install = player_install_map.get(player_id)
        if not install:
            continue
            
        # Payer probability (slightly higher for engaged players)
        payer_prob = 0.05 + (min(len(sessions), 50) * 0.001)
        if random.random() > payer_prob:
            continue
            
        # Player is a payer. They might make 1 to 5 purchases across their sessions
        num_purchases = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.15, 0.07, 0.03])[0]
        
        # Pick random sessions to make purchases in
        purchase_sessions = random.choices(sessions, k=min(num_purchases, len(sessions)))
        
        for sess in purchase_sessions:
            product = random.choice(products)
            sess_time = parse_datetime(sess["event_time"])
            # Purchase happens a few minutes into the session
            purchase_time = sess_time + timedelta(seconds=random.randint(60, 300))
            
            status = "completed"
            # Introduce intentional refunds (about 3% of purchases)
            if random.random() < 0.03:
                status = "refunded"
                
            txn_hex = f"{random.getrandbits(32):08x}".upper()
            
            purchases.append({
                "transaction_id": f"TXN_{txn_hex}",
                "player_id": player_id,
                "game_id": install["game_id"],
                "product_id": product["id"],
                "purchase_time": purchase_time.isoformat() + "Z",
                "platform": install["platform"],
                "country": install["country"],
                "currency": "USD",
                "gross_price": product["price"],
                "price_usd": product["price"],
                "transaction_status": status
            })
            
    # Sort chronologically
    purchases.sort(key=lambda x: x["purchase_time"])
    return purchases
