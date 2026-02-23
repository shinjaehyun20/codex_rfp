from typing import Callable, Dict, List

from apps.api.app.services.ids import make_id

def step_ingest(envelope: Dict) -> Dict:
    payload = dict(envelope["payload"])
    payload["ingest"] = "ok"
    return {**envelope, "payload": payload}

def step_state_create(envelope: Dict) -> Dict:
    payload = dict(envelope["payload"])
    payload["state_id"] = make_id("STATE")
    return {**envelope, "payload": payload}

def get_steps() -> List[Callable[[Dict], Dict]]:
    return [step_ingest, step_state_create]
