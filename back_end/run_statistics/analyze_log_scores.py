from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

rounds=[]
dynscores=[]
statscores=[]
newdynscores=[]
newstatscores=[]
times=[]
MAX=49960
with open("runs/past_runs/2019_04_04__16_10_48/log.log") as f:
    lines=f.readlines()
    splits=[]
    for i in lines:
        if i.strip():
            splits.append(i.split('|'))

    text=[i[3].strip() for i in splits if len(i)>=4]
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

    print(text[:10])
    for n,i in enumerate(text):
        if i=='New:':
            stat,dyn=text[n+2].split(" ")
            newstatscores.append(float(stat)/MAX)
            newdynscores.append(float(dyn)/MAX)
        if i=='Old:':
            stat, dyn = text[n + 2].split(" ")
            statscores.append(float(stat)/MAX)
            dynscores.append(float(dyn)/MAX)
        if i[:5] == "Round":
            vals=i.replace(':','|').replace('(','|').replace(')','|').split('|')
            rnd=int(vals[0].split(' ')[1])
            rounds.append(rnd)
            tm=vals[-1]
            tms=[0,0,0,0,0,0]+tm.split(" ")
            hrs=float(tms[-6])+float(tms[-4])/60+float(tms[-2])/3600
            times.append(hrs)
        rounds=rounds[:len(statscores)]
        times = times[:len(statscores)]
dynscoredeltas=[newdynscores[i]-dynscores[i] for i in range(len(rounds))]
statscoredeltas=[newstatscores[i]-statscores[i] for i in range(len(rounds))]
cnt=0
# print(rounds)
# print(dynscores)
# print(statscores)
# ax=plt.subplot(311)
# plt.title('Dynamic scores')
# plt.plot(rounds[1:],dynscores[1:])
ax1=plt.subplot(211)
plt.title('Scores')
plt.plot(times[1:],statscores[1:])
ax2=plt.subplot(212)
plt.title('Score changes')
plt.plot(times[1:],dynscoredeltas[1:])
plt.plot([times[1],times[-1]],[0,0])
ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:+.2%}'.format(y)))
ax1.set_xlabel("Time (h)")
ax2.set_xlabel("Time (h)")
ax1.set_ylabel("Schedule completion")
ax2.set_ylabel("Change")
plt.show()