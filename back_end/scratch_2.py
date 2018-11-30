with open('teachers.txt','r') as f:
    cnt=1
    while f:
        i=f.readline().split(',')
        tid=i[2].strip()
        while len(i)>2:
            id,rm,pd,*args=f.readline().split(',')
            if args:
                f.readline()
                break
            print(cnt)
            print(f'teacher: {tid}')
            print(f'courseID: {id.strip()}')
            print(f'room: {rm.strip()}')
            print()
            cnt+=1
