import random
from validator import Validator


class Committee:
    def __init__(self, size, users, fanout, colatural=1):
        self.committeeSize = size
        self.validators = users
        self.blocks = []
        self.omittedBlocks = 0
        self.fanout = fanout
        self.colatural = colatural
        self.leaderBonus = 0.15
        self.aggregationBonus = 0.0002
        self.blockReward = 10000

    def shuffleTree(self):
        random.shuffle(self.validators)
        self.proposer = self.validators[0]
        for v in self.validators:
            v.currentRole = "Member"
            v.secondChance = False
            v.children = []
        self.validators[0].currentRole = "Leader"
        self.validators[0].parent = None
        for i in range(1, self.fanout + 1):
            self.validators[i].currentRole = "Aggregator"
            self.validators[i].parent = self.validators[0]
            for j in range((self.fanout * i) + 1, (self.fanout * i) + self.fanout + 1):
                self.validators[j].parent = self.validators[i]
                self.validators[i].children.append(self.validators[j])

    def distributeRewards(self, newBlock):
        for v in newBlock.signatures:
            v.attack(self.fanout, newBlock, self.blocks)
        count = len(newBlock.signatures)
        maxfault = int(self.committeeSize / 3)
        threshold = self.committeeSize - maxfault
        leaderBonus = ((count - threshold) / maxfault) * self.leaderBonus * self.blockReward
        fullLeaderBonus = self.leaderBonus * self.blockReward
        aggregationBonus = 0
        fullAggregationBonus = 0
        for i in range(len(self.validators)):
            v = self.validators[i]
            if v.currentRole == "Aggregator" and v in newBlock.signatures:
                for j in range((self.fanout * i) + 1, (self.fanout * i) + self.fanout + 1):
                    v2 = self.validators[j]
                    fullAggregationBonus += self.aggregationBonus * self.blockReward
                    if v2 in newBlock.signatures and not v2.secondChance:
                        aggregationBonus += self.aggregationBonus * self.blockReward
                        v.reward += self.aggregationBonus * self.blockReward
            if v.currentRole == "Leader":
                v.reward += leaderBonus
        votingReward = self.blockReward - fullLeaderBonus - fullAggregationBonus
        punishments = 0
        for v in newBlock.signatures:
            if v.secondChance:
                v.reward += ((votingReward / len(newBlock.signatures)) - (self.aggregationBonus * self.blockReward))
                punishments += (self.aggregationBonus * self.blockReward)
            else:
                v.reward += votingReward / len(newBlock.signatures)
        divisable = (fullLeaderBonus - leaderBonus) + (fullAggregationBonus - aggregationBonus) + punishments
        for v in self.validators:
            v.reward += divisable / len(self.validators)

    def round(self, roundNumber):
        self.shuffleTree()
        newBlock = self.proposer.propose(self.blocks)
        # print(self.proposer.__dict__)
        total = 0
        for v in self.validators:
            v.sign(newBlock)
        if newBlock.isConfirmed(self.committeeSize):
            self.blocks.append(newBlock)
            self.distributeRewards(newBlock)
            return True
        else:
            print("Invalid")
            return False