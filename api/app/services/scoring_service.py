from typing import List
from app.models.signal import NormalizedSignal

def calculate_risk_score(signals: List[NormalizedSignal]) -> float:
    """
    Deterministic scoring algorithm.
    Score = Weighted average of (Severity * Confidence)
    """
    if not signals:
        return 0.0
    
    total_weighted_severity = 0.0
    total_confidence = 0.0
    
    for signal in signals:
        # We cap severity and confidence at 1.0 just in case
        severity = min(signal.severity, 1.0)
        confidence = min(signal.confidence, 1.0)
        
        total_weighted_severity += (severity * confidence)
        total_confidence += confidence
        
    if total_confidence == 0:
        return 0.0
        
    # Final score normalized to 0-100
    base_score = (total_weighted_severity / len(signals)) * 100
    
    # Apply multipliers for volume/variety of signals
    variety_multiplier = min(1.0 + (len(set(s.signal_type for s in signals)) * 0.1), 1.5)
    
    final_score = min(base_score * variety_multiplier, 100.0)
    
    return round(final_score, 2)
