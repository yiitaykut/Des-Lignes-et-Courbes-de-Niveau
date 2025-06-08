import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, RadioButtons

# 10 farklı fonksiyon tanımı (farklı şekillerde)
def f1(x, y): return np.sin(x) + np.cos(y)
def f2(x, y): return np.sin(x*y)
def f3(x, y): return np.exp(-x*2 - y*2)
def f4(x, y): return np.sin(x) * np.cos(y)
def f5(x, y): return np.tanh(x) - np.tanh(y)
def f6(x, y): return np.sin(np.sqrt(x*2 + y*2))
def f7(x, y): return np.cos(x) + np.cos(y) - 1
def f8(x, y): return np.sin(x*2 - y*2)
def f9(x, y): return np.exp(np.sin(x) * np.cos(y))
def f10(x, y): return np.log(np.abs(x*y) + 1)

functions = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
function_names = [
    "sin(x)+cos(y)", "sin(xy)", "exp(-x²-y²)", "sin(x)*cos(y)", "tanh(x)-tanh(y)",
    "sin(sqrt(x²+y²))", "cos(x)+cos(y)-1", "sin(x² - y²)", "exp(sin(x)*cos(y))", "log(|xy|+1)"
]

# Grid oluştur
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)

# Başlangıç fonksiyon ve z0
current_func_idx = 0
Z = functions[current_func_idx](X, Y)
z0 = 0

# Figure ayarı
fig = plt.figure(figsize=(14,6))

# 2D contour plot
ax1 = fig.add_subplot(1, 2, 1)
contours = ax1.contour(X, Y, Z, levels=10, colors='blue')
ax1.clabel(contours, inline=True, fontsize=8)
ax1.set_title(f'Ligne de Niveau (2D): {function_names[current_func_idx]}')
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# 3D surface + contour at z=z0
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf = ax2.plot_surface(X, Y, Z, alpha=0.5, cmap='viridis')
contour_set = ax2.contour(X, Y, Z, levels=[z0], colors='red', linewidths=3, offset=z0)
ax2.set_title(f'Courbe de Niveau (3D, z={z0:.2f})')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z = f(x,y)')
ax2.set_zlim(np.min(Z), np.max(Z))

# Slider z0 için
ax_slider = plt.axes([0.25, 0.02, 0.50, 0.03])
slider = Slider(ax_slider, 'z kesiti', np.min(Z), np.max(Z), valinit=z0)

# Radio buttons fonksiyon seçimi için
rax = plt.axes([0.82, 0.3, 0.15, 0.4], facecolor='lightgoldenrodyellow')
radio = RadioButtons(rax, function_names)

def update_z(val):
    z_val = slider.val
    ax2.cla()
    ax2.plot_surface(X, Y, Z, alpha=0.5, cmap='viridis')
    ax2.contour(X, Y, Z, levels=[z_val], colors='red', linewidths=3, offset=z_val)
    ax2.set_title(f'Courbe de Niveau (3D, z={z_val:.2f})')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z = f(x,y)')
    ax2.set_zlim(np.min(Z), np.max(Z))
    fig.canvas.draw_idle()

def update_func(label):
    global current_func_idx, Z
    current_func_idx = function_names.index(label)
    Z = functions[current_func_idx](X, Y)
    
    # 2D plot update
    ax1.cla()
    contours = ax1.contour(X, Y, Z, levels=10, colors='blue')
    ax1.clabel(contours, inline=True, fontsize=8)
    ax1.set_title(f'Ligne de Niveau (2D): {label}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    
    # 3D plot update (reset slider range and value)
    ax2.cla()
    slider.valmin = np.min(Z)
    slider.valmax = np.max(Z)
    slider.set_val(0)  # slider event otomatik çağrılır
    
    ax2.plot_surface(X, Y, Z, alpha=0.5, cmap='viridis')
    ax2.contour(X, Y, Z, levels=[0], colors='red', linewidths=3, offset=0)
    ax2.set_title(f'Courbe de Niveau (3D, z=0.00)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z = f(x,y)')
    ax2.set_zlim(np.min(Z), np.max(Z))
    
    fig.canvas.draw_idle()

slider.on_changed(update_z)
radio.on_clicked(update_func)

plt.show()