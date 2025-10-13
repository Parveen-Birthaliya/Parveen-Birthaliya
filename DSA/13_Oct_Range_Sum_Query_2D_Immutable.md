```
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            self.prefix = []
            return
        
        rows, cols = len(matrix), len(matrix[0])
        # prefix has one extra row and column (all zeros) for boundary handling
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

        # Build prefix sum matrix
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                self.prefix[i][j] = (
                    matrix[i - 1][j - 1]                    
                    + self.prefix[i - 1][j]                
                    + self.prefix[i][j - 1]                
                    - self.prefix[i - 1][j - 1]             
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        # +1 offsets because prefix has an extra row & column at start
        r1, c1, r2, c2 = row1 + 1, col1 + 1, row2 + 1, col2 + 1
        
        return (
            self.prefix[r2][c2]
            - self.prefix[r1 - 1][c2]
            - self.prefix[r2][c1 - 1]
            + self.prefix[r1 - 1][c1 - 1]
        )
```
