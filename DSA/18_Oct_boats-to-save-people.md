```
class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        left, right = 0, len(people) - 1
        boats = 0

        while left <= right:
            # If lightest + heaviest can share one boat
            if people[left] + people[right] <= limit:
                left += 1  # both taken
                right -= 1
            else:
                # heaviest goes alone
                right -= 1

            boats += 1

        return boats
```
