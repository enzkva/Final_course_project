# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import List, Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    channel = Column(String)

    def __init__(self, user_id: int, channel: str) -> None:
        self.user_id = user_id
        self.channel = channel


Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def check_exist(user: int, channel: Optional[str] = None):
    with session_scope() as session:
        if channel:
            return [
                now.channel
                for now in session.query(User)
                .filter_by(user_id=user, channel=channel)
                .all()
            ]
        return [
            now.channel for now in session.query(User).filter_by(user_id=user).all()
        ]


def add_channel(user: int, channel: str) -> str:
    with session_scope() as session:
        if check_exist(user, channel):
            return "The channel already exists in channel list."
        new_user = User(user_id=user, channel=f"{channel}")
        session.add(new_user)
        session.commit()
        return "The channel has been added."


def delete_channel(user: int, channel: str) -> str:
    with session_scope() as session:
        if not check_exist(user, channel):
            return "The channel does not exist in channel list."
        session.query(User).filter_by(user_id=user, channel=channel).delete()
        session.commit()
        return (
            "Channel is deleted from channel list!\nYou can write next name of channel."
        )
