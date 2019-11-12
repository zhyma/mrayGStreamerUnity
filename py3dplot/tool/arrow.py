from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

if __name__ == '__main__' :
    fig = plt.figure()
    ax = Axes3D(fig)
    
    a = Arrow3D([0.0, 1.0], [0.0, 0.0], [0.0, 0.0], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
    a = Arrow3D([0.0, 0.0], [0.0, 1.0], [0.0, 0.0], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
    a = Arrow3D([0.0, 0.0], [0.0, 0.0], [0.0, 1.0], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
