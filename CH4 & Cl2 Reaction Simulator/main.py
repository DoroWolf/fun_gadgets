import math
import random
import sys

import pygame
import tkinter as tk

pygame.init()
pygame.display.set_caption("CH4 & Cl2 reaction simulator")

CARBON = (128, 128, 128)
HYDROGEN = (255, 255, 255)
CHLORINE = (0, 255, 0)

light_on = False
paused = False

def update_background():
    if light_on:
        return (50, 50, 50)
    else:
        return (0, 0, 0)

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, vx, vy, kind):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.kind = kind
        self.timer = random.randint(500, 1000) if kind == 'Cl2' else None
        self.angle = 0
        self.counting = False

    def start_timer(self):
        if self.kind == 'Cl2':
            self.counting = True
            self.timer = random.randint(500, 1000)

    def stop_timer(self):
        self.counting = False

    def move(self, width, height):
        if paused:
            return
        if self.counting:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = 0
        self.x += self.vx
        self.y += self.vy
        self.angle += math.hypot(self.vx, self.vy) * 0.1

        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        angle = self.angle
        def rotate_point(cx, cy, px, py, a):
            s, c = math.sin(a), math.cos(a)
            px -= cx
            py -= cy
            return (int(cx + px * c - py * s), int(cy + px * s + py * c))

        if self.kind == 'CH4':
            for dx, dy in [(10, 0), (0, 10), (-10, 0), (0, -10)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, HYDROGEN, (rx, ry), 4)
            pygame.draw.circle(screen, CARBON, (x, y), 8)
        elif self.kind == 'Cl2':
            pygame.draw.circle(screen, CHLORINE, rotate_point(x, y, x - 5, y, angle), 10)
            pygame.draw.circle(screen, CHLORINE, rotate_point(x, y, x + 5, y, angle), 10)
        elif self.kind == 'Cl•':
            surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*CHLORINE, 128), (10, 10), 10)
            screen.blit(surface, (x - 10, y - 10))
        elif self.kind == 'CH3•':
            surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            cx, cy = 15, 15
            for dx, dy in [(-10, 0), (0, 10), (0, -10)]:
                rx, ry = rotate_point(cx, cy, cx + dx, cy + dy, angle)
                pygame.draw.circle(surface, (*HYDROGEN, 128), (rx, ry), 4)
            pygame.draw.circle(surface, (*CARBON, 128), (cx, cy), 8)
            screen.blit(surface, (x - 15, y - 15))
        elif self.kind == 'HCl':
            pygame.draw.circle(screen, HYDROGEN, rotate_point(x, y, x - 4, y, angle), 5)
            pygame.draw.circle(screen, CHLORINE, rotate_point(x, y, x + 4, y, angle), 10)
        elif self.kind == 'CH3Cl':
            pygame.draw.circle(screen, CHLORINE, rotate_point(x, y, x + 10, y, angle), 10)
            for dx, dy in [(-10, 0), (0, 10), (0, -10)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, HYDROGEN, (rx, ry), 4)
            pygame.draw.circle(screen, CARBON, (x, y), 8)
        elif self.kind == 'CH2Cl•':
            surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            cx, cy = 20, 20
            pygame.draw.circle(surface, (*CHLORINE, 128), rotate_point(cx, cy, cx + 10, cy, angle), 10)
            for dx, dy in [(-10, 0), (0, -10)]:
                rx, ry = rotate_point(cx, cy, cx + dx, cy + dy, angle)
                pygame.draw.circle(surface, (*HYDROGEN, 128), (rx, ry), 4)
            pygame.draw.circle(surface, (*CARBON, 128), (cx, cy), 8)
            screen.blit(surface, (x - 20, y - 20))
        elif self.kind == 'CH2Cl2':
            for dx, dy in [(10, 0), (0, 10)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, CHLORINE, (rx, ry), 10)
            for dx, dy in [(-10, 0), (0, -10)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, HYDROGEN, (rx, ry), 4)
            pygame.draw.circle(screen, CARBON, (x, y), 8)
        elif self.kind == 'CHCl2•':
            surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            cx, cy = 20, 20
            for dx, dy in [(10, 0), (0, 10)]:
                rx, ry = rotate_point(cx, cy, cx + dx, cy + dy, angle)
                pygame.draw.circle(surface, (*CHLORINE, 128), (rx, ry), 10)
            rx, ry = rotate_point(cx, cy, cx, cy - 10, angle)
            pygame.draw.circle(surface, (*HYDROGEN, 128), (rx, ry), 4)
            pygame.draw.circle(surface, (*CARBON, 128), (cx, cy), 8)
            screen.blit(surface, (x - 20, y - 20))
        elif self.kind == 'CHCl3':
            for dx, dy in [(10, 0), (0, 10), (-10, 0)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, CHLORINE, (rx, ry), 10)
            pygame.draw.circle(screen, HYDROGEN, rotate_point(x, y, x, y - 10, angle), 4)
            pygame.draw.circle(screen, CARBON, (x, y), 8)
        elif self.kind == 'CCl3•':
            surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            cx, cy = 20, 20
            for dx, dy in [(10, 0), (0, 10), (-10, 0)]:
                rx, ry = rotate_point(cx, cy, cx + dx, cy + dy, angle)
                pygame.draw.circle(surface, (*CHLORINE, 128), (rx, ry), 10)
            pygame.draw.circle(surface, (*CARBON, 128), (cx, cy), 8)
            screen.blit(surface, (x - 20, y - 20))
        elif self.kind == 'CCl4':
            for dx, dy in [(10, 0), (0, 10), (-10, 0), (0, -10)]:
                rx, ry = rotate_point(x, y, x + dx, y + dy, angle)
                pygame.draw.circle(screen, CHLORINE, (rx, ry), 10)
            pygame.draw.circle(screen, CARBON, (x, y), 8)
        elif self.kind == 'C2H6':
            C1_x, C1_y = x - 8, y
            C2_x, C2_y = x + 8, y
            C1_x, C1_y = rotate_point(x, y, C1_x, C1_y, angle)
            C2_x, C2_y = rotate_point(x, y, C2_x, C2_y, angle)

            for dx, dy in [(0, 10), (-10, 0), (0, -10)]:
                h_x, h_y = rotate_point(C1_x, C1_y, C1_x + dx, C1_y + dy, angle)
                pygame.draw.circle(screen, HYDROGEN, (h_x, h_y), 4)
            
            for dx, dy in [(10, 0), (0, 10), (0, -10)]:
                h_x, h_y = rotate_point(C2_x, C2_y, C2_x + dx, C2_y + dy, angle)
                pygame.draw.circle(screen, HYDROGEN, (h_x, h_y), 4)

            pygame.draw.circle(screen, CARBON, (C1_x, C1_y), 8)
            pygame.draw.circle(screen, CARBON, (C2_x, C2_y), 8)

particles = []

def get_molecule_counts():
    root = tk.Tk()
    root.title("Setting molecule counts")
    root.geometry("300x140")
    root.resizable(False, False)

    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())

    tk.Label(root, text="CH₄ counts:").pack()
    ch4_entry = tk.Entry(root)
    ch4_entry.insert(0, "2")
    ch4_entry.pack()

    tk.Label(root, text="Cl₂ counts:").pack()
    cl2_entry = tk.Entry(root)
    cl2_entry.insert(0, "10")
    cl2_entry.pack()

    result = {}

    def submit():
        try:
            result["CH4"] = int(ch4_entry.get())
            result["Cl2"] = int(cl2_entry.get())
            if result["CH4"] < 0 or result["Cl2"] < 0 or result["CH4"] + result["Cl2"] > 500:
                raise ValueError
            root.destroy()
        except ValueError:
            pass

    tk.Button(root, text="Start", command=submit).pack(pady=10)
    root.mainloop()

    return result.get("CH4", 2), result.get("Cl2", 10)

def init(n_CH4, n_Cl2):
    particles.clear()
    width, height = screen.get_size()

    center_x, center_y = width // 2, height // 2
    range_x = width // 4
    range_y = height // 4

    for _ in range(n_CH4):
        x = random.randint(center_x - range_x, center_x + range_x)
        y = random.randint(center_y - range_y, center_y + range_y)
        particles.append(Particle(x, y, random.uniform(-1, 1), random.uniform(-1, 1), 'CH4'))

    for _ in range(n_Cl2):
        x = random.randint(center_x - range_x, center_x + range_x)
        y = random.randint(center_y - range_y, center_y + range_y)
        particles.append(Particle(x, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl2'))

    if light_on:
        for p in particles:
            p.start_timer()
            
def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def handle_reactions():
    new_particles = []
    removed = set()
    for i, p1 in enumerate(particles):
        if p1.kind == 'Cl2' and p1.counting:
            p1.timer -= 1
            if p1.timer <= 0:
                new_particles.append(Particle(p1.x + 20, p1.y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                new_particles.append(Particle(p1.x - 20, p1.y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                removed.add(i)

        for j, p2 in enumerate(particles):
            if i >= j or i in removed or j in removed:
                continue
            d = distance(p1, p2)
            if d > 20:
                continue

            kinds = {p1.kind, p2.kind}
            x, y = (p1.x + p2.x) / 2, (p1.y + p2.y) / 2

            if kinds == {'Cl•'}:
                # 自由基合并
                new_particles.append(Particle(x, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl2'))
                removed.update([i, j])
            elif 'Cl•' in kinds:
                # 链式反应
                other = (p1.kind if p2.kind == 'Cl•' else p2.kind)
                replacements = {
                    'CH4': 'CH3•',
                    'CH3Cl': 'CH2Cl•',
                    'CH2Cl2': 'CHCl2•',
                    'CHCl3': 'CCl3•',
                }
                if other in replacements:
                    new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), replacements[other]))
                    new_particles.append(Particle(x + 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'HCl'))
                    removed.update([i, j])
                elif other in ['CH3•', 'CH2Cl•', 'CHCl2•', 'CCl3•']:
                    new_name = {
                        'CH3•': 'CH3Cl',
                        'CH2Cl•': 'CH2Cl2',
                        'CHCl2•': 'CHCl3',
                        'CCl3•': 'CCl4'
                    }[other]
                    new_particles.append(Particle(x, y, random.uniform(-1, 1), random.uniform(-1, 1), new_name))
                    removed.update([i, j])
                else:
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        continue
                    nx, ny = dx / dist, dy / dist
                    p1.vx, p1.vy = -nx, -ny
                    p2.vx, p2.vy = nx, ny
            elif kinds == {'CH3•'}:
                # CH3•之间反应生成C2H6
                new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'C2H6'))
                removed.update([i, j])
            elif kinds == {'CH3•', 'Cl2'}:
                # CH3•与Cl2反应生成CH3Cl和Cl•
                new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'CH3Cl'))
                new_particles.append(Particle(x + 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                removed.update([i, j])
            elif kinds == {'CH2Cl•', 'Cl2'}:
                # CH2Cl•与Cl2反应生成CH2Cl2和Cl•
                new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'CH2Cl2'))
                new_particles.append(Particle(x + 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                removed.update([i, j])
            elif kinds == {'CHCl2•', 'Cl2'}:
                # CHCl2•与Cl2反应生成CHCl3和Cl•
                new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'CHCl3'))
                new_particles.append(Particle(x + 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                removed.update([i, j])
            elif kinds == {'CCl3•', 'Cl2'}:
                # CCl3•与Cl2反应生成CCl4和Cl•
                new_particles.append(Particle(x - 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'CCl4'))
                new_particles.append(Particle(x + 20, y, random.uniform(-1, 1), random.uniform(-1, 1), 'Cl•'))
                removed.update([i, j])
            else:
                # 如果不发生反应，弹开
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue
                nx, ny = dx / dist, dy / dist
                p1.vx, p1.vy = -nx, -ny
                p2.vx, p2.vy = nx, ny

    for i in sorted(removed, reverse=True):
        del particles[i]
    particles.extend(new_particles)

if __name__ == "__main__":
    n_ch4, n_cl2 = get_molecule_counts()
    init(n_CH4=n_ch4, n_Cl2=n_cl2)

    running = True
    while running:
        screen.fill(update_background())
        width, height = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:  # 检测P键
                    paused = not paused  # 切换暂停状态
                elif event.key == pygame.K_l:
                    light_on = not light_on
                    if light_on:
                        for p in particles:
                            p.start_timer()
                    else:
                        for p in particles:
                            p.stop_timer()
                elif event.key == pygame.K_r:
                    init(n_CH4=n_ch4, n_Cl2=n_cl2)

        if paused:
            font = pygame.font.Font(None, 36)
            text = font.render("Paused", True, (255, 255, 255))
            screen.blit(text, (10, 10))

        for p in particles:
            p.move(width, height)
            p.draw(screen)

        handle_reactions()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
