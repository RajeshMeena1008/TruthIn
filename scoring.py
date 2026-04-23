"""
scoring.py
Nutrition-based health scoring system (0-100) + goal-based verdict.
"""

SCORE_CONFIG = {
    "calories": (400, 250, 25, True),
    "fat":      (20,  10,  20, True),
    "sugar":    (15,  5,   20, True),
    "protein":  (5,   15,  20, False),  # higher = better
    "sodium":   (600, 300, 15, True),
}
HARMFUL_PENALTY = 15


def compute_health_score(nutrition: dict, has_harmful: bool = False) -> int:
    score = 100.0
    for key, (bad, ok, weight, inverted) in SCORE_CONFIG.items():
        val = float(nutrition.get(key, 0) or 0)
        if inverted:
            if val >= bad:
                score -= weight
            elif val >= ok:
                score -= weight * ((val - ok) / (bad - ok))
        else:
            if val < bad:
                score -= weight * 0.5
            elif val < ok:
                score -= weight * ((ok - val) / (ok - bad))
    if has_harmful:
        score -= HARMFUL_PENALTY
    return max(0, min(100, round(score)))


def classify_score(score) -> str:
    s = int(score)
    if s >= 80:   return "Healthy"
    elif s >= 50: return "Moderate"
    else:         return "Unhealthy"


def get_goal_verdict(nutrition: dict, goal: str) -> tuple[str, bool]:
    """
    Returns (verdict_text, is_good_for_goal).
    goal: 'Weight Loss' | 'Weight Gain' | 'General Health'
    """
    cal = float(nutrition.get("calories", 0) or 0)
    fat = float(nutrition.get("fat", 0) or 0)
    protein = float(nutrition.get("protein", 0) or 0)

    if goal == "Weight Loss":
        if cal <= 250 and fat <= 10:
            return "✅ Great for Weight Loss — low calorie & low fat", True
        else:
            return "❌ Not ideal for Weight Loss — high calorie/fat content", False

    elif goal == "Weight Gain":
        if cal >= 300 or fat >= 14 or protein >= 15:
            return "✅ Good for Weight Gain — calorie-dense or protein-rich", True
        else:
            return "❌ Low energy — may not help with Weight Gain goals", False

    return "", True  # General Health — no verdict


def get_recommendations(nutrition: dict, classification: str) -> list[str]:
    recs = []
    cal    = float(nutrition.get("calories", 0) or 0)
    sugar  = float(nutrition.get("sugar", 0) or 0)
    fat    = float(nutrition.get("fat", 0) or 0)
    sodium = float(nutrition.get("sodium", 0) or 0)
    protein= float(nutrition.get("protein", 0) or 0)

    if cal > 450:
        recs.append("🔥 High calorie — consider smaller portions.")
    if sugar > 20:
        recs.append("🍬 Excess sugar — consume in moderation.")
    elif sugar > 10:
        recs.append("⚠️ Moderate sugar — balance with fiber-rich foods.")
    if fat > 25:
        recs.append("🧈 High fat content — opt for healthier fat sources.")
    if sodium > 700:
        recs.append("🧂 Very high sodium — raises blood pressure risk.")
    elif sodium > 350:
        recs.append("🧂 Moderate sodium — stay well hydrated today.")
    if protein >= 20:
        recs.append("💪 Good protein content — great for muscle maintenance.")
    elif protein < 5:
        recs.append("💪 Low protein — pair with eggs, legumes, or lean meat.")

    if classification == "Healthy":
        recs.append("✅ Low calorie & nutritious — diet friendly choice.")
    elif classification == "Moderate":
        recs.append("📋 Acceptable in a balanced diet — not a daily staple.")
    else:
        recs.append("🚨 Unhealthy rating — limit intake and explore alternatives.")

    return recs
