from ai.Solution import Solution
from data.load import edges

model = Solution()
model.setEdges(edges)
model.solve()