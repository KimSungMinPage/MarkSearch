from collections import defaultdict
from typing import Iterable, Any
def mark_duplicates(items: Iterable[Any]) -> None:
    groups: dict[tuple, list[Any]] = defaultdict(list)
    for item in items: groups[item.duplicate_key()].append(item)
    group_no = 1
    for rows in groups.values():
        if len(rows) > 1:
            for row in rows:
                row.is_duplicate = True; row.duplicate_group_no = group_no
            group_no += 1
