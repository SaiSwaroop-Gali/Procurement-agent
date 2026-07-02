from dataclasses import dataclass
import uuid


@dataclass
class ProcurementRequest:

    part_id: str
    part_name: str

    current_stock: int
    recommended_order: int

    supplier_name: str
    supplier_email: str

    ai_analysis: str

    risk_level: str = "MEDIUM"

    manager_instructions: str = ""

    status: str = "PENDING_APPROVAL"

    request_id: str = ""

    def __post_init__(self):

        if not self.request_id:

            self.request_id = str(uuid.uuid4())[:8]