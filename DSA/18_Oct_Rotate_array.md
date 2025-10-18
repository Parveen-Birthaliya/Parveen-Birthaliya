```
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k = k % n  # handle cases where k > n

        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        # Step 1: Reverse entire array
        reverse(0, n - 1)
        # Step 2: Reverse first k elements
        reverse(0, k - 1)
        # Step 3: Reverse remaining elements
        reverse(k, n - 1)
```
```
nums = [1, 2, 3, 4, 5]
k = 2
k = k % len(nums)  # handle if k > len(nums)

rotated = nums[-k:] + nums[:-k]
print(rotated)
# Output: [4, 5, 1, 2, 3]
```
