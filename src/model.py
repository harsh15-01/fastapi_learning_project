from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey, LargeBinary, text, Integer, Boolean, func
from src.database import Base
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, TIMESTAMP


class BrandSettings(Base):
    __tablename__ = 'brand_settings'

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, index=True)
    settings_json = Column(Text, nullable=False)
    inactive_settings = Column(Boolean, default=False)
    created_by = Column(Integer, index=True)
    created_time = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')


class Story(Base):
    __tablename__ = 'story'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    summary = Column(Text)
    guide_id = Column(Integer, ForeignKey('video.id', ondelete='SET NULL', onupdate='CASCADE'))
    owner_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    categoryID = Column(Integer, nullable=True)
    inactive = Column(Boolean, nullable=False, default=False)
    created_time = Column(DateTime, nullable=True)
    background = Column(Text)
    description = Column(Text)
    isPrivate = Column(Boolean, nullable=False, default=True)
    story_type = Column(Integer, default=1, comment='1 = Video, 2 = ScreenShare, 3 = Audio, 4 = Chat')
    approvalpreferred = Column(Boolean, default=False)
    purpose = Column(String(255), nullable=True)
    timing = Column(String(255), nullable=True)
    distribution = Column(String(255), nullable=True)
    promotedToTeam = Column(Boolean, default=False)
    recording = Column(Boolean, nullable=False, default=False, comment='0 = Standard, 1 = Interactive')
    difficulty = Column(Integer, nullable=False, default=0,
                        comment='0 = General, 1= Low/Easy, 2= Medium, 3 = Hard/High')
    interactive_pattern = Column(Integer, nullable=False, default=2, comment='0 = General, 1 = Inbound, 2 = Outbound')
    interactive_format = Column(Integer, default=1, comment='1 = Guided, 2 = Unguided')
    compliance = Column(Boolean, nullable=False, default=False, comment='0-No , 1- Yes')
    ai_version = Column(Integer, nullable=True)
    rule_engine = Column(String(255), default='1.0', comment='Default is 1.0 and new is 1.1')
    coaching = Column(String(255), default='1.0', comment='Default is 1.0')
    user_workbench_version = Column(String(10), nullable=False, default='v1',
                                    comment='Specifies version of user workbench enabled for this story')


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    inactive = Column(Boolean, default=False, nullable=False)
    created_by = Column(Integer, default=0)
    created_time = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_by = Column(Integer, default=0)
    last_updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True
    )
