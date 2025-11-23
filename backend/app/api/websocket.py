"""WebSocket endpoints for real-time updates"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.websocket import manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Global WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, "global")
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back for now (can add custom handling)
            await manager.send_personal_message(f"Message received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "global")


@router.websocket("/ws/donations")
async def donations_websocket(websocket: WebSocket):
    """WebSocket endpoint for donation updates"""
    await manager.connect(websocket, "donations")
    try:
        while True:
            data = await websocket.receive_text()
            # Keep alive
            await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, "donations")


@router.websocket("/ws/campaigns/{campaign_id}")
async def campaign_websocket(websocket: WebSocket, campaign_id: int):
    """WebSocket endpoint for specific campaign updates"""
    connection_type = f"campaign_{campaign_id}"
    await manager.connect(websocket, connection_type)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, connection_type)


@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "global_connections": manager.get_connection_count("global"),
        "donation_connections": manager.get_connection_count("donations"),
        "campaign_connections": manager.get_connection_count("campaigns"),
    }
