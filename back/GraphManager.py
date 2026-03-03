import matplotlib.pyplot as plt
import back.DataManager as dm

def monthly_pie_chart(user, month_title, month):
    if len(user.data['sesiones']) == 0: return

    data = {}
    for session in reversed(user.data['sesiones']):
        if month != dm.get_session_month(session): continue

        _, piece_id, dur = session
        name = user.data['piezas'][piece_id][0]

        total = data.get(name, 0) + dur
        if total == 0: continue
        data[name] = total
    if len(data) == 0: return

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
    if len(user.data['sesiones']) == 0: return

    data = {}
    for session in user.data['sesiones']:
        date, piece_id, dur = session
        name = user.data['piezas'][piece_id][0]

        if name == piece: 
            key = dm.get_displayable_session(user, session)[0] # day/month
            data[key] = dur / 60
    
    one_day = True
    for k, v in data.items():
        if k != list(data.keys())[0]: one_day = False
    if one_day: return

    plt.clf()

    vals = data.values()
    keys = data.keys()
    
    plt.plot(keys, vals, linewidth=4)

    plt.show()