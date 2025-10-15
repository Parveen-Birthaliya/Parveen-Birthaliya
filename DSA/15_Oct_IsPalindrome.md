```
import re
class Solution:
    def isPalindrome(self, s: str) -> bool:
        
        def clean_text(s):
            if not isinstance(s, str):
                return s
            return re.sub(r'[^A-Za-z0-9]', '', s)
        s= clean_text(s)
        s=s.lower()
        for i in range(len(s)//2):
            if s[i] == s[-i-1]:
                continue
            else:
                return False
        return True
```
```
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l=[ch for ch in s if ch.isalnum()]
        st="".join(l).lower()
        if st==" ":
            return True
        if st==st[::-1]:
            return True
        else:
            return False
```
```
class Solution:
    def isPalindrome(self, s: str) -> bool:
        new_str = "".join([char for char in s if char.isalnum()]).lower()
        return new_str == new_str[::-1]
```
