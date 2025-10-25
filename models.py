from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Boolean, DateTime
from sqlalchemy.sql import func

class Task(Base):

    __tablename__ = "afraa"

    id = Column(Integer,
                primary_key = True,
                index = True
                
            )
    title = Column(String,
                     nullable = False
                 )
    description = Column(String,
                           nullable = False
                       )
    priority = Column(String,
                        nullable = False
                    )
    
    completed = Column(Boolean, 
                        default = False
                    )
    created_at = Column(DateTime(timezone = True),
                            server_default = func.now()
                    )
       # created_at: DateTime column with timezone
    # server_default=func.now(): Automatically set to current time
    updated_at = Column(DateTime(timezone = True),
                            server_default = func.now(),
                            onupdate = func.now()
                    )
      # updated_at: DateTime column with timezone


# tasks table:
# ┌────┬───────────┬─────────────┬───────────┬──────────┬────────────┬────────────┐
# │ id │   title   │ description │ completed │ priority │ created_at │ updated_at │
# ├────┼───────────┼─────────────┼───────────┼──────────┼────────────┼────────────┤
# │ 1  │ Buy milk  │ From store  │   False   │  medium  │ 2024-01-01 │ 2024-01-01 │
# │ 2  │ Walk dog  │ 30 minutes  │   True    │  high    │ 2024-01-02 │ 2024-01-02 │
# └────┴───────────┴─────────────┴───────────┴──────────┴────────────┴────────────┘