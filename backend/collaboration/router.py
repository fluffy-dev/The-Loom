from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status

from backend.collaboration.manager import manager
from backend.collaboration.service import CollaborationService
from backend.security.service import TokenService
from backend.user.dependencies.repository import IUserRepository

router = APIRouter(tags=["Collaboration"])


@router.websocket("/ws/{room_id}/{file_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: str,
        file_id: str,
        token: str,
        user_repo: IUserRepository
):
    """
    Handles WebSocket connections for real-time collaboration on a specific file.

    Authenticates the user via a token in the query params, connects them to the
    room, sends the initial document state, and then relays all CRDT updates
    between clients in the same room.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        room_id (str): The human-readable ID of the room.
        file_id (str): The ID of the file being edited.
        token (str): The user's JWT access token for authentication.
        user_repo (UserRepository): Dependency to fetch user data.
    """
    # 1. Аутентификация пользователя
    payload = TokenService.verify_token(token)
    if not payload or not payload.sub:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user_id = int(payload.sub)
        user = await user_repo.get(user_id)  # Проверяем, что пользователь существует
    except (ValueError, Exception):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 2. Подключение
    # Мы используем составной ID для комнаты в менеджере, чтобы различать файлы
    connection_room_id = f"{room_id}/{file_id}"
    await manager.connect(websocket, connection_room_id)

    collab_service = CollaborationService()

    # 3. Отправка начального состояния документа
    initial_state = await collab_service.get_document_state(room_id, file_id)
    if initial_state:
        # Y-Py протокол: сообщение с типом 0 означает синхронизацию/загрузку документа
        sync_message = b'\x00\x00' + initial_state
        await websocket.send_bytes(sync_message)

    try:
        # 4. Цикл приема и ретрансляции сообщений
        while True:
            data = await websocket.receive_bytes()
            # Сохраняем последнее состояние для новых подключений
            await collab_service.save_document_state(room_id, file_id, data)
            # Ретранслируем всем остальным
            await manager.broadcast(data, connection_room_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, connection_room_id)
        # Здесь можно добавить логику для обновления состояния "awareness"
        # Например, broadcast(awareness_update_message, ...)