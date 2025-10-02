class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        i = 0
        n = len(nums)
        while i < n - 1:
            if nums[i] != nums[i+1]:
                return nums[i]
            i += 2
        return nums[-1]
