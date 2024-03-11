require 'descriptive_statistics'
data = [2,6,9,3,5,1,8,3,6,9,2]
# => [2, 6, 9, 3, 5, 1, 8, 3, 6, 9, 2]
data.mean
# => 4.909090909090909
data.median
# => 5.0
data.variance
# => 7.7190082644628095
data.standard_deviation
# => 2.778310325442932

(1..5).mean #Range

DescriptiveStatistics.mode([1,2,3,4,5])

[1,2,3].standard_deviation