from typing import List, Optional, Any, Callable


def mergesort(data: list, key_func: Callable, reverse: bool = False) -> list:
    if len(data) <= 1:
        return data
    mid   = len(data) // 2
    left  = mergesort(data[:mid],  key_func, reverse)
    right = mergesort(data[mid:],  key_func, reverse)
    return _merge(left, right, key_func, reverse)


def _merge(left: list, right: list, key_func: Callable, reverse: bool) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        lv, rv = key_func(left[i]), key_func(right[j])
        if (lv >= rv) if reverse else (lv <= rv):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


class _BSTNode:
    __slots__ = ('key', 'records', 'left', 'right')

    def __init__(self, key: str, record):
        self.key     = key
        self.records = [record]
        self.left    = None
        self.right   = None


class OptimalBST:

    def __init__(self):
        self._root: Optional[_BSTNode] = None

    def build(self, records: list, key_attr: str) -> None:
        keyed = [(str(getattr(r, key_attr) or '').upper(), i, r)
                 for i, r in enumerate(records)]
        keyed.sort(key=lambda t: (t[0], t[1]))
        self._root = self._build(keyed, 0, len(keyed) - 1)

    def _build(self, pairs: list, lo: int, hi: int) -> Optional[_BSTNode]:
        if lo > hi:
            return None
        mid        = (lo + hi) // 2
        key, _, rec = pairs[mid]
        node       = _BSTNode(key, rec)
        node.left  = self._build(pairs, lo,     mid - 1)
        node.right = self._build(pairs, mid + 1, hi)
        return node

    def search_exact(self, query: str) -> list:
        results = []
        self._search_exact(self._root, query.upper(), results)
        return results

    def _search_exact(self, node: Optional[_BSTNode], q: str, out: list) -> None:
        if node is None:
            return
        if q == node.key:
            out.extend(node.records)
        elif q < node.key:
            self._search_exact(node.left,  q, out)
        else:
            self._search_exact(node.right, q, out)

    def search_prefix(self, prefix: str) -> list:
        results = []
        self._search_prefix(self._root, prefix.upper(), results)
        return results

    def _search_prefix(self, node: Optional[_BSTNode], p: str, out: list) -> None:
        if node is None:
            return
        if node.key.startswith(p):
            out.extend(node.records)
            self._search_prefix(node.left,  p, out)
            self._search_prefix(node.right, p, out)
        elif p < node.key:
            self._search_prefix(node.left,  p, out)
        else:
            self._search_prefix(node.right, p, out)

    def inorder(self) -> list:
        out = []
        self._inorder(self._root, out)
        return out

    def _inorder(self, node: Optional[_BSTNode], out: list) -> None:
        if node is None:
            return
        self._inorder(node.left,  out)
        out.extend(node.records)
        self._inorder(node.right, out)


def binary_search_name(sorted_parts: list, query: str) -> list:
    if not query:
        return sorted_parts

    q_upper = query.upper()
    n       = len(sorted_parts)
    lo, hi  = 0, n - 1
    first   = n

    while lo <= hi:
        mid  = (lo + hi) // 2
        name = (sorted_parts[mid].part_name or '').upper()
        if name >= q_upper:
            first = mid
            hi    = mid - 1
        else:
            lo = mid + 1

    results = []
    for i in range(first, n):
        name = (sorted_parts[i].part_name or '').upper()
        if not name.startswith(q_upper):
            break
        results.append(sorted_parts[i])

    if results:
        return results

    return [p for p in sorted_parts if q_upper in (p.part_name or '').upper()]