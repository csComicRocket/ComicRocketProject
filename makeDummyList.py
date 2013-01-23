#Eric Smith


def makeDummyList():
    """ Creates a notification_list file with 1000 blank entries"""
    f = open("notification_list",'w')
    for i in range(1000):
        f.write(str(i)+" ;www.google.com\n")
        
    f.close()

    return None

if __name__ == '__main__':
    makeDummyList();
    
