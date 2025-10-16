```
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l = 0
        h =  len(numbers) -1 
        arr = []
        while l < h:
            if numbers[l] + numbers[h] == target :
                arr.append(l+1)
                arr.append(h+1)
                return arr
            elif numbers[l] + numbers[h]  > target:
                h -= 1
            else :
                l +=1
```
