from print_pp.logging import Print

# this is local class for documentation purposes
# this class will look like the class on user.models -> UserInteraction
class UserInteraction:
    
    def __init__(self, score:int, next_node:'UserInteraction'=None):
        self.score = score
        self.next_node = next_node


class UserInteractionBinaryTree:

    """

        For this binary tree we'll have a maximum of 30 nodes, since the maximum score for each user interaction is 30.

        max_nodes = 30
        max_user_interactions for each node = 200
    
    """


    def __init__(self, user_interaction:UserInteraction, root:'UserInteractionBinaryTree'=None):
        
        # this is the number of nodes in the tree
        # this property should only be updated on the root of the tree
        self.num_nodes:int = 1

        self.user_interactions:list[UserInteraction] = [user_interaction]
        self.score:int = user_interaction.score
        
        self.root:UserInteractionBinaryTree = self if root is None else root
        self.left:UserInteractionBinaryTree = None
        self.right:UserInteractionBinaryTree = None
    

    def insert(self, user_interaction):
        self._insert(self.root, user_interaction)
        self.root.num_nodes += 1


    def _insert(self, current:'UserInteractionBinaryTree', user_interaction:UserInteraction):
        if user_interaction.score > current.score:
            if current.right is None:
                current.right = UserInteractionBinaryTree(user_interaction, root=self.root)
            else:
                self._insert(current.right, user_interaction)
        elif user_interaction.score < current.score:
            if current.left is None:
                current.left = UserInteractionBinaryTree(user_interaction, root=self.root)
            else:
                self._insert(current.left, user_interaction)
        else:
            current.user_interactions.append(user_interaction)


    def find(self, score:int) -> 'UserInteractionBinaryTree':
        if self.root is not None:
            return self._find(self.root, score)
        else:
            return None


    def _find(self, current:'UserInteractionBinaryTree', score:int) -> 'UserInteractionBinaryTree':
        if current.score == score:
            return current
        elif current.score < score and current.right is not None:
            return self._find(current.right, score)
        elif current.score > score and current.left is not None:
            return self._find(current.left, score)


    def delete(self, score:int):
        # why self root?
        self.root = self._delete(self.root, score)
        self.root.num_nodes -= 1


    def _delete(self, current:'UserInteractionBinaryTree', score:int):
        if current is None:
            return current

        if score < current.score:
            current.left = self._delete(current.left, score)
        
        elif score > current.score:
            current.right = self._delete(current.right, score)
        
        else:
            if current.left is None and current.right is None:
                current = None
            elif current.left is None:
                current = current.right
            elif current.right is None:
                current = current.left
            else:
                temp:UserInteractionBinaryTree = self._find_min(current.right)
                current.score = temp.score
                current.right = self._delete(current.right, temp.score)
        
        return current


    def _find_min(self, current:'UserInteractionBinaryTree') -> 'UserInteractionBinaryTree':
        if current.left is None:
            return current
        else:
            return self._find_min(current.left)


    # create a generator that yield the values from max to min
    def get_values(self, direction:str='max') -> 'UserInteractionBinaryTree':
        if direction == 'max':
            highest_score = self.root.num_nodes
            while highest_score >= 0:
                node = self.find(highest_score)
                if node is not None:
                    yield node
                highest_score -= 1
        else:
            lowest_score = 0
            while lowest_score <= self.root.num_nodes:
                node = self.find(lowest_score)
                if node is not None:
                    yield node
                lowest_score += 1

        yield None
        
    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)
        Print('num_nodes', self.root.num_nodes)


    def _print_tree(self, current:'UserInteractionBinaryTree'):
        if current is not None:
            self._print_tree(current.left)
            Print(('score', 'num_interactions'), (current.score, len(current.user_interactions)), bl=False)
            self._print_tree(current.right)
    

    def __str__(self) -> str:
        return f'score: {self.score} - num_interactions: {len(self.user_interactions)}'


def create_binary_tree(user_interaction:UserInteraction, return_highest_score:bool=False) -> UserInteractionBinaryTree:
    
    head = user_interaction
    current_score = 0
    linked_list_len = 0
    average_score = 0

    while user_interaction is not None:
        linked_list_len += 1
        current_score += user_interaction.score
        user_interaction = user_interaction.next_node

    average_score = current_score / linked_list_len

    # get the node that is closest to the average score
    # and create a binary tree with that node as the root
    user_interaction = head
    closest_operation = None
    closest_node = None

    while user_interaction is not None:
        if user_interaction.score == average_score:
            closest_node = user_interaction
            break
            
        operation = user_interaction.score - average_score
        if closest_operation is None or abs(operation) < abs(closest_operation):
            closest_operation = operation
            closest_node = user_interaction
    
        user_interaction = user_interaction.next_node

    
    # create a binary tree with the closest node as the root
    root = UserInteractionBinaryTree(closest_node)
        
    # insert the rest of the nodes in the binary tree
    user_interaction = head
    while user_interaction is not None:
        if user_interaction is not closest_node:
            root.insert(user_interaction)
        user_interaction = user_interaction.next_node


    return root


