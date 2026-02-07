##This is the important file of the project
# What the file is??
##It is a schema, a contact, a shared language between nodes

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from datetime import datetime


class Metadata(TypedDict):
    session_id: str   #sesion id : Session which we are running
    timestamps : Dict[str, str] ##Time stamps in which we are running that session

class MemoryState(TypedDict):
   ##raw user input

    user_input: str
   #memories retrieved from storage
    retrieved_memories : List[Dict[str,Any]]
    ##Conversational summary(used for memory write-back)
    summary : Optional[str]
    metadata : Metadata