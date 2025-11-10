import math

def compute_scores(pe, eps, rev, rsi):
    try:
        quant = max(0, 100 - min(pe or 200, 200) / 2)
        growth = min(100, ((eps or 0) + (rev or 0)) * 50)
        quality = 100 - abs(rsi - 50)
        overall = round((quant * 0.4 + growth * 0.4 + quality * 0.2), 2)
        return {
            "quant": round(quant, 2),
            "quality": round(growth, 2),
            "catalyst": round(quality, 2),
            "overall_score": overall,
        }
    except Exception:
        return {"quant": 0, "quality": 0, "catalyst": 0, "overall_score": 0}


def stance_from_overall(score):
    if score >= 75:
        return "Buy"
    elif score >= 50:
        return "Hold"
    else:
        return "Wait"
