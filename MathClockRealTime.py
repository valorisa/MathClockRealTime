import sympy as sp
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.animation import FuncAnimation

# Active le rendu mathtext de matplotlib
plt.rcParams['text.usetex'] = False
plt.rcParams['font.size'] = 12

x = sp.Symbol('x', real=True)

def generate_math_expression(value, prefer_short=False):
    """
    Génère une expression mathématique qui s'évalue à 'value'.
    Retourne directement une string LaTeX (pas d'évaluation par SymPy).
    """
    
    # Expressions COURTES (longueur LaTeX < 15 caractères)
    short_expressions = [
        f"|{value}|",
        f"{value}^1",
        f"\\sqrt{{{value}^2}}",
        f"\\lceil {value - 0.5} \\rceil",
        f"\\lfloor {value + 0.5} \\rfloor",
        f"{value} \\cdot 1",
        f"{value} + 0",
        f"\\sqrt[3]{{{value}^3}}",
        f"\\lceil {value} \\rceil",
        f"\\lfloor {value} \\rfloor",
        f"0 + {value}",
        f"{value} - 0",
        f"1 \\cdot {value}",
        f"\\pi \\times {value}/\\pi",
        f"\\sqrt{{{value}}}",
    ]
    
    if value > 1:
        short_expressions.extend([
            f"\\frac{{{value}^2}}{{{value}}}",
            f"\\frac{{{value}!}}{{{value-1}!}}",
            f"\\binom{{{value}}}{{1}}",
            f"{value} + \\phi",
        ])
    
    # Expressions MOYENNES (longueur LaTeX 15-25 caractères)
    medium_expressions = [
        f"\\log(e^{{{value}}})",
        f"{value} \\times \\cos(0)",
        f"{value} + \\sin(0)",
        f"e^{{\\ln({value})}}",
        f"{value} \\times e^0",
        f"\\int_0^1 {value} \\, dx",
        f"\\tan(\\frac{{\\pi}}{{4}}) \\times {value}",
        f"{value} \\div \\cos(0)",
        f"\\sec(0) \\times {value}",
        f"\\csc(\\frac{{\\pi}}{{2}}) \\times {value}",
        f"\\sin(\\frac{{\\pi}}{{3}}) \\times {value}",
        f"\\sum_{{i=1}}^{{{value}}} 1",
        f"\\log_{{10}}(10^{{{value}}})",
    ]
    
    if value > 1:
        medium_expressions.extend([
            f"{value} + \\tan(0)",
            f"{value} \\times \\sin(\\pi/2)",
            f"\\lim_{{x \\to 0}} \\frac{{\\sin({value} x)}}{{x}}",
            f"\\frac{{d}}{{dx}} ({value} x) \\Big|_{{x=1}}",
            f"e \\times \\log_e({value})",
        ])
    
    # Expressions LONGUES (longueur LaTeX > 25 caractères)
    long_expressions = []
    if value > 1:
        long_expressions.extend([
            f"\\int_{{0}}^{{{value}}} 1 \\, dx",
            f"{value-1} + \\cos^2(x) + \\sin^2(x)",
            f"\\log_{{{value}}}( {value}^{{{value}}} )",
            f"\\sqrt[{value}]{{{value}^{{{value}}}}}",
            f"({value-1} + 1) \\times \\cos(0)",
            f"\\sum_{{i=1}}^{{{value}}} \\frac{{1}}{{i}}",
            f"\\sqrt{{{value}^2 + \\pi^2}}",
            f"\\log_{{e}}(e^{{{value}}})",
        ])
    
    # Sélection selon la préférence
    if prefer_short:
        pool = short_expressions
    else:
        pool = short_expressions + medium_expressions + long_expressions
    
    return random.choice(pool)


def draw_clock():
    """Crée et anime l'horloge mathématique."""
    fig, ax = plt.subplots(figsize=(11, 11))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Cercle principal
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=3, color='#2c3e50')
    ax.add_artist(circle)
    
    # Paramètres d'affichage
    MAX_LATEX_LENGTH = 30
    BASE_FONTSIZE = 14
    MIN_FONTSIZE = 9
    
    # Positions critiques (près des axes)
    CRITICAL_POSITIONS = [12, 3, 6, 9]

    print("\n" + "="*70)
    print("🕐 GÉNÉRATION DE L'HORLOGE MATHÉMATIQUE")
    print("="*70)
    
    for h in range(1, 13):
        angle = np.pi/2 - (h * 2 * np.pi / 12)
        
        # Distance et préférence selon la position
        if h in CRITICAL_POSITIONS:
            distance = 1.30
            prefer_short = True
        else:
            distance = 1.22
            prefer_short = False
            
        x_pos = distance * np.cos(angle)
        y_pos = distance * np.sin(angle)

        # Génération de plusieurs candidats
        candidates = []
        for _ in range(15):
            expr_latex = generate_math_expression(h, prefer_short=prefer_short)
            candidates.append(expr_latex)
        
        # Sélection de la meilleure expression (choix aléatoire parmi les valides)
        valid_candidates = [c for c in candidates if len(c) <= MAX_LATEX_LENGTH]
        if valid_candidates:
            best_latex = random.choice(valid_candidates)
        else:
            best_latex = str(h)
        
        print(f"✓ Position {h:2d}: ${best_latex}$ ({len(best_latex)} caractères)")
        
        # Ajustement de la taille de police selon la longueur
        if len(best_latex) <= 10:
            final_fontsize = BASE_FONTSIZE + 2
        elif len(best_latex) <= 15:
            final_fontsize = BASE_FONTSIZE + 1
        elif len(best_latex) <= 20:
            final_fontsize = BASE_FONTSIZE
        elif len(best_latex) <= 25:
            final_fontsize = BASE_FONTSIZE - 2
        else:
            final_fontsize = max(MIN_FONTSIZE, BASE_FONTSIZE - 3)
        
        # Padding adaptatif
        if len(best_latex) <= 10:
            pad_size = 0.3
        elif len(best_latex) <= 20:
            pad_size = 0.35
        else:
            pad_size = 0.4
        
        # Affichage avec mathtext
        ax.text(
            x_pos, y_pos, f"${best_latex}$",
            fontsize=final_fontsize,
            ha='center', va='center',
            bbox=dict(
                facecolor='white', 
                alpha=0.95, 
                edgecolor='#95a5a6', 
                linewidth=1,
                boxstyle=f'round,pad={pad_size}'
            ),
            color='#2c3e50',
            weight='normal'
        )
    
    print("="*70)
    print("✅ Horloge générée avec succès! Les expressions sont visibles.\n")
    
    # Aiguilles de l'horloge
    hour_hand, = ax.plot([], [], linewidth=8, color='#2c3e50', 
                         solid_capstyle='round', zorder=5)
    minute_hand, = ax.plot([], [], linewidth=5, color='#e74c3c', 
                           solid_capstyle='round', zorder=6)
    second_hand, = ax.plot([], [], linewidth=2, color='#27ae60', 
                           solid_capstyle='round', zorder=7)
    
    # Point central
    ax.plot(0, 0, 'o', color='#34495e', markersize=14, zorder=10)
    
    # Titre ajusté pour éviter le tronquage
    plt.title("⏰ Horloge Mathématique Animée ⏰", 
              fontsize=20, weight='bold', pad=20, color='#2c3e50')
    
    # Légende
    legend_elements = [
        plt.Line2D([0], [0], color='#2c3e50', linewidth=8, label='Heures'),
        plt.Line2D([0], [0], color='#e74c3c', linewidth=5, label='Minutes'),
        plt.Line2D([0], [0], color='#27ae60', linewidth=2, label='Secondes')
    ]
    ax.legend(handles=legend_elements, loc='upper left', 
              fontsize=12, framealpha=0.95, edgecolor='#bdc3c7')

    def update(frame):
        """Met à jour la position des aiguilles."""
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second + now.microsecond / 1_000_000
        
        # Calcul des angles
        hour_angle = np.pi/2 - ((hour + minute/60) * 2 * np.pi / 12)
        minute_angle = np.pi/2 - ((minute + second/60) * 2 * np.pi / 60)
        second_angle = np.pi/2 - (second * 2 * np.pi / 60)
        
        # Mise à jour des aiguilles
        hour_hand.set_data([0, 0.50 * np.cos(hour_angle)], 
                          [0, 0.50 * np.sin(hour_angle)])
        minute_hand.set_data([0, 0.75 * np.cos(minute_angle)], 
                            [0, 0.75 * np.sin(minute_angle)])
        second_hand.set_data([0, 0.88 * np.cos(second_angle)], 
                            [0, 0.88 * np.sin(second_angle)])
        
        return hour_hand, minute_hand, second_hand

    # Animation
    anim = FuncAnimation(fig, update, interval=50, blit=True, 
                        cache_frame_data=False)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_clock()
