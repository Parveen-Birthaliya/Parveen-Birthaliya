```
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        Set = {}
        count = 0
        for num in nums:
            if num in Set:
                Set[num] +=1
            else:
                Set[num] = 1
        Sorted_Set = sorted(Set.items(), key = lambda item: item[1], reverse = True)
        array = [item[0] for item in Sorted_Set[:k]]
        return array
```
Best Solution
```
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        sorted_counter = sorted(Counter(nums).items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_counter[:k]]
```

```
from collections import Counter
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Part 1: Count frequencies of each number in nums
        # Counter(nums) creates a dictionary-like object mapping numbers to their counts.
        # Example: if nums = [1,1,1,2,2,3], Counter(nums) would be Counter({1: 3, 2: 2, 3: 1})
        counts = Counter(nums)
        
        # Part 2: Sort the items (key-value pairs) from the Counter
        # counts.items() returns a view of (number, count) tuples.
        # sorted(...) sorts this list of tuples.
        # key=lambda x: x[1] specifies that the sorting should be based on the second element of each tuple (which is the count).
        # reverse=True ensures the sort is in descending order (highest count first).
        # Example: if counts = Counter({1: 3, 2: 2, 3: 1}), sorted_counter would be [(1, 3), (2, 2), (3, 1)]
        sorted_counter = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        # Part 3: Extract the top k elements (numbers)
        # sorted_counter[:k] slices the sorted list to get only the first k (number, count) tuples.
        # [num for num, _ in ...] is a list comprehension.
        # For each (num, count) tuple in the sliced list, it takes 'num' (the number)
        # and ignores '_' (the count, which we don't need in the final output).
        # This creates a new list containing only the top k most frequent numbers.
        # Example: if k=2 and sorted_counter is [(1, 3), (2, 2), (3, 1)],
        # sorted_counter[:k] would be [(1, 3), (2, 2)].
        # The list comprehension would then extract [1, 2].
        return [num for num, _ in sorted_counter[:k]]

```
