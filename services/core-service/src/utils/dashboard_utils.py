from collections import Counter
from collections import defaultdict
from typing import Dict
from bson import ObjectId


async def count_scores_overall(resume_list, mongo_collection):
    analyzed_ids = [resume.analysis_id for resume in resume_list if resume.analysis_id]
    object_ids = [
        ObjectId(id) if not isinstance(id, ObjectId) else id for id in analyzed_ids
    ]
    cursor = mongo_collection.find({"_id": {"$in": object_ids}}, {"overall_score": 1})

    counts = Counter({"above_80": 0, "below_or_equal_80": 0})
    async for doc in cursor:
        score = doc.get("overall_score", 0)
        if score > 80:
            counts["above_80"] += 1
        else:
            counts["below_or_equal_80"] += 1

    return counts


async def get_monthly_score_breakdown_from_mongo(
    mongo_collection, analysis_id_to_month: Dict[str, str]
) -> Dict[str, Dict[str, int]]:
    score_counts = defaultdict(lambda: {"score_gt_80": 0, "score_lte_80": 0})

    if not analysis_id_to_month:
        return score_counts

    object_ids = [
        ObjectId(aid) if not isinstance(aid, ObjectId) else aid
        for aid in analysis_id_to_month.keys()
    ]

    cursor = mongo_collection.find({"_id": {"$in": object_ids}}, {"overall_score": 1})

    async for doc in cursor:
        score = doc.get("overall_score", 0)
        month = analysis_id_to_month.get(str(doc["_id"]))
        if not month:
            continue
        if score > 80:
            score_counts[month]["score_gt_80"] += 1
        else:
            score_counts[month]["score_lte_80"] += 1

    return score_counts
