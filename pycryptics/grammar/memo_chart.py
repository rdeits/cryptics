from __future__ import division
from nltk.parse.earleychart import IncrementalChart
from nltk.parse.chart import LeafEdge, Tree

class ClueTree(Tree):
    def __init__(self, node_or_str, children=None):
        self.answers = None
        super(ClueTree, self).__init__(node_or_str, children)

    def __str__(self):
        return self._pprint_flat('', '()', False)

    def __repr__(self):
        return self.__str__()

    def derivations(self, answer):
        if self.node.endswith('_arg'):
            return self[0].derivations(self.answers[answer][0])
        result = "(" + self.node + " "
        arg_answers = self.answers[answer]
        for i, child in enumerate(self):
            if isinstance(child, basestring):
                result += '"' + child + '"'
            else:
                result += child.derivations(arg_answers[i])
            if i < len(self) - 1:
                result += " "
        if answer != "" and not any(answer == a for a in arg_answers):
            result += " -> " + answer.upper()
        result += ")"
        return result

    def long_derivation(self, answer, score=None):
        result = ""
        arg_answers = self.answers[answer]
        if len(self) == 0:
            return result
        if len(self) == 1 and answer == arg_answers[0]:
            if isinstance(self[0], ClueTree):
                return self[0].long_derivation(arg_answers[0])
            else:
                return ""
        indicator = None
        for i, child in enumerate(self):
            if isinstance(child, basestring):
                continue
            if child.node.endswith('_'):
                indicator = child[0]
            else:
                result += child.long_derivation(arg_answers[i])
        if self.node != 'top':
            result += '\n'

        if indicator is not None:
            result += "'" + indicator + "' means to "
        non_empty_args = ["'" + a + "'" for a in arg_answers if a != ""]
        if self.node == 'rev':
            result += "reverse " + non_empty_args[0]
        elif self.node == 'sub':
            result += "take a substring of " + non_empty_args[0]
        elif self.node == 'ins':
            result += "insert " + non_empty_args[0] + " and " + non_empty_args[1]
        elif self.node == 'ana':
            result += "anagram " + non_empty_args[0]
        elif self.node == 'syn':
            result += "Take a synonym of " + non_empty_args[0]
        elif self.node == 'first':
            result += "Take the first letter of " + non_empty_args[0]
        elif self.node == 'null':
            result += non_empty_args[0] + " is a filler word."
        elif self.node == 'd':
            result += non_empty_args[0] + " is the definition."
        elif self.node == 'top' and len(non_empty_args) > 1:
            result += "\nCombine " + comma_list(non_empty_args)

        if answer != "" and (self.node != 'top' or len(non_empty_args) > 1):
            result += " to get " + answer.upper() + "."

        if self.node == 'top' and score is not None:
            result += "\n" + answer.upper() + " matches "
            for child in self:
                if child.node == 'd':
                    result += "'" + child[0] + "'"
                    break
            result += " with confidence score {:.0%}.".format(score)
        return result

def comma_list(args):
    result = ""
    for i, a in enumerate(args):
        result += a
        if i < len(args) - 1 and len(args) > 2:
            result += ","
        if i == len(args) - 2:
            result += " and "
        else:
            result += " "
    return result

if __name__ == '__main__':
    print comma_list(['foo'])
    print comma_list(['foo', 'bar'])
    print comma_list(['foo', 'bar', 'baz'])
    print comma_list(['foo', 'bar', 'baz', 'bap'])

class MemoChart(IncrementalChart):
    def parses(self, root, tree_class=Tree):
        """
        Return a list of the complete tree structures that span
        the entire chart, and whose root node is ``root``.
        """
        trees = []
        self.memo = {}
        for edge in self.select(start=0, end=self._num_leaves, lhs=root):
            trees += self.trees(edge, tree_class=ClueTree, complete=True)
        return trees

    def trees(self, edge, tree_class=ClueTree, complete=False):
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
        # print "edge:", edge
        # print "memo:", self.memo
        # import pdb; pdb.set_trace()
        if edge in self.memo:
            # print "cache hit for edge:", edge
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
        # print "returning trees:", trees
        return trees