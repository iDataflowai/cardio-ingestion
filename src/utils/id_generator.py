import uuid
from uuid import uuid4


def trace_id_generator():
    return f"trace_{uuid.uuid4()}"

