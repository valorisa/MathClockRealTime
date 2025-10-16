import sympy as sp
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.animation import FuncAnimation

x = sp.Symbol('x', real=True)

def random_advanced_expr(value):
    funcs = [
        lambda v: sp.log(sp.exp(v)),
        lambda v: sp.sqrt(v**2),
        lambda v: sp.Abs(v),
        lambda v: sp.floor(v + 0.7),
        lambda v: v*sp.exp(0),
        lambda v: sp.cos(0) + v - 1,
        lambda v: sp.sin(sp.pi) + v,
        lambda v: v + sp.I*0,
        lambda v: sp.Integral(1, (x, 0, v)),
        lambda v: sp.Sum(1, (x, 1, v)),
        lambda v: sp.log(value) / sp.log(sp.exp(1)),
        lambda v: sp.Pow(v,1),
    ]
    random.shuffle(funcs)
    for f in funcs:
        try:
            expr = f(value)
            expr = sp.simplify(expr)
            if expr.equals(sp.Integer(value)):
                return expr
        except:
            continue
    return sp.Integer(value)

def expr_to_str(expr):
    latex_str = sp.latex(expr)
    latex_str = latex_str.replace(r"limits", "")  # Correction rendering matplotlib
    return latex_str

def draw_clock():
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-1.3,1.3)
    ax.set_ylim(-1.3,1.3)
    ax.set_aspect('equal')
    ax.axis('off')

    circle = plt.Circle((0,0),1,fill=False,linewidth=2)
    ax.add_artist(circle)

    hour_exprs = []
    for h in range(1, 13):
        expr = random_advanced_expr(h)
        hour_exprs.append(expr)

    for h in range(1, 13):
        angle = np.pi/2 - (h * 2 * np.pi / 12)
        x_pos = 0.85 * np.cos(angle)
        y_pos = 0.85 * np.sin(angle)
        expr_str = expr_to_str(hour_exprs[h-1])
        ax.text(x_pos, y_pos, f"${expr_str}$", fontsize=18, ha='center', va='center')

    hour_hand, = ax.plot([], [], linewidth=6, color='darkblue', label='Heure')
    minute_hand, = ax.plot([], [], linewidth=3, color='red', label='Minute')
    second_hand, = ax.plot([], [], linewidth=1, color='green', label='Seconde')

    ax.plot(0,0, 'ko')
    plt.title("Horloge Mathématique Avancée Animée", fontsize=20)
    plt.legend(loc='upper right')

    def update(frame):
        now = datetime.now()
        hour = now.hour % 12 or 12
        minute = now.minute
        second = now.second + now.microsecond / 1_000_000

        hour_angle = np.pi/2 - ((hour + minute / 60) * 2 * np.pi / 12)
        minute_angle = np.pi/2 - (minute * 2 * np.pi / 60)
        second_angle = np.pi/2 - (second * 2 * np.pi / 60)

        hour_x = [0, 0.5 * np.cos(hour_angle)]
        hour_y = [0, 0.5 * np.sin(hour_angle)]
        minute_x = [0, 0.8 * np.cos(minute_angle)]
        minute_y = [0, 0.8 * np.sin(minute_angle)]
        second_x = [0, 0.9 * np.cos(second_angle)]
        second_y = [0, 0.9 * np.sin(second_angle)]

        hour_hand.set_data(hour_x, hour_y)
        minute_hand.set_data(minute_x, minute_y)
        second_hand.set_data(second_x, second_y)

        return hour_hand, minute_hand, second_hand

    anim = FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)

    plt.show()

if __name__ == "__main__":
    draw_clock()
