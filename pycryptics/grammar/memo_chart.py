from nltk.parse.earleychart import IncrementalChart
from nltk.parse.chart import LeafEdge, Tree

class MemoChart(IncrementalChart):
    def parses(self, root, tree_class=Tree):
        """
        Return a list of the complete tree structures that span
        the entire chart, and whose root node is ``root``.
        """
        trees = []
        self.memo = {}
        for edge in self.select(start=0, end=self._num_leaves, lhs=root):
            trees += self.trees(edge, tree_class=tree_class, complete=True)
        return trees

    def trees(self, edge, tree_class=Tree, complete=False):
        """
        Return a list of the tree structures that are associated
        with ``edge``.

        If ``edge`` is incomplete, then the unexpanded children will be
        encoded as childless subtrees, whose node value is the
        corresponding terminal or nonterminal.

        :rtype: list(Tree)
        :note: If two trees share a common subtree, then the same
            Tree may be used to encode that subtree in
            both trees.  If you need to eliminate this subtree
            sharing, then create a deep copy of each tree.
        """
        return self._trees(edge, complete, tree_class=tree_class)

    def _trees(self, edge, complete, tree_class):
        """
        A helper function for ``trees``.

        :param memo: A dictionary used to record the trees that we've
            generated for each edge, so that when we see an edge more
            than once, we can reuse the same trees.
        """
        # If we've seen this edge before, then reuse our old answer.
        print "edge:", edge
        print "memo:", self.memo
        # import pdb; pdb.set_trace()
        if edge in self.memo:
            print "cache hit for edge:", edge
            return self.memo[edge]

        trees = []

        # when we're reading trees off the chart, don't use incomplete edges
        if complete and edge.is_incomplete():
            return trees

        # Until we're done computing the trees for edge, set
        # memo[edge] to be empty.  This has the effect of filtering
        # out any cyclic trees (i.e., trees that contain themselves as
        # descendants), because if we reach this edge via a cycle,
        # then it will appear that the edge doesn't generate any
        # trees.
        self.memo[edge] = []

        # Leaf edges.
        if isinstance(edge, LeafEdge):
            leaf = self._tokens[edge.start()]
            self.memo[edge] = leaf
            return [leaf]

        # Each child pointer list can be used to form trees.
        for cpl in self.child_pointer_lists(edge):
            # Get the set of child choices for each child pointer.
            # child_choices[i] is the set of choices for the tree's
            # ith child.
            child_choices = [self._trees(cp, complete, tree_class)
                             for cp in cpl]

            # For each combination of children, add a tree.
            for children in self._choose_children(child_choices):
                lhs = edge.lhs().symbol()
                trees.append(tree_class(lhs, children))

        # If the edge is incomplete, then extend it with "partial trees":
        if edge.is_incomplete():
            unexpanded = [tree_class(elt,[])
                          for elt in edge.rhs()[edge.dot():]]
            for tree in trees:
                tree.extend(unexpanded)

        # Update the memoization dictionary.
        self.memo[edge] = trees

        # Return the list of trees.
        print "returning trees:", trees
        return trees