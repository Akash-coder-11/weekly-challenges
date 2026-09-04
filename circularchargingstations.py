class Solution:

    def findOrigin(self, charge: list[int],
                   cost: list[int]) -> int:
        sz = len(charge)
        overallnet = 0
        currentrun = 0
        possibleans = 0
        for pos in range(sz):
            step_diff = charge[pos] - cost[pos]
            overallnet = overallnet + step_diff
            currentrun = currentrun + step_diff
            if 0 > currentrun:
                possibleans = pos + 1
                currentrun = 0
        if overallnet < 0:
            return -1
        return possibleans