# 1
```
from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Removes all occurrences of val in nums in-place and returns the new length.
        Uses two-pointers with swapping from the end.
        """
        left = 0
        right = len(nums) - 1

        while left <= right:
            if nums[left] == val:
                # Swap with the rightmost element (could also be val)
                nums[left] = nums[right]
                right -= 1
                # Don't increment left, need to check the swapped element
            else:
                left += 1
        
        # left points to the new length of array excluding 'val'
        return left
```
