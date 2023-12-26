img = detector.findHands(img , draw=False)
        lmlist = detector.findPossition(img)
        if lmlist[0]:
            print(lmlist)
            cmd = 'ON'
        else:
            cmd = 'OFF'