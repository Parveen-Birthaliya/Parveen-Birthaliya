## But Time complexity exceed

```

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        final = []
        for num in range(len(nums)):
            arr = nums.copy()
            del arr[num]
            product = math.prod(arr)
            final.append(product)

        return final

```

## Solution
```

python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        answer=[1]*len(nums)
        prefix=1
        postfix=1

        #prefix update
        for i in range(len(nums)):
            answer[i]=prefix
            prefix*=nums[i]

        for j in range(len(nums)-1,-1,-1):
            answer[j]*=postfix
            postfix*=nums[j]
        return answer

        ```
