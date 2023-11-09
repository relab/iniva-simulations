from committee import Committee
from validator import Validator

if __name__ == '__main__':
    totalRounds = 100000
    omittedBlocks = []

    ms = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    #ms = [0.30]
    mCounts = [int(i * 111) for i in ms]
    print(mCounts)

    rewardss = [[], [], []]
    for mCount in mCounts:

        users = []
        for i in range(0, 110 - mCount):
            users.append(Validator(len(users), "Correct", 1, 0))
        victim = Validator(len(users), "Correct", 2, 0)
        users.append(victim)
        for i in range(0, mCount):
            users.append(Validator(len(users), "Byzantine", 3, victim, True, True, True, 0))

        committee = Committee(111, users, 10, 1)
        for i in range(0, totalRounds):
            print(str(mCount) + " " + str(i))
            isProduced = committee.round(i)

        total = [0, 0, 0]
        nums = [110 - mCount, 1, mCount]
        for k in range(1, 4):
            for j in range(0, len(users)):
                if users[j].group == k:
                    total[k - 1] += users[j].reward
        rewards = [total[j] / sum(total) for j in range(len(total))]
        rewards = [rewards[j] / nums[j] for j in range(len(rewards))]
        temp = 1 / 111
        # rewards = [(x * 0.01) /temp for x in rewards]
        rewards = [(x - temp) for x in rewards]
        rewards = [rewards[j] / temp for j in range(len(rewards))]
        for k in range(1, 4):
            rewardss[k - 1].append(rewards[k - 1])
        print(rewards)
    print(rewardss)