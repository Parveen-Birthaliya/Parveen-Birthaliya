```
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        length = min(len(word1),len(word2))
        string=""
        for i in range(length):
            string +=  word1[i] + word2[i]
           
        if len(word1) ==  len(word2):
            return string

        elif len(word1) > length:
            string = string + word1[length:]
        else :
            string = string+ word2[length:]

        return string

```
