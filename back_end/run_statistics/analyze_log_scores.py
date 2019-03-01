# from matplotlib import pyplot


with open("runs/past_runs/2019_02_27__19_17_13/log.log") as f:
    lines=f.readlines()
    for i in lines[:10]:
        splits=i.split('|')
        text=splits[3].strip()
        if text[:5]=="Round":
            vals=text.replace(':')
            print(vals)