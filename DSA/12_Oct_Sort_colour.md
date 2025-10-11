```
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            for j in range(len(nums)-1,i,-1):
                if nums[i] == 0 :
                    i = i +1
                elif nums[j] == 2:
                    j = j -1
                elif nums[i] == 2:
                    num = nums[i]
                    nums[i] = nums[j]
                    nums[j] = num
                    j= j -1

                elif nums[j]==0:
                    num = nums[i]
                    nums[i] = nums[j]
                    nums[j] = num
                    i= i +1


```
## Best Solution # pointer
```
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        low =0
        mid = 0
        high = len(nums)-1

        for num in nums:
            if nums[mid] ==0:
                nums[low],nums[mid] = nums[mid], nums[low]
                mid += 1
                low += 1
            
            elif nums[mid] == 2:
                nums[mid], nums[high] =  nums[high], nums[mid]
                high -= 1

            else:
                mid += 1


```
