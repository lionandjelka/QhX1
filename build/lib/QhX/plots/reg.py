
import matplotlib.pyplot as plt
import numpy as np


def plt_freq_heatmap(data, extent, label = 'correlation coefficient', xlabel = r'Frequency $[d^{-1}]$', ylabel =  'Frequency $[d^{-1}]$'):
    """Function for plotting of heatmap of Hybrid2D output

        Parameters
        ----------
        data: autocorrelation data (output of hybrid2d method)
        label: label for each points
        xlabel, ylabel: text for x and y labels 
    """
    
    fig, ax = plt.subplots(figsize=[5, 4])
    im=ax.imshow(np.rot90(data).T/np.rot90(data).T.max(),extent=extent)#,ax.colorbar()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    
    clb=fig.colorbar(im, orientation='vertical')
    
    clb.ax.set_ylabel(label,fontsize=13)
    plt.show()
    


def fig_plot(tt, yy, xlabel='t [days]', ylabel='magnitude [mag]'):
    """
    Function for figure plotting

    Parameters
    ----------
    tt: x-axis data (usually time)
    yy: y-axis data (magnitude)
    xlabel, ylabel: text for x and y labels 
    """

    # Calculate the mean difference for the sampling
    sampling = np.mean(np.diff(tt))
    label = f'Sampling: {sampling:.2f}'

    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)
    ax.plot(tt, yy, 'ko', markersize=1, label=label)

    custom_xlim = (tt.min(), tt.max())
    custom_ylim = (yy.min() - 0.1, yy.max() + 0.1)
    ax.set_xlabel(xlabel, fontsize=18, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=18, labelpad=10)
    ax.tick_params(direction='in', pad=5, labelsize=13)
    plt.setp(ax, xlim=custom_xlim, ylim=custom_ylim)
    ax.legend(fontsize=12)

    plt.show()
