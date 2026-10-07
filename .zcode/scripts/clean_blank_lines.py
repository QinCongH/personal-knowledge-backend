import re

path = 'md/3_RAG链路搭建.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 去掉 --- 分隔符前后的空行： --- 上下各贴紧
content = re.sub(r'\n+\n---\n+\n', '\n\n---\n\n', content)

# 2. 标题(#, ##, ###)后紧贴内容（去掉标题后的空行）
# 只对 ## 级别及以上做处理，避免影响普通段落
def tight_heading(match):
    return match.group(0).rstrip() + '\n'

# 3. 去除 --- 周围多余的空行（保留一个）
content = re.sub(r'\n{2,}---\n{2,}', '\n\n---\n\n', content)

# 4. 删除行尾的空白字符
content = re.sub(r'[ \t]+\n', '\n', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# 输出对比
print(f"Lines: {content.count(chr(10))}")
print("Done")