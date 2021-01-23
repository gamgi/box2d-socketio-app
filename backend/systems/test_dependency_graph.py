from ecs.base_system import System
import systems.dependency_graph as graph


class FooSystem(System):
    requires = []  # type:ignore


class BarSystem(System):
    requires = []  # type:ignore


class BazSystem(System):
    requires = [FooSystem]


class BaySystem(System):
    requires = [FooSystem]


class BakSystem(System):
    requires = [BaySystem, BazSystem]


class BaxSystem(System):
    pass


class TestDependencyGraph:
    def test_build_graph(self):
        result = graph._build_graph([
            FooSystem, BaySystem, BazSystem, BarSystem, BakSystem, BaxSystem  # type:ignore
        ])

        assert result == {
            FooSystem: [],
            BarSystem: [],
            BaxSystem: [],
            BazSystem: [FooSystem],
            BaySystem: [FooSystem],
            BakSystem: [BaySystem, BazSystem],
        }

    def test_resolve_dependency_order(self):
        order = graph.resolve_dependency_order([
            FooSystem, BaySystem, BazSystem, BarSystem, BakSystem, BaxSystem  # type:ignore
        ])

        assert order == [
            FooSystem,
            BarSystem,
            BaxSystem,
            BaySystem,
            BazSystem,
            BakSystem,
        ]

        order = graph.resolve_dependency_order([
            FooSystem, BarSystem, BazSystem, BaySystem, BakSystem, BaxSystem  # type:ignore
        ])

        assert order == [
            FooSystem,
            BarSystem,
            BaxSystem,
            BazSystem,
            BaySystem,
            BakSystem,
        ]
