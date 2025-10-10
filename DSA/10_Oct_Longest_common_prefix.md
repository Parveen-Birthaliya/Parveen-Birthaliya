# 1 Vertical
```
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""  # Empty list edge case
        if not strs[0]:
            return ""  # First string is empty
        
        # Iterate over each character index of the first string
        for j in range(len(strs[0])):
            char = strs[0][j]
            # Compare this character with the corresponding character in other strings
            for i in range(1, len(strs)):
                # If current string is shorter or characters mismatch
                if j == len(strs[i]) or strs[i][j] != char:
                    return strs[0][:j]  # Return prefix found so far
        
        # All characters of the first string are common prefix
        return strs[0]
```
# 2  Horizontal 
```
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""  # Empty list edge case
        
        # Take the first string as initial prefix
        prefix = strs[0]
        
        # Compare prefix with each subsequent string
        for i in range(1, len(strs)):
            # While the current string does not start with the prefix,
            # shorten the prefix by removing the last character
            while not strs[i].startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:  # If prefix becomes empty, no common prefix
                    return ""
        
        return prefix
```
