from screeninfo import get_monitors
for m in get_monitors():
    for n in m:
        print(n)
