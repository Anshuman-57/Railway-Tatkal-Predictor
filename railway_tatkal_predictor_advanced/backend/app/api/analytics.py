
from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/route-demand")
def route_demand():
    return [
        {"route":"ADI-MFP", "demand":88, "avg_wl_movement":23, "risk":"High"},
        {"route":"ADI-NDLS", "demand":81, "avg_wl_movement":31, "risk":"Medium"},
        {"route":"NDLS-MFP", "demand":93, "avg_wl_movement":19, "risk":"High"},
        {"route":"ADI-JP", "demand":62, "avg_wl_movement":42, "risk":"Low"},
    ]

@router.get("/train-popularity")
def train_popularity():
    return [
        {"train_no":"19483", "name":"Ananya Express", "score":91},
        {"train_no":"12957", "name":"Swarna Jayanti Rajdhani", "score":87},
        {"train_no":"12566", "name":"Bihar Sampark Kranti", "score":94},
        {"train_no":"19037", "name":"Avadh Express", "score":83},
    ]
