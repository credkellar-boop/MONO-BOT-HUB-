import hashlib
import os

def verify_deed_integrity(expected_hash: str) -> bool:
    """
    Ensures the bot is operating under a valid, untampered Master Deed.
    If the PDF is modified or missing, the bot self-terminates.
    """
    deed_path = "legal/master_deed.pdf"
    
    if not os.path.exists(deed_path):
        print("CRITICAL: Master Deed missing. Unauthorized operation.")
        return False
        
    with open(deed_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    if file_hash == expected_hash:
        print("LEGAL CHECK: Master Deed Verified.")
        return True
    else:
        print("CRITICAL: Master Deed Mismatch. Potential hijacking detected.")
        return False
