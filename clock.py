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
k = sp.Symbol('k', integer=True)

def evaluate_expression(latex, value):
    """Évalue une expression LaTeX avec SymPy pour vérifier si elle vaut exactement 'value'."""
    try:
        # Appliquer le formatage uniquement si %d est présent
        if '%d' in latex:
            expr_str = latex % value
        else:
            expr_str = latex
        # Supprimer les délimiteurs pour l'évaluation
        expr_str = expr_str.replace(r"\lfloor ", "").replace(r" \rfloor", "").replace(r"\lceil ", "").replace(r" \rceil", "")
        expr = sp.sympify(sp.latex_to_sympy(expr_str) if hasattr(sp, 'latex_to_sympy') else expr_str)
        result = sp.simplify(expr)
        return result.equals(value) if hasattr(result, 'equals') else result == value
    except Exception as e:
        print(f"Evaluation error for {latex}: {e}")
        return False

def iterated_log(value):
    """Calcule le nombre d'itérations de ln nécessaires pour obtenir ≤ 1."""
    count = 0
    current = value
    while current > 1 and count < 10:
        current = sp.ln(current)
        count += 1
    return count

def generate_math_expression(value, prefer_short=False):
    # Expressions complexes et variées, sans trivialités, corrigées pour exactitude
    complex_expressions = []
    if value == 1:
        complex_expressions.append((r"\int_{0}^{1} \frac{1}{1 + \tan^2(x)} \sec^2(x) \, dx", lambda v: sp.integrate(1/(1 + sp.tan(x)**2) * sp.sec(x)**2, (x, 0, v))))
    if value == 2:
        complex_expressions.append((r"\sum_{k=1}^{2} (1 - \frac{1}{k(k+1)})", lambda v: sp.summation(1 - 1/(k*(k+1)), (k, 1, v))))  # Exactement 2
    if value == 3:
        complex_expressions.append((r"\int_{0}^{3} e^{x} e^{-x} \, dx", lambda v: sp.integrate(sp.exp(x) * sp.exp(-x), (x, 0, v))))
    if value == 4:
        complex_expressions.append((r"\ln^*(\exp(\exp(\exp(\exp(1)))))", lambda v: iterated_log(sp.exp(sp.exp(sp.exp(sp.exp(1)))))))
    if value == 5:
        complex_expressions.append((r"\frac{\text{card}(S_5)}{24}", lambda v: 120 / 24))
    if value == 6:
        complex_expressions.append((r"\sum_{k=1}^{6} \frac{1}{k(k+1)} \cdot 6", lambda v: 6 * sp.summation(1/(k*(k+1)), (k, 1, v))))
    if value == 7:
        complex_expressions.append((r"\int_{0}^{7} \frac{\sin^2(x) + \cos^2(x)}{1} \, dx", lambda v: sp.integrate((sp.sin(x)**2 + sp.cos(x)**2)/1, (x, 0, v))))
    if value == 8:
        complex_expressions.append((r"\sum_{k=1}^{8} \ln(e) / \ln(e)", lambda v: sp.summation(1, (k, 1, v))))
    if value == 9:
        complex_expressions.append((r"\int_{0}^{9} (e^x / e^x) \, dx", lambda v: sp.integrate(sp.exp(x)/sp.exp(x), (x, 0, v)) if v > 0 else 0))
    if value == 10:
        complex_expressions.append((r"\sum_{k=1}^{10} \frac{10}{k} - \frac{10}{k+1} + \frac{1}{11}", lambda v: sp.summation(10/k - 10/(k+1) + 1/11, (k, 1, v)) - 9/11))
    if value == 11:
        complex_expressions.append((r"\int_{0}^{11} (\tan^2(x) + 1) \cdot \frac{1}{\sec^2(x)} \, dx", lambda v: sp.integrate((sp.tan(x)**2 + 1) * 1/sp.sec(x)**2, (x, 0, v))))
    if value == 12:
        complex_expressions.append((r"\sum_{k=1}^{12} \frac{12! / (12-k)!}{11! / (11-k)!}", lambda v: sp.summation(sp.factorial(12)/(sp.factorial(12-k)*sp.factorial(k)) / (sp.factorial(11)/(sp.factorial(11-k)*sp.factorial(k))), (k, 1, v))))

    # Intégrales complexes variées
    integral_expressions = [
        (r"\int_{0}^{%d} \sin^2(x) + \cos^2(x) \, dx", lambda v: sp.integrate(sp.sin(x)**2 + sp.cos(x)**2, (x, 0, v))),
        (r"\int_{0}^{%d} e^x e^{-x} \, dx", lambda v: sp.integrate(sp.exp(x) * sp.exp(-x), (x, 0, v)))
    ]
    if value > 1:
        integral_expressions.extend([
            (r"\int_{0}^{%d} \frac{1}{\sec^2(x)} (\tan^2(x) + 1) \, dx", lambda v: sp.integrate(1/sp.sec(x)**2 * (sp.tan(x)**2 + 1), (x, 0, v))),
            (r"\int_{0}^{%d} \frac{\sin(x)}{\sin(x)} \, dx", lambda v: sp.integrate(sp.sin(x)/sp.sin(x), (x, 0, v)) if v > 0 else 0)
        ])

    # Séries complexes variées
    series_expressions = [
        (r"\sum_{k=1}^{%d} \frac{1}{k(k+1)} \cdot %d", lambda v: v * sp.summation(1/(k*(k+1)), (k, 1, v))),
        (r"\sum_{k=1}^{%d} \frac{%d}{k} - \frac{%d}{k+1}", lambda v: sp.summation(v/k - v/(k+1), (k, 1, v)))
    ]
    if value > 1:
        series_expressions.extend([
            (r"\sum_{k=1}^{%d} \frac{%d! / (%d-k)!}{(%d-1)! / (%d-1-k)!}", lambda v: sp.summation(sp.factorial(v)/(sp.factorial(v-k)*sp.factorial(k)) / (sp.factorial(v-1)/(sp.factorial(v-1-k)*sp.factorial(k))), (k, 1, v))),
            (r"\sum_{k=1}^{%d} \ln(e) / \ln(e)", lambda v: sp.summation(1, (k, 1, v)))
        ])

    # Combinaison selon la préférence
    if prefer_short:
        pool = complex_expressions
    else:
        pool = complex_expressions + integral_expressions + series_expressions

    candidates = []
    max_attempts = 20
    attempts = 0
    while attempts < max_attempts and not candidates:
        for latex_template, expr_lambda in pool:
            try:
                sympy_result = sp.simplify(expr_lambda(value))
                # Décision entre plancher et plafond basée sur la proximité
                if not (sympy_result.equals(value) if hasattr(sympy_result, 'equals') else sympy_result == value):
                    result_float = float(sympy_result)
                    diff_lower = value - result_float
                    diff_upper = result_float - value
                    if diff_lower < 1 and diff_lower >= 0:  # Plus proche du plancher
                        latex = r"\lfloor " + latex_template % value + r" \rfloor" if '%d' in latex_template else r"\lfloor " + latex_template + r" \rfloor"
                        if len(latex) <= 30 and evaluate_expression(latex.replace(r"\lfloor ", "").replace(r" \rfloor", ""), value):
                            candidates.append(latex)
                    elif diff_upper < 1 and diff_upper >= 0:  # Plus proche du plafond
                        latex = r"\lceil " + latex_template % value + r" \rceil" if '%d' in latex_template else r"\lceil " + latex_template + r" \rceil"
                        if len(latex) <= 30 and evaluate_expression(latex.replace(r"\lceil ", "").replace(r" \rceil", ""), value):
                            candidates.append(latex)
                else:
                    latex = latex_template % value if '%d' in latex_template else latex_template
                    if len(latex) <= 30 and evaluate_expression(latex, value):
                        candidates.append(latex)
            except Exception as e:
                print(f"Failed to evaluate {latex_template} for value {value}: {e}")
                pass
        attempts += 1

    if candidates:
        return random.choice(candidates)
    else:
        print(f"Warning: No valid expression found for value {value} after {max_attempts} attempts, using fallback.")
        return str(value)

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
        if minute % 5 == 0 and second < 1:
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
                    elif latex_len <= 30: final_fontsize = BASE_FONTSIZE - 3
                    else: final_fontsize = max(MIN_FONTSIZE, BASE_FONTSIZE - 4)
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

    anim = FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False, repeat=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_clock()
