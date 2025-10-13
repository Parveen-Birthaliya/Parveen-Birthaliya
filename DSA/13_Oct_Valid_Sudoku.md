# hash set
```
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        rows = defaultdict(set)
        cols = defaultdict(set)
        boxes = defaultdict(set)

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    continue

                if (
                    val in rows[r] or
                    val in cols[c] or
                    val in boxes[(r//3, c//3)]
                ):
                    return False

                rows[r].add(val)
                cols[c].add(val)
                boxes[(r//3, c//3)].add(val)

        return True      
```
# using bit
```
class Solution:
    def isValidSudoku(self, board):
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    continue

                bit = 1 << (int(val) - 1)
                box_id = (r // 3) * 3 + (c // 3)

                if (rows[r] & bit) or (cols[c] & bit) or (boxes[box_id] & bit):
                    return False

                rows[r] |= bit
                cols[c] |= bit
                boxes[box_id] |= bit

        return True
```
# brute force
```
class Solution:
    def isValidSudoku(self, board):
        def is_valid_unit(unit):
            nums = [c for c in unit if c != '.']
            return len(nums) == len(set(nums))
        
        # check rows
        for row in board:
            if not is_valid_unit(row):
                return False

        # check columns
        for col in zip(*board):
            if not is_valid_unit(col):
                return False

        # check 3x3 boxes
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                box = [
                    board[i][j]
                    for i in range(r, r + 3)
                    for j in range(c, c + 3)
                ]
                if not is_valid_unit(box):
                    return False
        
        return True
```
