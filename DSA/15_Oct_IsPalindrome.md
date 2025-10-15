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
