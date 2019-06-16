import re

input = "hello :))..."
# output = re.sub(u'(^[\u4E00-\u9FA5a-zA-Z0-9+_])', r'', input)
output = re.sub(u'([\u0021-\u002f|\u003A-\u0040|\u005B-\u0060|\u007B-\u007E|\uFF01-\uFFEE])', r'', input)
print(output)