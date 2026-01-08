import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.animation import FuncAnimation
import random

# Configuration matplotlib
import matplotlib
matplotlib.use('TkAgg')
plt.rcParams['text.usetex'] = False
plt.rcParams['font.size'] = 12

def generate_original_expression(value):
    """Génère des expressions mathématiques originales et rigoureuses (compatible matplotlib)"""
    
    expressions = {
        1: [
            r"\gcd(7, 6)",  # PGCD
            r"\dim(\mathbb{R})",  # Dimension de R
            r"\chi(\mathrm{disque})",  # Caractéristique d'Euler du disque
            r"\lim_{x \to 0} \frac{\sin x}{x}",  # Limite classique
            r"e^{i\pi} + 2",  # Formule d'Euler modifiée
            r"\mathrm{rang}(\vec{e}_1)",  # Rang vecteur unitaire
            r"|\mathbb{Z}_1|",  # Cardinal
        ],
        2: [
            r"\chi(\mathrm{sph\grave{e}re})",  # Caractéristique d'Euler de S²
            r"\deg(x^2)",  # Degré polynôme
            r"\binom{2}{1}",  # Coefficient binomial
            r"|\{0,1\}|",  # Cardinal ensemble
            r"\gcd(6, 4)",  # PGCD
            r"\mathrm{Tr}(I_2)",  # Trace identité 2x2
            r"1 + 1",  # Somme
        ],
        3: [
            r"\dim(\mathbb{R}^3)",  # Dimension espace
            r"\lfloor \pi \rfloor",  # Partie entière de π
            r"\binom{3}{2}",  # Combinaisons
            r"|\mathbb{Z}_3|",  # Cardinal Z/3Z
            r"\gcd(9, 12)",  # PGCD
            r"\# \mathrm{\ c\hat{o}t\acute{e}s\ triangle}",  # Côtés triangle
            r"1 + 2",  # Somme
        ],
        4: [
            r"2^2",  # Puissance
            r"\# \{z \in \mathbb{C} : z^4=1\}",  # Racines 4èmes
            r"\lfloor e \rfloor + 1",  # Partie entière de e + 1
            r"\gcd(8, 12)",  # PGCD
            r"\binom{4}{1}",  # Coefficient binomial
            r"\dim(\mathbb{C}^2)",  # Dimension (sur R)
            r"|2i|^2",  # Module au carré
        ],
        5: [
            r"\binom{5}{1}",  # Coefficient binomial
            r"\# \mathrm{\ sommets\ pentagone}",  # Sommets pentagone
            r"\lfloor \sqrt{26} \rfloor",  # Partie entière √26
            r"|\{1,2,3,4,5\}|",  # Cardinal
            r"10 / 2",  # Division
            r"\gcd(15, 20)",  # PGCD
            r"1 + 4",  # Somme
        ],
        6: [
            r"3!",  # Factorielle
            r"\# \mathrm{\ faces\ cube}",  # Faces d'un cube
            r"\gcd(18, 24)",  # PGCD
            r"\binom{4}{2}",  # Combinaisons
            r"2 \times 3",  # Produit simple
            r"|\mathbb{Z}_6|",  # Cardinal
            r"\mathrm{Tr}(2I_3)",  # Trace 2×identité 3x3
        ],
        7: [
            r"\# \mathrm{\ jours/semaine}",  # Jours de la semaine
            r"\lfloor 2\pi \rfloor + 1",  # Partie entière de 2π + 1
            r"\binom{7}{1}",  # Coefficient binomial
            r"|\mathbb{Z}_7|",  # Cardinal Z/7Z
            r"4 + 3",  # Somme
            r"14 / 2",  # Division
            r"\gcd(21, 14)",  # PGCD
        ],
        8: [
            r"2^3",  # Puissance
            r"\# \mathrm{\ sommets\ cube}",  # Sommets cube
            r"\binom{8}{7}",  # Coefficient binomial
            r"\gcd(16, 24)",  # PGCD
            r"|\mathbb{Z}_8|",  # Cardinal
            r"4 \times 2",  # Produit
            r"\lfloor 3\pi \rfloor - 1",  # Partie entière
        ],
        9: [
            r"3^2",  # Puissance
            r"\binom{9}{8}",  # Coefficient binomial
            r"\lfloor \pi^2 \rfloor",  # Partie entière π²
            r"\dim(\mathbb{R}^9)",  # Dimension
            r"|\{1,2,...,9\}|",  # Cardinal
            r"18 / 2",  # Division
            r"|3i|^2",  # Module au carré
        ],
        10: [
            r"\binom{5}{2}",  # Coefficient binomial
            r"2 \times 5",  # Produit
            r"|\mathbb{Z}_{10}|",  # Cardinal Z/10Z
            r"\# \mathrm{\ doigts}",  # Doigts humains
            r"20 / 2",  # Division
            r"\gcd(30, 20)",  # PGCD
            r"\lfloor e^2 \rfloor + 3",  # Partie entière
        ],
        11: [
            r"\binom{11}{10}",  # Coefficient binomial
            r"\lfloor \sqrt{123} \rfloor",  # Partie entière √123
            r"|\mathbb{Z}_{11}|",  # Cardinal Z/11Z (corps fini)
            r"6 + 5",  # Somme
            r"\gcd(33, 22)",  # PGCD
            r"22 / 2",  # Division
            r"3! + 5",  # Factorielle + 5
        ],
        12: [
            r"3 \times 4",  # Produit
            r"\# \mathrm{\ ar\hat{e}tes\ cube}",  # Arêtes cube
            r"\binom{12}{11}",  # Coefficient binomial
            r"\gcd(24, 36)",  # PGCD
            r"|\{1,2,...,12\}|",  # Cardinal
            r"24 / 2",  # Division
            r"3! + 3!",  # Double factorielle
        ]
    }
    
    return random.choice(expressions.get(value, [str(value)]))

def draw_clock():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')

    # Cercle principal avec style élégant
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=4, color='#2c3e50', alpha=0.8)
    ax.add_artist(circle)

    # Cercle décoratif externe
    circle_outer = plt.Circle((0, 0), 1.12, fill=False, linewidth=1.5, color='#95a5a6', alpha=0.5, linestyle='--')
    ax.add_artist(circle_outer)

    # Traits pour les heures et minutes
    for i in range(60):
        angle = np.pi/2 - (i * 2 * np.pi / 60)
        if i % 5 == 0:
            length = 0.12
            linewidth = 2.5
            color = '#34495e'
        else:
            length = 0.06
            linewidth = 1
            color = '#95a5a6'
        x_start = 1.0 * np.cos(angle)
        y_start = 1.0 * np.sin(angle)
        x_end = (1.0 - length) * np.cos(angle)
        y_end = (1.0 - length) * np.sin(angle)
        ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=linewidth, zorder=4)

    # Paramètres d'affichage améliorés
    BASE_FONTSIZE = 11
    CRITICAL_POSITIONS = [12, 3, 6, 9]
    
    # Distances ajustées pour chaque position
    position_distances = {
        12: 1.40,  # Haut - plus loin
        1: 1.32,
        2: 1.32,
        3: 1.42,   # Droite - plus loin
        4: 1.32,
        5: 1.32,
        6: 1.40,   # Bas - plus loin
        7: 1.32,
        8: 1.32,
        9: 1.42,   # Gauche - plus loin
        10: 1.32,
        11: 1.32
    }

    # Génération et affichage des expressions mathématiques
    texts = []
    print("\n" + "="*80)
    print("🎯 HORLOGE MATHÉMATIQUE - FORMULES ORIGINALES")
    print("="*80)
    
    for h in range(1, 13):
        angle = np.pi/2 - (h * 2 * np.pi / 12)
        distance = position_distances.get(h, 1.32)
        x_pos = distance * np.cos(angle)
        y_pos = distance * np.sin(angle)
        
        expr = generate_original_expression(h)
        
        # Ajustement dynamique de la taille selon la longueur
        expr_len = len(expr)
        if expr_len > 35:
            fontsize = BASE_FONTSIZE - 2
            pad = 0.35
        elif expr_len > 25:
            fontsize = BASE_FONTSIZE - 1
            pad = 0.38
        else:
            fontsize = BASE_FONTSIZE
            pad = 0.42
        
        text = ax.text(
            x_pos, y_pos, f"${expr}$",
            fontsize=fontsize,
            ha='center', va='center',
            bbox=dict(
                facecolor='#ecf0f1',
                alpha=0.95,
                edgecolor='#34495e',
                linewidth=1.5,
                boxstyle=f'round,pad={pad}'
            ),
            color='#2c3e50',
            weight='bold'
        )
        texts.append(text)
        print(f"  {h:2d}h → ${expr}$")
    
    print("="*80 + "\n")

    # Aiguilles
    hour_hand, = ax.plot([], [], linewidth=9, color='#34495e', solid_capstyle='round', zorder=5)
    minute_hand, = ax.plot([], [], linewidth=6, color='#e74c3c', solid_capstyle='round', zorder=6)
    second_hand, = ax.plot([], [], linewidth=2.5, color='#3498db', solid_capstyle='round', zorder=7)

    # Centre de l'horloge
    ax.plot(0, 0, 'o', color='#e74c3c', markersize=16, zorder=10)
    ax.plot(0, 0, 'o', color='#ecf0f1', markersize=8, zorder=11)

    plt.title("⚡ Horloge Mathématique - Édition Originale ⚡", 
              fontsize=22, weight='bold', pad=25, color='#2c3e50',
              bbox=dict(boxstyle='round,pad=0.6', facecolor='#ecf0f1', edgecolor='#34495e', linewidth=2))

    # Légende stylisée
    legend_elements = [
        plt.Line2D([0], [0], color='#34495e', linewidth=9, label='Heures'),
        plt.Line2D([0], [0], color='#e74c3c', linewidth=6, label='Minutes'),
        plt.Line2D([0], [0], color='#3498db', linewidth=2.5, label='Secondes')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, 
              framealpha=0.9, edgecolor='#34495e', fancybox=True, shadow=True)

    def update(frame):
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second + now.microsecond / 1_000_000

        # Rafraîchissement toutes les 3 minutes
        if minute % 3 == 0 and second < 1:
            print(f"\n🔄 Rafraîchissement à {now.strftime('%H:%M:%S')}")
            for h, text in enumerate(texts, 1):
                angle = np.pi/2 - (h * 2 * np.pi / 12)
                distance = position_distances.get(h, 1.32)
                x_pos = distance * np.cos(angle)
                y_pos = distance * np.sin(angle)
                
                new_expr = generate_original_expression(h)
                text.set_text(f"${new_expr}$")
                text.set_position((x_pos, y_pos))
                
                # Ajustement dynamique
                expr_len = len(new_expr)
                if expr_len > 35:
                    text.set_fontsize(BASE_FONTSIZE - 2)
                    pad = 0.35
                elif expr_len > 25:
                    text.set_fontsize(BASE_FONTSIZE - 1)
                    pad = 0.38
                else:
                    text.set_fontsize(BASE_FONTSIZE)
                    pad = 0.42
                
                text.set_bbox(dict(
                    facecolor='#ecf0f1',
                    alpha=0.95,
                    edgecolor='#34495e',
                    linewidth=1.5,
                    boxstyle=f'round,pad={pad}'
                ))
                print(f"  {h:2d}h → ${new_expr}$")

        # Calcul des angles
        hour_angle = np.pi/2 - ((hour + minute/60) * 2 * np.pi / 12)
        minute_angle = np.pi/2 - ((minute + second/60) * 2 * np.pi / 60)
        second_angle = np.pi/2 - (second * 2 * np.pi / 60)

        # Mise à jour des aiguilles
        hour_hand.set_data([0, 0.45 * np.cos(hour_angle)], [0, 0.45 * np.sin(hour_angle)])
        minute_hand.set_data([0, 0.70 * np.cos(minute_angle)], [0, 0.70 * np.sin(minute_angle)])
        second_hand.set_data([0, 0.85 * np.cos(second_angle)], [0, 0.85 * np.sin(second_angle)])

        return hour_hand, minute_hand, second_hand

    anim = FuncAnimation(fig, update, frames=None, interval=100, blit=True, 
                        cache_frame_data=False, repeat=True)

    def on_close(event):
        print("\n👋 Fermeture de l'horloge...\n")
        plt.close()

    fig.canvas.mpl_connect('close_event', on_close)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_clock()