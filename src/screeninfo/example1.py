import screeninfo

if __name__ == '__main__':
    for monitor in screeninfo.get_monitors():
        print(monitor)