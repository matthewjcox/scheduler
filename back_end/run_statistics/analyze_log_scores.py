from matplotlib import pyplot as plt

rounds=[]
dynscores=[]
statscores=[]
newdynscores=[]
newstatscores=[]
with open("runs/past_runs/2019_03_04__20_51_00/log.log") as f:
    lines=f.readlines()
    splits=[]
    for i in lines:
        splits.append(i.split('|'))
    text=[i[3].strip() for i in splits]
    # for i in text:
    #     if i[:5]=="Round":
    #         vals=i.replace(':','|').replace('(','|').replace(')','|').split('|')
    #         rnd=int(vals[0].split(' ')[1])
    #         dyn=float(vals[1].split(' ')[2])
    #         stat=float(vals[2])
    #         rounds.append(rnd)
    #         dynscores.append(dyn)
    #         statscores.append(stat)
    #         # if 35430<rnd<35450:
    #         #     print(rnd, dyn, stat)
    for n,i in enumerate(text):
        if i=='New:':
            newstatscores.append(float(text[n+2]))
            newdynscores.append(float(text[n+3]))
        if i=='Old:':
            statscores.append(float(text[n+2]))
            dynscores.append(float(text[n+3]))
        if i[:5] == "Round":
            vals=i.replace(':','|').replace('(','|').replace(')','|').split('|')
            rnd=int(vals[0].split(' ')[1])
            rounds.append(rnd)
dynscoredeltas=[newdynscores[i]-dynscores[i] for i in range(len(rounds))]
statscoredeltas=[newstatscores[i]-statscores[i] for i in range(len(rounds))]
cnt=0
for n,i in enumerate(statscoredeltas):

    if i<-8000:
        cnt += 1
        print(n,i)
print(cnt)
# print(rounds)
# print(dynscores)
# print(statscores)
ax=plt.subplot(311)
plt.title('Dynamic scores')
plt.plot(rounds[1:],dynscores[1:])
plt.subplot(312)
plt.title('Static scores')
plt.plot(rounds[1:],statscores[1:])
plt.subplot(313)
plt.title('Dynamic score deltas')
plt.plot(rounds[1:],dynscoredeltas[1:])
plt.show()