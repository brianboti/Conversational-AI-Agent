from __future__ import annotations

from typing import Any, Dict, List, Optional
from google.cloud import firestore as gfs
from ..logging import log_event


class TranscriptRepository:
    def __init__(self) -> None:
        self._client: Optional[gfs.Client] = None

    def client(self) -> Optional[gfs.Client]:
        if self._client is None:
            try:
                self._client = gfs.Client()
                log_event("INFO", "firestore.init.ok")
            except Exception as exc:
                log_event("ERROR", "firestore.init.fail", error=str(exc))
                self._client = None
        return self._client

    def save_transcript(self, doc_id: str, document: Dict[str, Any]) -> None:
        cli = self.client()
        if not cli:
            raise RuntimeError("firestore unavailable")
        cli.collection("call_transcripts").document(doc_id).set(document, merge=True)

    def list_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        cli = self.client()
        if not cli:
            raise RuntimeError("firestore unavailable")
        snaps = (
            cli.collection("call_transcripts")
            .order_by("created_at", direction=gfs.Query.DESCENDING)
            .limit(limit)
            .stream()
        )
        items: List[Dict[str, Any]] = []
        for s in snaps:
            d = s.to_dict()
            d["id"] = s.id
            d.pop("raw", None)
            items.append(d)
        return items

    def get_one(self, doc_id: str) -> Optional[Dict[str, Any]]:
        cli = self.client()
        if not cli:
            raise RuntimeError("firestore unavailable")
        doc = cli.collection("call_transcripts").document(doc_id).get()
        if not doc.exists:
            return None
        d = doc.to_dict()
        d["id"] = doc.id
        d.pop("raw", None)
        return d
