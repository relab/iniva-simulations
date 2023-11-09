import random
from block import Block

class Validator:
    def __init__(self, id, type, group=0, target=0, attackSteal=False, attackOmission=False, attackForce=False, colatural=1):
        self.id = id
        self.type = type
        self.reward = 0
        self.proposedBlocks = []
        self.target = target
        self.group = group
        self.attackSteal = attackSteal
        self.attackOmission = attackOmission
        self.attackForce = attackForce
        self.currentRole = "Member"
        self.colatural = colatural
        self.parent = None
        self.children = []
        self.secondChance = False


    def propose(self, blocks):
        r = random.randint(0, 100)
        b = Block(len(blocks), r, self)
        self.proposedBlocks.append(b)
        return b


    def sign(self, NewBlock):
        if NewBlock.isValid():
            NewBlock.signatures.append(self)

    def attack(self, fanout, block, blocks):
        if self.type == "Byzantine":
            if self.attackOmission:
                self.omitVote(fanout, block, blocks)
            if self.attackSteal:
                self.stealBonus()
            if self.attackForce:
                self.forcePunishment()

    def omitVote(self, fanout, block, blocks):
        if self.currentRole == "Leader":
            if len(blocks) == 1:
                return
            if blocks[-2].proposer.type == "Byzantine":
                block.signatures.remove(self.target)
                return
            if self.target.currentRole == "Member" and self.target.parent.type == "Byzantine":
                block.signatures.remove(self.target)

    def stealBonus(self):
        if self.currentRole == "Leader":
            if self.target.currentRole == "Aggregator":
                for child in self.target.children:
                    if child.type == "Byzantine":
                        child.secondChance = True

    def forcePunishment(self):
        if self.currentRole == "Aggregator":
            if self.target in self.children:
                self.target.secondChance = True

