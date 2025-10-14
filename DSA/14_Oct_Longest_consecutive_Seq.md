# 1
```
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        seen = set(nums)
        ans = 0
        for num in seen:
            if num - 1 not in seen:
                length = 1
                
                while num + length in seen:
                    length += 1

                ans = max(ans, length)

        return ans
```
# 2
```
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        nums.sort()
        current_length = 1
        max_length = 1
        
        for i in range(1, len(nums)):
            # Skip duplicates
            if nums[i] == nums[i-1]:
                continue
            # Check for consecutive sequence
            if nums[i] == nums[i-1] + 1:
                current_length += 1
                max_length = max(max_length, current_length)
            else:
                current_length = 1
        
        return max_length
