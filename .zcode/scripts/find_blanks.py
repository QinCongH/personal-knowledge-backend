path = 'md/3_RAG链路搭建.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

blank_count = 0
prev_line_idx = 0
excess_locations = []
for i, line in enumerate(lines, 1):
    if line.strip() == '':
        blank_count += 1
    else:
        if blank_count >= 2:
            excess_locations.append((prev_line_idx, i, blank_count))
        blank_count = 0
        prev_line_idx = i

if excess_locations:
    print("Found locations with 2+ consecutive blank lines:")
    for loc in excess_locations:
        print(f"  After line {loc[0]}, before line {loc[1]}: {loc[2]} blank lines")
        # Show context
        start = max(0, loc[0]-1)
        end = min(len(lines), loc[1])
        for k in range(start, end):
            marker = ">>>" if k == loc[0] else "   "
            print(f"    {marker} L{k+1}: {lines[k].rstrip()}")
else:
    print("No locations with 2+ consecutive blank lines found.")

print(f"\nTotal lines: {len(lines)}")
print(f"Total blank lines: {sum(1 for l in lines if l.strip() == '')}")