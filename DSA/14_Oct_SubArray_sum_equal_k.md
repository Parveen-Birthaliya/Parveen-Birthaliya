```
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sum = 0
        count = 0
        prefix_count = {0: 1} 
        for num in nums:
            prefix_sum += num

            if prefix_sum - k in prefix_count:
                count += prefix_count[prefix_sum - k]

            prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

        return count
```

```
class Solution:
    def subarraySum(self, nums:List[int], k:int) -> int:
        count = 0
        current_sum = 0

        sum_counts = {0:1}

        for num in nums:
            current_sum += num

            if (current_sum - k) in sum_counts:
                count += sum_counts[current_sum -k]

            sum_counts[current_sum] = sum_counts.get(current_sum, 0) + 1

        return count
```
