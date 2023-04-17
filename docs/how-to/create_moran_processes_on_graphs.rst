.. _moran-process-on-graphs:

Create Moran Processes On Graphs
================================

The library also provides a graph-based Moran process [Shakarian2013]_ with
:code:`MoranProcess`.  To use this feature you must supply at least one
:code:`Axelrod.graph.Graph` object, which can be initialized with just a list of
edges::

    edges = [(source_1, target1), (source2, target2), ...]

The nodes can be any hashable object (integers, strings, etc.). For example::

    >>> import axelrod as axl
    >>> from axelrod.graph import Graph
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)

Graphs are undirected by default but you can pass :code:`directed=True` to
create a directed graph. Various intermediates such as the list of neighbors
are cached for efficiency by the graph object.

A Moran process can be invoked with one or two graphs. The first graph, the
*interaction graph*, dictates how players are matched up in the scoring phase.
Each player plays a match with each neighbor. The second graph dictates how
players replace another during reproduction. When an individual is selected to
reproduce, it replaces one of its neighbors in the *reproduction graph*. If only
one graph is supplied to the process, the two graphs are assumed to be the same.

To create a graph-based Moran process, use a graph as follows::

    >>> from axelrod.graph import Graph
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)
    >>> players = [axl.Cooperator(), axl.Cooperator(), axl.Cooperator(), axl.Defector()]
    >>> mp = axl.MoranProcess(players, interaction_graph=graph, seed=40)
    >>> results = mp.play()
    >>> mp.population_distribution()
    Counter({'Defector': 4})

You can supply the :code:`reproduction_graph` as a keyword argument. The
standard Moran process is equivalent to using a complete graph with no loops
for the :code:`interaction_graph` and with loops for the
:code:`reproduction_graph`.
