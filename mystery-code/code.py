min_dist = float('inf')
points = [(1,1), (3,5), (-3,2), (4,4), (-1,-3)]
point1 = None
point2 = None
for a in points:
	for b in points:
                dist = ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)  # Pythagoras told me this should work; actually distance squared, but sqrt(x) is monotonic
                if min_dist > dist and a is not b: 
                    min_dist = dist
                    point1 = a
                    point2 = b
print(point1)
print(point2)

