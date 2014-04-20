class ChipStack(object):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return "%d" % self.amount

    def emit(self, stack, amount):
        stack.absorb(self, amount)

    def absorb(self, stack, amount):
        if amount <= stack.amount:
            amount_to_absorb = amount
        else:
            amount_to_absorb = stack.amount

        self.amount += amount_to_absorb
        stack.amount -= amount_to_absorb

        return amount_to_absorb

    def absorb_entire_stack(self, stack):
        self.absorb(stack, stack.amount)
