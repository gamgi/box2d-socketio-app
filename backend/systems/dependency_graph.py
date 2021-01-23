from typing import List, Dict, Type
from ecs.base_system import System
from collections import defaultdict
from itertools import cycle

MAX_RESOLVE_ATTEMPTS = 50


def resolve_dependency_order(systems: List[Type[System]]):
    graph = _build_graph(systems)
    left = sorted(graph, key=lambda key: len(graph[key]))
    values = cycle(left.copy())

    order: List[Type[System]] = []
    for step in range(MAX_RESOLVE_ATTEMPTS):
        if left:
            system = next(values)
            if system not in left:
                continue
        else:
            break

        requires: List[System] = getattr(system, 'requires', [])  # type:ignore
        if all(sys in order for sys in requires):
            order.append(system)
            left.remove(system)
    else:
        raise RuntimeError('Could not resolve system order')

    return order


def _build_graph(systems: List[Type[System]]) -> Dict[Type[System], List[Type[System]]]:
    graph: Dict = defaultdict(list)
    for system in systems:
        if hasattr(system, 'requires'):
            graph[system] += system.requires  # type: ignore
        else:
            graph[system] = []  # type: ignore
    return dict(graph)
