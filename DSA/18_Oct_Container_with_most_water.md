```
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) -1
        max_area =0
        while left < right:
            n = right - left
            h = min(height[left],height[right])
            area = n*h
            max_area = max(area,max_area)
            if height[left] > height[right]:
                right -=1
            else :
                left +=1
            
```
