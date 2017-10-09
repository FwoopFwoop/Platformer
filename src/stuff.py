from screeninfo import get_monitors
for m in get_monitors('osx'):
    print(str(m))
