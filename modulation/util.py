import matplotlib.pyplot as plt

def triangular(x,A):
    return np.absolute(np.fmod(np.absolute(x),2*A)-A)

def plot_graph(x,y,title,name,xlabel="Volts",ylabel="Frequncy",color="b",condition="scatter"):
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(20,3))
    plot_axis(fig,ax)
    s = [1 for i in x]
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if condition=="scatter":
        plt.scatter(x,y,s,c=color)
    elif condition=="plot":
        plt.plot(x,y,s,c=color)
    fig.tight_layout()
    plt.savefig(f'static/results/{name}',bbox_inches='tight')
    plt.close()


def plot_axis(fig,ax):
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')



