"""WebSocket manager for real-time updates"""
from typing import Dict, Set
from fastapi import WebSocket
import json


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        # Store active connections by type
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "global": set(),
            "donations": set(),
            "campaigns": set(),
            "organizations": set(),
        }

    async def connect(self, websocket: WebSocket, connection_type: str = "global"):
        """Accept new WebSocket connection"""
        await websocket.accept()
        if connection_type not in self.active_connections:
            self.active_connections[connection_type] = set()
        self.active_connections[connection_type].add(websocket)

    def disconnect(self, websocket: WebSocket, connection_type: str = "global"):
        """Remove WebSocket connection"""
        if connection_type in self.active_connections:
            self.active_connections[connection_type].discard(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client"""
        await websocket.send_text(message)

    async def broadcast(self, message: dict, connection_type: str = "global"):
        """Broadcast message to all connected clients of a type"""
        if connection_type not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[connection_type]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections[connection_type].discard(connection)

    async def broadcast_donation_update(self, donation_data: dict):
        """Broadcast new donation to all connected clients"""
        message = {
            "type": "donation_created",
            "data": donation_data
        }
        await self.broadcast(message, "donations")
        await self.broadcast(message, "global")

    async def broadcast_campaign_update(self, campaign_data: dict):
        """Broadcast campaign update"""
        message = {
            "type": "campaign_updated",
            "data": campaign_data
        }
        await self.broadcast(message, "campaigns")
        await self.broadcast(message, "global")

    async def broadcast_milestone(self, milestone_data: dict):
        """Broadcast milestone achievement"""
        message = {
            "type": "milestone_achieved",
            "data": milestone_data
        }
        await self.broadcast(message, "global")

    def get_connection_count(self, connection_type: str = "global") -> int:
        """Get number of active connections"""
        return len(self.active_connections.get(connection_type, set()))


# Global connection manager instance
manager = ConnectionManager()
