```
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        nums.sort()
        return nums
```


```

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums
        
        mid = len(nums) // 2

        left_sorted = self.sortArray(nums[:mid])
        right_sorted = self.sortArray(nums[mid:])

        merge_sorted = []

        i, j = 0, 0 

        while i < len(left_sorted) or j < len(right_sorted):

            if i < len(left_sorted) and j < len(right_sorted):
                val1 = left_sorted[i]
                val2 = right_sorted[j]
            elif i < len(left_sorted):
                val1  = left_sorted[i]
                val2 = float("inf")
            else:
                val1  = float("inf")           
                val2 = right_sorted[j]       

            if val1 < val2:
                merge_sorted.append(val1)
                i += 1
            else:
                merge_sorted.append(val2)
                j += 1

        return merge_sorted
```
