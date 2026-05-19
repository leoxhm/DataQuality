from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    uuid: str
    path: str
    data_file: str
    qc_files: List[str]
    name_user: str
    name_domain: str
    name_cust: str
    bus_dt: str
    backtrack: str
    dmd3t: str
    table_nm: str
