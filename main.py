from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

app = FastAPI()

# 允許所有網頁存取（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GroupBuy(BaseModel):
    id: int
    title: str
    description: str
    price: float
    lat: float
    lng: float
    people_joined: int
    people_limit: int
    deadline: str

# 假資料庫，先留空
groupbuys: List[GroupBuy] = []

@app.get("/")
def read_root():
    return {"message": "Hello GroupBuy API 🚀"}

@app.post("/groupbuys")
def create_groupbuy(groupbuy: GroupBuy):
    groupbuys.append(groupbuy)
    return {"message": "GroupBuy created successfully"}

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLng = math.radians(lng2 - lng1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/nearby-groupbuys")
def get_nearby_groupbuys(lat: float = Query(...), lng: float = Query(...), radius: float = 3):
    nearby = []
    for gb in groupbuys:
        dist = haversine(lat, lng, gb.lat, gb.lng)
        if dist <= radius:
            status = "open"
            if gb.people_joined >= gb.people_limit:
                status = "full"
            elif gb.people_joined >= gb.people_limit * 0.8:
                status = "almost_full"

            nearby.append({
                "id": gb.id,
                "title": gb.title,
                "description": gb.description,
                "price": gb.price,
                "lat": gb.lat,
                "lng": gb.lng,
                "people_joined": gb.people_joined,
                "people_limit": gb.people_limit,
                "deadline": gb.deadline,
                "distance": round(dist,2),
                "status": status
            })
    return nearby

@app.post("/join-groupbuy/{groupbuy_id}")
def join_groupbuy(groupbuy_id: int):
    for gb in groupbuys:
        if gb.id == groupbuy_id:
            if gb.people_joined < gb.people_limit:
                gb.people_joined += 1
                return {"message": "加入成功", "people_joined": gb.people_joined}
            else:
                return {"message": "團購已滿"}
    return {"message": "找不到此團購"}