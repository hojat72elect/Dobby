import screeninfo

if __name__ == '__main__':
    for monitor in screeninfo.get_monitors(screeninfo.Enumerator.Windows):
        print(monitor)