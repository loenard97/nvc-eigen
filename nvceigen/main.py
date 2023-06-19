import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from nvceigen.vector import Vector3D
from nvceigen.eigen import resonances, odmr_fit_func


def calculate_resonances(x, Bx, By, Bz):
    """
    Calculate resonances from B-Field
    """
    c = 1
    a1, a2, a3, a4, a5, a6, a7, a8 = [0.1] * 8
    w1, w2, w3, w4, w5, w6, w7, w8 = [10] * 8
    f1, f2, f3, f4, f5, f6, f7, f8 = np.sort(resonances(Vector3D(Bx, By, Bz)))
    return odmr_fit_func(x, c, a1, w1, f1, a2, w2, f2, a3, w3, f3, a4, w4, f4, a5, w5, f5, a6, w6, f6, a7, w7, f7, a8, w8, f8)


def plot():
    mw_freq = np.linspace(2600, 3100, 800)
    initial_b_field = [0, 0, 0]

    fig = plt.figure("NV center Hamiltonian")
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    fig.subplots_adjust(bottom=0.45)

    # resonances plot
    line, = ax1.plot(mw_freq, calculate_resonances(mw_freq, *initial_b_field), lw=2)
    ax1.set_xlabel('MW Frequency / MHz')

    # slider
    ax_slider_bx = fig.add_axes([0.25, 0.3, 0.65, 0.03])
    slider_bx = Slider(
        ax=ax_slider_bx,
        label='B_x',
        valmin=-100,
        valmax=100,
        valinit=initial_b_field[0],
    )
    ax_slider_by = fig.add_axes([0.25, 0.2, 0.65, 0.03])
    slider_by = Slider(
        ax=ax_slider_by,
        label="B_y",
        valmin=-100,
        valmax=100,
        valinit=initial_b_field[1],
        # orientation="vertical"
    )
    ax_slider_bz = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    slider_bz = Slider(
        ax=ax_slider_bz,
        label="B_z",
        valmin=-100,
        valmax=100,
        valinit=initial_b_field[2],
    )

    # button
    ax_btn_reset = fig.add_axes([0.05, 0.3, 0.1, 0.04])
    btn_reset = Button(ax_btn_reset, 'Reset', hovercolor='0.975')

    def handle_button_reset(event):
        slider_bx.reset()
        slider_by.reset()
        slider_bz.reset()

    btn_reset.on_clicked(handle_button_reset)

    ax_btn_invert = fig.add_axes([0.05, 0.2, 0.1, 0.04])
    btn_invert = Button(ax_btn_invert, 'Invert', hovercolor='0.975')

    def handle_btn_invert(event):
        slider_bx.set_val(-slider_bx.val)
        slider_by.set_val(-slider_by.val)
        slider_bz.set_val(-slider_bz.val)

    btn_invert.on_clicked(handle_btn_invert)

    # nv and field plot
    nv_vectors = [
        Vector3D( 1, -1, -1).normalize() * 70,
        Vector3D(-1,  1, -1).normalize() * 70,
        Vector3D(-1, -1,  1).normalize() * 70,
        Vector3D( 1,  1,  1).normalize() * 70,
    ]

    ax2.quiver(0, 0, 0, slider_bx.val, slider_by.val, slider_bz.val, pivot='tail', color='red')
    for vec in nv_vectors:
        ax2.quiver(0, 0, 0, *vec, pivot='tail', color='green')
    ax2.set_xlim([-100, 100])
    ax2.set_ylim([-100, 100])
    ax2.set_zlim([-100, 100])
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')

    # animation
    def update(val):
        line.set_ydata(calculate_resonances(mw_freq, slider_bx.val, slider_by.val, slider_bz.val))
        ax2.clear()
        ax2.quiver(0, 0, 0, slider_bx.val, slider_by.val, slider_bz.val, pivot='tail', color='red')
        for vec in nv_vectors:
            ax2.quiver(0, 0, 0, *vec, pivot='tail', color='green')
        ax2.set_xlim([-100, 100])
        ax2.set_ylim([-100, 100])
        ax2.set_zlim([-100, 100])
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel('z')
        fig.canvas.draw_idle()

    slider_bx.on_changed(update)
    slider_by.on_changed(update)
    slider_bz.on_changed(update)

    plt.show()


if __name__ == '__main__':
    plot()
