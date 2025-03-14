from sqlalchemy.orm import Session
from ..models import ChatSession, ChatMessage
from fastapi import HTTPException


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def process_message(self, user_id: int, message: str, session_id: str = None):
        if session_id:
            session = self.db.query(ChatSession).filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            ).first()
            if not session:
                raise HTTPException(status_code=403, detail="Session not found")
        else:
            session = ChatSession(user_id=user_id)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            # 添加系统消息
            system_msg = ChatMessage(
                session_id=session.id,
                role="system",
                content="你是一个智能助手"
            )
            self.db.add(system_msg)

        # 用户消息
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=message
        )
        self.db.add(user_msg)

        # 示例回复
        ai_response = f"已收到：{message}"
        ai_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=ai_response
        )
        self.db.add(ai_msg)

        self.db.commit()
        return {
            "reply": ai_response,
            "session_id": session.id,
            "history": [
                {"role": msg.role, "content": msg.content}
                for msg in session.messages
            ]
        }