from validator import Validator

class InivaValidator (Validator):
    def __init__(self, id, type, group=0, target=0, attackSteal=False, attackOmission=False, attackForce=False, attackNoVote = False, colatural=1):
        super().__init__(id, type, group, target, attackSteal, attackOmission, attackForce, attackNoVote, colatural)
        self.parent = None
        self.children = []
        self.secondChance = False

    def attack(self, block, blocks):
        if self.type == "Byzantine":
            if self.attackOmission:
                self.omitVote(block, blocks)
            if self.attackSteal:
                self.stealBonus()
            if self.attackForce:
                self.forcePunishment()
            if self.attackNoVote:
                self.noVote(block)

    def omitVote(self, block, blocks):
        if self.currentRole == "Leader":
            if len(blocks) == 1:
                return
            if blocks[-2].proposer.type == "Byzantine":
                block.signatures.remove(self.target)
                return
            if self.target.currentRole == "Member" and self.target.parent.type == "Byzantine":
                block.signatures.remove(self.target)

    def stealBonus(self):
        if self.parent == self.target and self.target.currentRole == "Aggregator":
            self.secondChance = True

    def forcePunishment(self):
        if self.currentRole == "Aggregator":
            if self.target in self.children:
                self.target.secondChance = True

    def noVote(self, block):
        if self.target.currentRole == "Leader":
            block.signatures.remove(self)
            if self.currentRole == "Aggregator":
                for child in self.children:
                    child.secondChance = True
