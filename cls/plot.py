# 这个链接有相关的seaborn的示例数据与显示效果
# https://www.jianshu.com/p/5ff47c7d0cc9

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class MyPlot(object):

    def __init__(self, datas):
        self.datas = datas

    # 使用更为应用级别的库，基于matplotlib seaborn
    def snsPlotTest(self):
        # Define a variable N
        N = 500
        # Construct the colormap
        current_palette = sns.color_palette("muted", n_colors=5)
        cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
        # Initialize the data
        data1 = np.random.randn(N)
        data2 = np.random.randn(N)
        # Assume that there are 5 possible labels
        colors = np.random.randint(0,5,N)
        # Create a scatter plot
        plt.scatter(data1, data2, c=colors, cmap=cmap)
        # Add a color bar
        plt.colorbar()
        # Show the plot
        plt.savefig('d:/aaa.png')
        plt.show()