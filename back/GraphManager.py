import matplotlib.pyplot as plt

def monthly_pie_chart(user, month_title, month):
    month_str = f"-{month:02d}-" # Feb: -02-
    print(month_str)

    data = {}
    for date, sessions in reversed(user.data['sesiones'].items()):
        if not month_str in date: continue

        for name, dur in sessions:
            total = data.get(name, 0) + dur
            if total == 0: continue
            data[name] = total
    
    vals = data.values()
    keys = data.keys()
    
    # PIE CHART
    _, ax = plt.subplots(figsize=(6, 4))
    porciones, _ = ax.pie(vals, radius=0.7)
    ax.set_position([-0.2,0,1,1])

    ax.legend(porciones, keys,
        title=month_title,
        loc="center left",
        bbox_to_anchor=(0.9, 0, 0.5, 1))

    if len(vals) > 0:
        plt.show()

def piece_graph(user, piece):
    plt.clf()

    keys = []
    vals = []

    for date, sessions in user.data['sesiones'].items():
        for name, dur in sessions:
            if name == piece: 
                keys.append(f"{int(date.split('-')[2])}/{int(date.split('-')[1])}") # 2026-02-16 → 16/2
                vals.append(dur/60)
    
    plt.plot(keys, vals, linewidth=4)

    if len(keys) > 1:
        plt.show()