import json

with open("med-spec.txt") as f:
    spec = f.readlines()
x = {}
for s in spec:
    s = s.strip().split("\t")
    if " or " in s[1]:
        ss = s[1].split(" or ")
        if ss[0] not in x:
            x[ss[0]] = [s[0]]
        else:
            x[ss[0]].append(s[0])

        if ss[0] not in x[ss[0]]:
            x[ss[0]].append(ss[0])

        if ss[1] not in x:
            x[ss[1]] = [s[0]]
        else:
            x[ss[1]].append(s[0])

        if ss[1] not in x[ss[1]]:
            x[ss[1]].append(ss[1])

    else:
        if s[1] not in x:
            x[s[1]] = [s[0]]
        else:
            x[s[1]].append(s[0])

        if s[1] not in x[s[1]]:
            x[s[1]].append(s[1])

print(json.dumps(x, indent=4))\
