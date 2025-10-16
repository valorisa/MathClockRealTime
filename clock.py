import sympy as sp
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.animation import FuncAnimation

# Force l'utilisation d'un backend compatible
import matplotlib
matplotlib.use('TkAgg')

# Active le rendu mathtext de matplotlib
plt.rcParams['text.usetex'] = False
plt.rcParams['font.size'] = 12

x = sp.Symbol('x', real=True)

def generate_math_expression(value, prefer_short=False):
    # Expressions de base exactes (sans 0 + n, n^1, et complexes avec valeurs numériques)
    basic_expressions = [
        r"\sqrt{%d^2}" % value, r"\frac{%d \cdot 1}{1}" % value, r"\pi \times %d/\pi" % value
    ]
    
    # Intégrales complexes rigoureusement exactes avec valeurs numériques
    integral_expressions = [
        r"\int_{0}^{%d} 1 \, dx" % value,
        r"\int_{0}^{%d} (1 + 0)^{x} \, dx" % value,
        r"%d \cdot \int_{0}^{1} x^{0} \, dx" % value
    ]
    if value > 1:
        integral_expressions.extend([
            r"\int_{0}^{%d} \frac{%d \cdot x^{%d}}{%d} \, dx" % (value, value, value-1, value),
            r"\int_{0}^{%d} \frac{1}{%d} \cdot %d \, dx" % (value, value, value)
        ])

    # Séries complexes rigoureusement exactes avec valeurs numériques
    series_expressions = [
        r"\sum_{k=1}^{%d} 1" % value,
        r"\sum_{k=0}^{%d} (1)" % (value-1)
    ]
    if value > 1:
        series_expressions.extend([
            r"\sum_{k=0}^{%d} (2k + 1 - 2k)" % (value-1),
            r"\sum_{k=1}^{%d} 1 \cdot \frac{%d - (k - 1)}{%d - (k - 1)}" % (value, value, value)
        ])

    # Combinaison selon la préférence
    if prefer_short:
        pool = basic_expressions
    else:
        pool = basic_expressions + integral_expressions + series_expressions
    
    return random.choice(pool)

def draw_clock():
    fig, ax = plt.subplots(figsize=(11, 11))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Cercle principal
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=3, color='#34495e')
    ax.add_artist(circle)
    
    # Ajout des traits pour les minutes
    for i in range(60):
        angle = np.pi/2 - (i * 2 * np.pi / 60)
        if i % 5 == 0:
            length = 0.1
            linewidth = 1.5
        else:
            length = 0.05
            linewidth = 0.8
        x_start = 1.1 * np.cos(angle)
        y_start = 1.1 * np.sin(angle)
        x_end = (1.1 + length) * np.cos(angle)
        y_end = (1.1 + length) * np.sin(angle)
        ax.plot([x_start, x_end], [y_start, y_end], color='#7f8c8d', linewidth=linewidth, zorder=4)

    MAX_LATEX_LENGTH = 30
    BASE_FONTSIZE = 14
    MIN_FONTSIZE = 9
    CRITICAL_POSITIONS = [12, 3, 6, 9]

    # Stocker les textes pour mise à jour dynamique
    texts = []
    for h in range(1, 13):
        angle = np.pi/2 - (h * 2 * np.pi / 12)
        if h in CRITICAL_POSITIONS:
            distance = 1.30
            prefer_short = True
        else:
            distance = 1.22
            prefer_short = False
        x_pos = distance * np.cos(angle)
        y_pos = distance * np.sin(angle)

        best_latex = generate_math_expression(h, prefer_short)
        text = ax.text(x_pos, y_pos, f"${best_latex}$", fontsize=BASE_FONTSIZE, ha='center', va='center',
                       bbox=dict(facecolor='white', alpha=0.9, edgecolor='#bdc3c7', linewidth=1,
                                 boxstyle='round,pad=0.35,rounding_size=0.1'), color='#2c3e50', weight='normal')
        texts.append(text)
    
    print("\n" + "="*70)
    print("🕐 GÉNÉRATION DE L'HORLOGE MATHÉMATIQUE")
    print("="*70)
    for h, text in enumerate(texts, 1):
        print(f"✓ Position {h:2d}: ${text.get_text()[1:-1]}$ ({len(text.get_text()[1:-1])} caractères)")  # Supprime $ pour le comptage
    print("="*70)
    print("✅ Horloge générée avec succès! Les expressions seront rafraîchies toutes les 5 minutes.\n")
    
    hour_hand, = ax.plot([], [], linewidth=8, color='#8e44ad', solid_capstyle='round', zorder=5)
    minute_hand, = ax.plot([], [], linewidth=5, color='#e74c3c', solid_capstyle='round', zorder=6)
    second_hand, = ax.plot([], [], linewidth=2, color='#27ae60', solid_capstyle='round', zorder=7)
    
    ax.plot(0, 0, 'o', color='#34495e', markersize=14, zorder=10)
    
    plt.title("Horloge Mathématique Animée", fontsize=20, weight='bold', pad=20, color='#2c3e50')
    
    # Légende minimisée dans le coin inférieur droit
    legend_elements = [plt.Line2D([0], [0], color='#8e44ad', linewidth=8, label='Heures'),
                      plt.Line2D([0], [0], color='#e74c3c', linewidth=5, label='Minutes'),
                      plt.Line2D([0], [0], color='#27ae60', linewidth=2, label='Secondes')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.7, edgecolor='#bdc3c7')

    def update(frame):
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second + now.microsecond / 1_000_000
        
        # Rafraîchissement des formules toutes les 5 minutes
        if minute % 5 == 0 and second < 1:  # Vérifie le début de chaque intervalle de 5 minutes
            for h, text in enumerate(texts, 1):
                if h in CRITICAL_POSITIONS:
                    prefer_short = True
                else:
                    prefer_short = False
                best_latex = generate_math_expression(h, prefer_short)
                if len(best_latex) <= MAX_LATEX_LENGTH:
                    text.set_text(f"${best_latex}$")
                    # Ajuster la taille de police dynamiquement
                    latex_len = len(best_latex)
                    if latex_len <= 10: final_fontsize = BASE_FONTSIZE + 2
                    elif latex_len <= 15: final_fontsize = BASE_FONTSIZE + 1
                    elif latex_len <= 20: final_fontsize = BASE_FONTSIZE
                    elif latex_len <= 25: final_fontsize = BASE_FONTSIZE - 2
                    else: final_fontsize = max(MIN_FONTSIZE, BASE_FONTSIZE - 3)
                    text.set_fontsize(final_fontsize)
                    pad_size = 0.3 if latex_len <= 10 else 0.35 if latex_len <= 20 else 0.4
                    text.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='#bdc3c7', linewidth=1,
                                     boxstyle=f'round,pad={pad_size},rounding_size=0.1'))
            print(f"\nRafraîchissement des formules à {now.strftime('%H:%M:%S')}")
            for h, text in enumerate(texts, 1):
                print(f"✓ Position {h:2d}: ${text.get_text()[1:-1]}$ ({len(text.get_text()[1:-1])} caractères)")
        
        # Mettre à jour les aiguilles
        hour_angle = np.pi/2 - ((hour + minute/60) * 2 * np.pi / 12)
        minute_angle = np.pi/2 - ((minute + second/60) * 2 * np.pi / 60)
        second_angle = np.pi/2 - (second * 2 * np.pi / 60)
        
        hour_hand.set_data([0, 0.50 * np.cos(hour_angle)], [0, 0.50 * np.sin(hour_angle)])
        minute_hand.set_data([0, 0.75 * np.cos(minute_angle)], [0, 0.75 * np.sin(minute_angle)])
        second_hand.set_data([0, 0.88 * np.cos(second_angle)], [0, 0.88 * np.sin(second_angle)])
        print(f"Updating: {now.strftime('%H:%M:%S.%f')[:-3]}")  # Débogage
        fig.canvas.draw()
        fig.canvas.flush_events()
        return hour_hand, minute_hand, second_hand

    anim = FuncAnimation(fig, update, interval=1000, cache_frame_data=False, repeat=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_clock()
