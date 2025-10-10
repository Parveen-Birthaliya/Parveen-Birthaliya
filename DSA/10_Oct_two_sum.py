# Day Oct 10 2025
# 1 
# 
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
  
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i


# 2 
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Using a hash map to store numbers and their indices.
        # This allows for O(1) average time lookup.
        num_map = {}  # Maps: value -> index

        for i, num in enumerate(nums):
            complement = target - num
            
            # Check if the complement needed to reach the target is already in our map.
            if complement in num_map:
                # If found, we have our two numbers.
                # num_map[complement] is the index of the first number,
                # and i is the index of the current number.
                return [num_map[complement], i]
            
            # If the complement is not found, add the current number and its index to the map.
            # This makes it available as a potential complement for subsequent numbers.
            num_map[num] = i
        
        # According to the problem constraints ("Only one valid answer exists."),
        # this part should not be reachable.
        return []


# 3
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Returns two indices such that nums[i] + nums[j] == target.
        Works for both sorted and unsorted input arrays.
        Uses hashmap (O(n)) if unsorted, or two-pointer (O(n)) if sorted.
        """
        n = len(nums)
        if n < 2:
            raise ValueError("Need at least two numbers")

        # Check if the list is sorted (non-decreasing)
        is_sorted = all(nums[i] <= nums[i+1] for i in range(n-1))
        
        if is_sorted:
            # 🔹 Two-pointer method for sorted arrays
            left, right = 0, n - 1
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    return [left, right]
                elif s < target:
                    left += 1
                else:
                    right -= 1
            raise ValueError("No two sum solution")

        else:
            # 🔹 Hashmap method for unsorted arrays
            seen = {}  # num -> index
            for i, num in enumerate(nums):
                complement = target - num
                if complement in seen:
                    return [seen[complement], i]
                seen[num] = i

            raise ValueError("No two sum solution")
