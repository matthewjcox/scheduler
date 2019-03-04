from matplotlib import pyplot as plt

rounds=[]
dynscores=[]
statscores=[]
with open("runs/past_runs/2019_03_01__20_09_06/log.log") as f:
    lines=f.readlines()
    for i in lines:
        splits=i.split('|')
        text=splits[3].strip()
        if text[:5]=="Round":
            vals=text.replace(':','|').replace('(','|').replace(')','|').split('|')
            rnd=int(vals[0].split(' ')[1])
            dyn=float(vals[1].split(' ')[2])
            stat=float(vals[2])
            rounds.append(rnd)
            dynscores.append(dyn)
            statscores.append(stat)
            # if 35430<rnd<35450:
            #     print(rnd, dyn, stat)
# print(rounds)
# print(dynscores)
# print(statscores)

plt.plot(rounds,dynscores)
plt.show()