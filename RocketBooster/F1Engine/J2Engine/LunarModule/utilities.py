# Code for pageTree, pageNode, and sanitizeId function originated from
# Brett Alistair Kromkamp - brettkromkamp@gmail.com
# www.quesucede.com
# Code has been modified. Class, variable, and function names have been
# changed from Brett's original code. Data types have been changed and
# new data members and corresponding methods [will be] added to code.
# Tree structure is kept from original code. [might be changed, but doubt it.]

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

def sanitizeId(id):
    return id.strip().replace(" ", "")

