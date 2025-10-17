```
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        nums.sort()
    
        for i in range(len(nums)-2):
            if i > 0 and nums[i] == nums[i+1]:
                continue
            j = i +1
            h = len(nums) -1
            while j < h :
                m = nums[i]+nums[j]+nums[h]
           
                if m > 0:
                    h -= 1
                elif m < 0:
                    j +=1
                else:
                    result.append([nums[i],nums[j],nums[h]])

                    while j < h and nums[j] == nums[j+1]:
                        j += 1

                    while j < h and nums[h] == nums[h-1]:
                        h -= 1
                    
                    j += 1
                    h -= 1

        return result
```
