class Solution:

    def findOrigin(self, charge: list[int],
                   cost: list[int]) -> int:
        sz = len(charge)
        overall_net = 0
        current_run = 0
        possible_ans = 0
        for pos in range(sz):
            step_diff = charge[pos] - cost[pos]
            overall_net = overall_net + step_diff
            current_run = current_run + step_diff
            if 0 > current_run:
                possible_ans = pos + 1
                current_run = 0
        if overall_net < 0:
            return -1
        return possible_ans