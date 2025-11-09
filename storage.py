"""Minimal filesystem-backed storage for the template.

This is intentionally tiny: it stores JSON content nodes under the
`MCP_SNIPPETS_ROOT` (default `/data`) and provides a couple of helper
functions used by the template tools. It's provided so the template can
be run inside Docker with a mounted volume and persist state by default.
"""
from __future__ import annotations
import json
import os
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

ROOT = Path(os.environ.get("MCP_SNIPPETS_ROOT", "/data"))
NODE_DIR = ROOT / "nodes" / "content"
EDGE_DIR = ROOT / "edges"

for p in [NODE_DIR, EDGE_DIR]:
    p.mkdir(parents=True, exist_ok=True)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def add_content(content: str, title: Optional[str] = None, date: Optional[str] = None, style: Optional[List[str]] = None, tags: Optional[List[str]] = None, authors: Optional[List[str]] = None) -> str:
    cid = str(uuid.uuid4())
    node = {
        "id": cid,
        "type": "content",
        "title": title,
        "date": date or _iso_now(),
        "style": style or [],
        "tags": tags or [],
        "authors": authors or [],
        "content": content,
    }
    path = NODE_DIR / f"{cid}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(node, f, ensure_ascii=False, indent=2)
    return cid


def get_node(node_id: str) -> Dict[str, Any]:
    p = NODE_DIR / f"{node_id}.json"
    if not p.exists():
        raise FileNotFoundError(node_id)
    return json.loads(p.read_text(encoding="utf-8"))


def get_all_content_count() -> int:
    try:
        return len(list(NODE_DIR.glob("*.json")))
    except Exception:
        return 0


def iter_content_nodes():
    for p in NODE_DIR.glob("*.json"):
        try:
            yield json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
