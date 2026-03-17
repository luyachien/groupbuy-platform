from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math
from fastapi import Query

app = FastAPI()

class GroupBuy(BaseModel):
    id: int
    title: str
    description: str
    price: float
    lat: float   # 緯度
    lng: float   # 經度

# 假資料庫
groupbuys: List[GroupBuy] = []

@app.get("/")
def read_root():
    return {"message": "Hello GroupBuy API 🚀"}

@app.post("/groupbuys")
def create_groupbuy(groupbuy: GroupBuy):
    groupbuys.append(groupbuy)
    return {"message": "GroupBuy created successfully"}

@app.get("/groupbuys")
def get_groupbuys():
    return groupbuys

def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # 地球半徑 km
    dLat = math.radians(lat2 - lat1)
    dLng = math.radians(lng2 - lng1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/nearby-groupbuys")
def get_nearby_groupbuys(lat: float = Query(...), lng: float = Query(...), radius: float = 3):
    # 找出 radius km 內的團購
    nearby = []
    for gb in groupbuys:
        dist = haversine(lat, lng, gb.lat, gb.lng)
        if dist <= radius:
            nearby.append({
                "id": gb.id,
                "title": gb.title,
                "description": gb.description,
                "price": gb.price,
                "lat": gb.lat,
                "lng": gb.lng,
                "distance": round(dist, 2)
            })
    return nearby