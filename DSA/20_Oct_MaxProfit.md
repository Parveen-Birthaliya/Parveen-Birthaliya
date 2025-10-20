```class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float('inf')  # minimum price seen so far
        max_profit = 0            # maximum profit so far
        
        for price in prices:
            # If we find a smaller buying price, update min_price
            if price < min_price:
                min_price = price
            # Otherwise, check if selling now gives a better profit
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit
```
