import json
import os
import pandas as pd
from datetime import datetime

def generate_fleet_report():
    """Aggregates all bot statuses into a 'Max' executive summary."""
    manifest_path = 'configs/fleet_manifest.json'
    audit_report_path = 'GLOBAL_FLEET_AUDIT_2026.csv'
    
    if not os.path.exists(manifest_path):
        print("ERROR: Manifest not found.")
        return

    with open(manifest_path, 'r') as f:
        fleet = json.load(f)

    total_bots = len(fleet)
    active_bots = sum(1 for bot in fleet if bot['status'] == 'active')
    
    print(f"--- MONO-BOT-HUB STATUS [{datetime.now().strftime('%Y-%m-%d %H:%M')}] ---")
    print(f"Total Fleet: {total_bots} | Online: {active_bots} | Health: {(active_bots/total_bots)*100:.1f}%")
    
    if os.path.exists(audit_report_path):
        df = pd.read_csv(audit_report_path)
        threats = len(df)
        total_value_secured = df['amount'].sum() if 'amount' in df.columns else 0
        print(f"Recent Threats Flagged: {threats}")
        print(f"Total Value Under Protection: ${total_value_secured:,.2f}")
    else:
        print("Audit Engine: Waiting for first hourly sync...")
    print("-" * 50)

if __name__ == "__main__":
    generate_fleet_report()
