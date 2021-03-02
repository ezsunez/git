class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorderTraversal(self, root: TreeNode):  # 中序 Inorder Traversal  迭代    左根右
    res = []
    nodes = []
    while root or nodes != []:
        while root:
            nodes.append(root)
            root = root.left
        root = nodes.pop()
        res.append(root.val)
        root = root.right
    return res


#######################################################################################
def a(self, node, res):  # 中序 Inorder Traversal 递归
    if not node: return
    self.a(node.left, res)
    res.append(node.val)
    self.a(node.right, res)
    return res


def inorderTraversal(self, root: TreeNode):
    res = []
    res = self.a(root, res)
    return res


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def preorderTraversal(self, root: TreeNode):  # 前序  predorder 迭代 根左右
    res = []
    lst = []
    while root or lst != []:
        while root:
            lst.append(root)
            res.append(root.val)
            root = root.left
        root = lst.pop()
        root = root.right
    return res


#######################################################################################
def a(self, node, res):  # 前序  predorder 递归
    if not node:
        return
    res.append(node.val)
    self.a(node.left, res)
    self.a(node.right, res)
    return res


def preorderTraversal(self, root: TreeNode):
    res = []
    res = self.a(root, res)
    return res


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def postorderTraversal(self, root: TreeNode):  # 后序  postdorder 递归   左右根
    res = []
    res = self.a(root, res)
    return res


def a(self, node, res):
    if not node: return
    self.a(node.left, res)
    self.a(node.right, res)
    res.append(node.val)
    return res


#######################################################################################

def postorderTraversal(self, root: TreeNode):  # 后序  postdorder 迭代
    res = []
    lst = []
    while root or lst != []:
        while root:
            res.append(root.val)
            lst.append(root)
            root = root.right
        root = lst.pop()
        root = root.left
    res.reverse()
    return res
