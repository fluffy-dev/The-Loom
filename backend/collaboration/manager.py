from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active WebSocket connections for collaboration rooms.
    """
    def __init__(self):
        """Initializes the manager with an empty dictionary of active connections."""
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        """
        Accepts a new WebSocket connection and adds it to the room's pool.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            room_id (str): The ID of the room the user is joining.
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        """
        Removes a WebSocket connection from the room's pool.

        Args:
            websocket (WebSocket): The WebSocket connection instance to remove.
            room_id (str): The ID of the room the user is leaving.
        """
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: bytes, room_id: str, sender: WebSocket):
        """
        Broadcasts a message to all clients in a room except the sender.

        Args:
            message (bytes): The message to broadcast (expects binary data).
            room_id (str): The ID of the room to broadcast to.
            sender (WebSocket): The WebSocket connection of the message sender.
        """
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection is not sender:
                    await connection.send_bytes(message)

# Создаем один экземпляр менеджера, который будет использоваться всем приложением (Singleton)
manager = ConnectionManager()