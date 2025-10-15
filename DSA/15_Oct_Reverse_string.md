```
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        left = 0 
        right =  len(s)-1
        while left < right:
            num = s[left]
            s[left] = s[right]
            s[right] = num
            left = left + 1
            right = right -1 
```
```

        s[:] = s[::-1]

```
```

        for i in range(len(s) // 2):
            s[i], s[~i] =s[~i], s[i]
```
