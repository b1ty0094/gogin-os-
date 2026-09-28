import pygame
import sys
import os
import json
import hashlib
import datetime
import struct

# ============================================================
# ВСТРОЕННЫЙ КОД ОС
# ============================================================
GOGIN_OS_CODE = r'''import pygame
import sys
import datetime
import os
import json
import hashlib
import math
import time
import webbrowser

pygame.init()

WINDOW_W, WINDOW_H = 1000, 700
WIDTH, HEIGHT = WINDOW_W, WINDOW_H
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GoginOS v5.3 - Linux-like Terminal OS")
clock = pygame.time.Clock()
is_fullscreen = False

INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(INSTALL_DIR, "config.json")

if not os.path.exists(CONFIG_PATH):
    print("GoginOS не установлена! Запустите installer.py")
    input("Enter для выхода...")
    sys.exit(1)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

USERNAME = CONFIG.get('username', 'user')
USER_PASSWORD_HASH = CONFIG.get('password_hash', '')
ROOT_PASSWORD_HASH = CONFIG.get('root_password_hash', '')
ROOT_PASSWORD_PLAIN = "00912322"

CONFIG['boot_count'] = CONFIG.get('boot_count', 0) + 1
CONFIG['last_boot'] = datetime.datetime.now().isoformat()
with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(CONFIG, f, indent=2, ensure_ascii=False)

try:
    icon_path = os.path.join(INSTALL_DIR, "gogin.png")
    if os.path.exists(icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))
except:
    pass

COLORS = {
    'bg': (12, 12, 12), 'text': (0, 255, 100), 'text_dim': (0, 150, 60),
    'error': (255, 80, 80), 'info': (80, 180, 255), 'warning': (255, 200, 0),
    'prompt_user': (100, 255, 150), 'prompt_root': (255, 100, 100),
    'cursor': (0, 255, 100), 'success': (46, 204, 113),
    'win_bg': (30, 35, 45), 'win_title': (20, 25, 35),
    'win_border': (60, 70, 90), 'win_text': (230, 230, 230),
    'win_accent': (52, 152, 219), 'win_button': (70, 80, 100),
    'win_button_hover': (90, 100, 120),
    'browser_bg': (255, 255, 255), 'browser_bar': (240, 240, 240),
    'google_blue': (66, 133, 244), 'google_red': (219, 68, 55),
    'google_yellow': (244, 160, 0), 'google_green': (15, 157, 88),
    'bios_bg': (0, 30, 0), 'bios_text': (200, 200, 200), 'bios_highlight': (255, 255, 255),
}

font = font_small = font_ui = font_ui_bold = font_ui_large = None
font_google = font_clock_big = font_play = font_bios = font_bios_big = None

def create_fonts():
    global font, font_small, font_ui, font_ui_bold, font_ui_large, font_google
    global font_clock_big, font_play, font_bios, font_bios_big
    font = pygame.font.SysFont('consolas,couriernew,monospace', 18)
    font_small = pygame.font.SysFont('consolas,couriernew,monospace', 14)
    font_ui = pygame.font.SysFont('arial,segoeui', 16)
    font_ui_bold = pygame.font.SysFont('arial,segoeui', 16, bold=True)
    font_ui_large = pygame.font.SysFont('arial,segoeui', 28, bold=True)
    font_google = pygame.font.SysFont('arial,segoeui', 60, bold=True)
    font_clock_big = pygame.font.SysFont('arial', 60, bold=True)
    font_play = pygame.font.SysFont('arial', 30)
    font_bios = pygame.font.SysFont('consolas,couriernew,monospace', 16)
    font_bios_big = pygame.font.SysFont('consolas,couriernew,monospace', 22, bold=True)

create_fonts()

def hash_password(p):
    return hashlib.sha256(p.encode('utf-8')).hexdigest()

APP_STORE = {
    'calculator': {'name': 'Калькулятор', 'size': '2 МБ', 'desc': 'Простой калькулятор', 'icon': 'C'},
    'notepad': {'name': 'Блокнот', 'size': '1 МБ', 'desc': 'Записная книжка', 'icon': 'N'},
    'paint': {'name': 'Рисовалка', 'size': '3 МБ', 'desc': 'Рисуйте мышкой', 'icon': 'P'},
    'clock': {'name': 'Часы', 'size': '1 МБ', 'desc': 'Цифровые часы', 'icon': 'T'},
    'music': {'name': 'Плеер', 'size': '5 МБ', 'desc': 'Музыкальный плеер', 'icon': 'M'},
    'browser': {'name': 'Yonin Tor', 'size': '10 МБ', 'desc': 'Интернет-браузер', 'icon': 'W'},
    'files': {'name': 'Файлы', 'size': '2 МБ', 'desc': 'Файловый менеджер', 'icon': 'F'},
    'real_browser': {'name': 'Настоящий интернет', 'size': '0 МБ', 'desc': 'Открыть реальный Google в системном браузере', 'icon': 'X'},
}

# ============================================================
# РЕАЛИСТИЧНАЯ ВИРТУАЛЬНАЯ ФС
# ============================================================
class VirtualFS:
    def __init__(self):
        now = datetime.datetime.now()
        self.root = {
            'home': {
                'тип': 'dir', 'дата': now - datetime.timedelta(days=30), 'размер': 0,
                USERNAME: {
                    'тип': 'dir', 'дата': now - datetime.timedelta(days=30), 'размер': 0,
                    'Документы': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=20), 'размер': 0,
                        'резюме.txt': {
                            'тип': 'file', 'содержимое': "=== РЕЗЮМЕ ===\n\nИмя: " + USERNAME + "\nГород: Москва\n\nОпыт работы:\n- 2023-2025: Python-разработчик\n- 2021-2023: Системный администратор\n\nНавыки:\n- Python, Pygame\n- Linux, Bash\n- Git, Docker",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=5, hours=3), 'размер': 245
                        },
                        'заметки.txt': {
                            'тип': 'file', 'содержимое': "Мои заметки:\n\n1. Купить молоко\n2. Изучить Linux\n3. Написать свою ОС на Python\n4. Сделать иконку\n5. Установить приложения\n\n---\nВажное: не забыть про пароль root (00912322)",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=2, hours=8), 'размер': 178
                        },
                        'список_дел.txt': {
                            'тип': 'file', 'содержимое': "[ ] Сделать уборку\n[x] Написать ОС\n[ ] Купить продукты\n[x] Установить GoginOS\n[ ] Прочитать книгу\n[ ] Позвонить маме",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(hours=12), 'размер': 112
                        },
                        'Отчёты': {
                            'тип': 'dir', 'дата': now - datetime.timedelta(days=15), 'размер': 0,
                            'отчёт_январь.txt': {
                                'тип': 'file', 'содержимое': "ОТЧЁТ ЗА ЯНВАРЬ\n\nВыполнено задач: 24/30\nПотрачено часов: 156\nЭффективность: 80%\n\nВыводы: хороший месяц, но нужно больше времени на отдых.",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=14), 'размер': 156
                            },
                            'отчёт_февраль.txt': {
                                'тип': 'file', 'содержимое': "ОТЧЁТ ЗА ФЕВРАЛЬ\n\nВыполнено задач: 28/30\nПотрачено часов: 168\nЭффективность: 93%\n\nВыводы: отличный результат!",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=2), 'размер': 165
                            }
                        }
                    },
                    'Загрузки': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=10), 'размер': 0,
                        'gogin_installer.py': {
                            'тип': 'file', 'содержимое': "# Установщик GoginOS\n# Установите командой: python gogin_installer.py\n\nprint('Добро пожаловать в GoginOS!')",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=10, hours=2), 'размер': 128
                        },
                        'python_cheatsheet.txt': {
                            'тип': 'file', 'содержимое': "PYTHON ШПАРГАЛКА\n\nОсновы:\n  print('Hello')   - вывод\n  x = 5           - переменная\n  if x > 0:       - условие\n\nЦиклы:\n  for i in range(10):  - цикл\n  while x < 10:        - while\n\nФункции:\n  def hello():\n      print('Hi')",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=8), 'размер': 312
                        },
                        'photo_2025.png': {
                            'тип': 'file', 'содержимое': '[БИНАРНЫЙ ФАЙЛ PNG]\nНе читается как текст',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=3), 'размер': 2458624, 'бинарый': True
                        },
                        'архив.zip': {
                            'тип': 'file', 'содержимое': '[ZIP АРХИВ]\nСодержит 15 файлов',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=7), 'размер': 10485760, 'бинарый': True
                        }
                    },
                    'Изображения': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=25), 'размер': 0,
                        'screenshot_1.png': {
                            'тип': 'file', 'содержимое': '[ИЗОБРАЖЕНИЕ PNG 1920x1080]',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=5), 'размер': 524288, 'бинарый': True
                        },
                        'wallpaper.jpg': {
                            'тип': 'file', 'содержимое': '[ИЗОБРАЖЕНИЕ JPEG]',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=20), 'размер': 3145728, 'бинарый': True
                        },
                        'avatar.png': {
                            'тип': 'file', 'содержимое': '[ИЗОБРАЖЕНИЕ PNG 256x256]',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=15), 'размер': 65536, 'бинарый': True
                        }
                    },
                    'Музыка': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=18), 'размер': 0,
                        'gogin_theme.mp3': {
                            'тип': 'file', 'содержимое': '[MP3 АУДИО]\nДлительность: 3:42',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=15), 'размер': 5242880, 'бинарый': True
                        },
                        'playlist.txt': {
                            'тип': 'file', 'содержимое': "МОЙ ПЛЕЙЛИСТ\n\n1. Gogin Theme - 3:42\n2. Python Beats - 4:15\n3. Linux Sound - 3:28\n4. Coding Vibes - 5:01\n5. Terminal Dreams - 4:33",
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=10), 'размер': 198
                        }
                    },
                    'Видео': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=12), 'размер': 0,
                        'demo.mp4': {
                            'тип': 'file', 'содержимое': '[ВИДЕО MP4 1080p]\nДлительность: 5:23',
                            'владелец': USERNAME, 'дата': now - datetime.timedelta(days=8), 'размер': 157286400, 'бинарый': True
                        }
                    },
                    'проекты': {
                        'тип': 'dir', 'дата': now - datetime.timedelta(days=30), 'размер': 0,
                        'gogin_os': {
                            'тип': 'dir', 'дата': now - datetime.timedelta(days=25), 'размер': 0,
                            'main.py': {
                                'тип': 'file', 'содержимое': "import pygame\n\ndef main():\n    print('GoginOS запущена!')\n\nif __name__ == '__main__':\n    main()",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=20), 'размер': 156
                            },
                            'README.md': {
                                'тип': 'file', 'содержимое': "# GoginOS\n\nLinux-подобная ОС на Python.\n\n## Возможности\n- Терминал\n- Магазин приложений\n- sudo + BIOS\n- Yonin Tor",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=18), 'размер': 234
                            }
                        },
                        'web_site': {
                            'тип': 'dir', 'дата': now - datetime.timedelta(days=15), 'размер': 0,
                            'index.html': {
                                'тип': 'file', 'содержимое': "<!DOCTYPE html>\n<html>\n<head>\n  <title>Мой сайт</title>\n</head>\n<body>\n  <h1>Привет!</h1>\n</body>\n</html>",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=12), 'размер': 189
                            },
                            'style.css': {
                                'тип': 'file', 'содержимое': "body {\n    font-family: Arial;\n    background: #f0f0f0;\n}\n\nh1 { color: #3498db; }",
                                'владелец': USERNAME, 'дата': now - datetime.timedelta(days=12), 'размер': 112
                            }
                        }
                    },
                    'readme.txt': {
                        'тип': 'file', 'содержимое': "Добро пожаловать, " + USERNAME + "!\n\nЭто ваша домашняя директория в GoginOS.\nЗдесь вы можете создавать свои файлы и папки.\n\nОсновные команды:\n  help         - список команд\n  open <app>   - запустить приложение\n  install <app>- установить приложение\n  apps         - список приложений\n  google       - открыть настоящий Google\n\nsudo пароль: 00912322",
                        'владелец': USERNAME, 'дата': now - datetime.timedelta(days=1), 'размер': 358
                    }
                }
            },
            'root': {
                'тип': 'dir', 'дата': now - datetime.timedelta(days=60), 'размер': 0,
                'секрет.txt': {
                    'тип': 'file', 'содержимое': "ТОЛЬКО ДЛЯ ROOT\n\nЕсли ты это читаешь - значит ты вошёл как root.\n\nПароль: 00912322\n\nНе рассказывай никому!",
                    'владелец': 'root', 'права': 'root_only', 'дата': now - datetime.timedelta(days=45), 'размер': 128
                },
                'bios.log': {
                    'тип': 'file', 'содержимое': "[BIOS LOG]\n\n[OK] BIOS v5.3 initialized\n[OK] Memory test: 2048 MB passed\n[OK] Boot device: Virtual HDD\n[OK] Loading kernel...\n[OK] System booted successfully",
                    'владелец': 'root', 'права': 'root_only', 'дата': now - datetime.timedelta(hours=6), 'размер': 178
                }
            },
            'etc': {
                'тип': 'dir', 'дата': now - datetime.timedelta(days=60), 'размер': 0,
                'config.conf': {
                    'тип': 'file', 'содержимое': "[system]\nversion = 5.3\nname = GoginOS\nkernel = Python " + sys.version.split()[0] + "\n\n[user]\nname = " + USERNAME + "\nhome = /home/" + USERNAME,
                    'владелец': 'root', 'дата': now - datetime.timedelta(days=1), 'размер': 189
                },
                'hostname': {
                    'тип': 'file', 'содержимое': "gogin",
                    'владелец': 'root', 'дата': now - datetime.timedelta(days=60), 'размер': 5
                },
                'shadow': {
                    'тип': 'file', 'содержимое': "root:$6$xyz$00912322:19000:0:99999:7:::\n" + USERNAME + ":$6$abc$********:19000:0:99999:7:::",
                    'владелец': 'root', 'права': 'root_only', 'дата': now - datetime.timedelta(days=60), 'размер': 156
                },
                'passwd': {
                    'тип': 'file', 'содержимое': "root:x:0:0:root:/root:/bin/bash\n" + USERNAME + ":x:1000:1000:" + USERNAME + ":/home/" + USERNAME + ":/bin/bash",
                    'владелец': 'root', 'дата': now - datetime.timedelta(days=60), 'размер': 132
                }
            },
            'bin': {
                'тип': 'dir', 'дата': now - datetime.timedelta(days=60), 'размер': 0,
                'python': {'тип': 'file', 'содержимое': '[ИСПОЛНЯЕМЫЙ ФАЙЛ]', 'владелец': 'root', 'дата': now - datetime.timedelta(days=60), 'размер': 4194304, 'бинарый': True},
                'bash': {'тип': 'file', 'содержимое': '[ИСПОЛНЯЕМЫЙ ФАЙЛ]', 'владелец': 'root', 'дата': now - datetime.timedelta(days=60), 'размер': 2097152, 'бинарый': True},
                'ls': {'тип': 'file', 'содержимое': '[ИСПОЛНЯЕМЫЙ ФАЙЛ]', 'владелец': 'root', 'дата': now - datetime.timedelta(days=60), 'размер': 131072, 'бинарый': True}
            },
            'tmp': {'тип': 'dir', 'дата': now, 'размер': 0},
            'var': {
                'тип': 'dir', 'дата': now - datetime.timedelta(days=60), 'размер': 0,
                'log': {
                    'тип': 'dir', 'дата': now - datetime.timedelta(days=60), 'размер': 0,
                    'system.log': {
                        'тип': 'file', 'содержимое': "[SYSTEM LOG]\n\n" + now.strftime('%Y-%m-%d %H:%M:%S') + " [INFO] System started\n" + now.strftime('%Y-%m-%d %H:%M:%S') + " [INFO] User " + USERNAME + " logged in\n" + now.strftime('%Y-%m-%d %H:%M:%S') + " [INFO] GoginOS v5.3 running",
                        'владелец': 'root', 'дата': now, 'размер': 245
                    }
                }
            }
        }
        self.cwd = ['home', USERNAME]
    
    def get_current_dir(self):
        c = self.root
        for p in self.cwd:
            if p in c and isinstance(c[p], dict) and c[p].get('тип') == 'dir':
                c = c[p]
            else: return None
        return c
    
    def get_path_string(self):
        return '/' + '/'.join(self.cwd) if self.cwd else '/'
    
    def list_dir(self, parts):
        t = self.root
        for p in parts:
            if p in ('', '.'): continue
            if p == '..': continue
            if p in t and isinstance(t[p], dict) and t[p].get('тип') == 'dir':
                t = t[p]
            else: return None
        return t
    
    def resolve_path(self, path):
        if path.startswith('/'):
            parts = [p for p in path.split('/') if p]
        else:
            parts = self.cwd.copy()
            for p in path.split('/'):
                if p in ('', '.'): continue
                elif p == '..':
                    if parts: parts.pop()
                else: parts.append(p)
        return parts
    
    def mkdir(self, name):
        c = self.get_current_dir()
        if name in c: return False
        c[name] = {'тип': 'dir', 'дата': datetime.datetime.now(), 'размер': 0}
        return True
    
    def create_file(self, name, content='', owner=USERNAME):
        c = self.get_current_dir()
        c[name] = {
            'тип': 'file', 'содержимое': content, 'владелец': owner,
            'дата': datetime.datetime.now(), 'размер': len(content.encode('utf-8'))
        }
        return True
    
    def delete(self, name, is_root=False):
        c = self.get_current_dir()
        if name not in c: return False
        item = c[name]
        if item['тип'] == 'dir':
            subitems = [k for k in item if k not in ('тип', 'дата', 'размер')]
            if len(subitems) > 0: return False
        if item.get('владелец') == 'root' and not is_root: return 'no_permission'
        del c[name]; return True


class BIOS:
    def __init__(self):
        self.active = False
        self.menu_index = 0
        self.message = ""
        self.message_timer = 0
        self.system_info = {
            'BIOS Version': 'GoginBIOS v5.3', 'Build Date': '2025-01-15',
            'Processor': 'Python Virtual CPU @ 3.2 GHz', 'Memory': '2048 MB',
            'Boot Device': 'Virtual HDD (Python)', 'OS Installed': 'GoginOS v5.3',
            'User': USERNAME, 'Boot Count': str(CONFIG.get('boot_count', 0)),
            'Kernel': 'Python ' + sys.version.split()[0],
        }
        self.menu_items = [
            ('System Information', self.show_info), ('Boot Device Priority', self.show_boot),
            ('Memory Test', self.run_memtest), ('Reset Configuration', self.reset_config),
            ('Save & Exit', self.exit_bios), ('Exit Without Saving', self.exit_bios),
        ]
    def show_info(self): self.message = "System info shown above"; self.message_timer = 120
    def show_boot(self): self.message = "Boot: Virtual HDD -> GoginOS"; self.message_timer = 120
    def run_memtest(self): self.message = "Memory test: 2048 MB OK (passed)"; self.message_timer = 180
    def reset_config(self): self.message = "Config reset! (demo)"; self.message_timer = 120
    def exit_bios(self): self.active = False
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.active = False
            elif event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                _, action = self.menu_items[self.menu_index]; action()
            return True
        return False
    def draw(self, screen):
        if not self.active: return
        screen.fill(COLORS['bios_bg'])
        pygame.draw.rect(screen, COLORS['bios_text'], (10, 10, WIDTH - 20, HEIGHT - 20), 2)
        title = font_bios_big.render("GoginBIOS Setup Utility v5.3", True, COLORS['bios_highlight'])
        screen.blit(title, (30, 25))
        pygame.draw.line(screen, COLORS['bios_text'], (20, 65), (WIDTH - 20, 65), 1)
        screen.blit(font_bios.render("System Information", True, COLORS['bios_highlight']), (30, 85))
        pygame.draw.line(screen, COLORS['bios_text'], (25, 108), (WIDTH // 2 - 10, 108), 1)
        y = 120
        for k, v in self.system_info.items():
            screen.blit(font_bios.render(k + ":", True, COLORS['bios_text']), (40, y))
            screen.blit(font_bios.render(str(v), True, COLORS['bios_highlight']), (WIDTH // 2 - 150, y)); y += 24
        screen.blit(font_bios.render("Menu", True, COLORS['bios_highlight']), (WIDTH // 2 + 20, 85))
        pygame.draw.line(screen, COLORS['bios_text'], (WIDTH // 2 + 15, 108), (WIDTH - 20, 108), 1)
        y = 120
        for i, (name, _) in enumerate(self.menu_items):
            if i == self.menu_index:
                pygame.draw.rect(screen, (0, 100, 0), (WIDTH // 2 + 20, y - 2, WIDTH // 2 - 40, 24))
                color = COLORS['bios_highlight']; prefix = "> "
            else: color = COLORS['bios_text']; prefix = "  "
            screen.blit(font_bios.render(prefix + name, True, color), (WIDTH // 2 + 30, y)); y += 26
        if self.message_timer > 0:
            self.message_timer -= 1
            pygame.draw.rect(screen, (0, 80, 0), (30, HEIGHT - 100, WIDTH - 60, 28))
            screen.blit(font_bios.render(self.message, True, COLORS['bios_highlight']), (40, HEIGHT - 96))
        screen.blit(font_bios.render("Arrow Keys: Navigate | Enter: Select | ESC: Exit", True, COLORS['bios_text']), (30, HEIGHT - 55))
        logo = font_bios.render("(C) 2025 GoginOS Project", True, COLORS['bios_text'])
        screen.blit(logo, (WIDTH - logo.get_width() - 30, HEIGHT - 55))


class AppWindow:
    def __init__(self, app_id, title, x, y, width, height):
        self.app_id = app_id; self.title = title
        self.x = x; self.y = y; self.width = width; self.height = height
        self.is_dragging = False; self.drag_off_x = 0; self.drag_off_y = 0
        self.close_btn = pygame.Rect(x + width - 30, y + 6, 22, 22)
        self.min_btn = pygame.Rect(x + width - 58, y + 6, 22, 22)
        self.data = {}; self.on_open()
    def on_open(self): pass
    def update_rects(self):
        self.close_btn = pygame.Rect(self.x + self.width - 30, self.y + 6, 22, 22)
        self.min_btn = pygame.Rect(self.x + self.width - 58, self.y + 6, 22, 22)
    def handle_event(self, event): return False
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (self.x+4, self.y+4, self.width, self.height), border_radius=8)
        pygame.draw.rect(screen, COLORS['win_bg'], (self.x, self.y, self.width, self.height), border_radius=8)
        pygame.draw.rect(screen, COLORS['win_border'], (self.x, self.y, self.width, self.height), 2, border_radius=8)
        pygame.draw.rect(screen, COLORS['win_title'], (self.x, self.y, self.width, 34), border_top_left_radius=8, border_top_right_radius=8)
        screen.blit(font_ui_bold.render(self.title, True, COLORS['win_text']), (self.x + 12, self.y + 8))
        pygame.draw.rect(screen, (231,76,60), self.close_btn, border_radius=4)
        screen.blit(font_small.render("X", True, (255,255,255)), (self.close_btn.x+7, self.close_btn.y+4))
        pygame.draw.rect(screen, (241,196,15), self.min_btn, border_radius=4)
        screen.blit(font_small.render("-", True, (255,255,255)), (self.min_btn.x+8, self.min_btn.y+2))
        self.draw_content(screen)
    def draw_content(self, screen): pass


class CalculatorApp(AppWindow):
    def on_open(self): self.data['display'] = "0"; self.data['buttons'] = []
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for (r, l) in self.data['buttons']:
                if r.collidepoint(event.pos): self.press(l); return True
        return False
    def press(self, l):
        d = self.data['display']
        if l == 'C': self.data['display'] = "0"
        elif l == '=':
            try: self.data['display'] = str(eval(d))
            except: self.data['display'] = "Err"
        elif l == '<': self.data['display'] = d[:-1] if len(d) > 1 else "0"
        else:
            if d == "0" and l not in ('+','-','*','/','.'): self.data['display'] = l
            else: self.data['display'] = d + l
    def draw_content(self, screen):
        dr = pygame.Rect(self.x+15, self.y+50, self.width-30, 50)
        pygame.draw.rect(screen, (20,25,35), dr, border_radius=5)
        pygame.draw.rect(screen, COLORS['win_accent'], dr, 1, border_radius=5)
        ds = font_ui_large.render(self.data['display'][-15:], True, (255,255,255))
        screen.blit(ds, (dr.right - ds.get_width() - 15, dr.y + 10))
        labels = [['C','<','/','*'],['7','8','9','-'],['4','5','6','+'],['1','2','3','='],['0','.','','']]
        self.data['buttons'] = []
        bw, bh, gap = 60, 45, 8
        sx, sy = self.x + 15, self.y + 115
        for ri, row in enumerate(labels):
            for ci, l in enumerate(row):
                if not l: continue
                bx, by = sx + ci*(bw+gap), sy + ri*(bh+gap)
                rect = pygame.Rect(bx, by, bw, bh)
                hover = rect.collidepoint(pygame.mouse.get_pos())
                if l == '=': c = COLORS['win_accent'] if not hover else (70,170,230)
                elif l in ('C','<'): c = (231,76,60) if not hover else (250,100,90)
                elif l in ('+','-','*','/'): c = (241,196,15) if not hover else (255,220,60)
                else: c = COLORS['win_button'] if not hover else COLORS['win_button_hover']
                pygame.draw.rect(screen, c, rect, border_radius=5)
                tc = font_ui_bold.render(l, True, (255,255,255))
                screen.blit(tc, (rect.centerx - tc.get_width()//2, rect.centery - tc.get_height()//2))
                self.data['buttons'].append((rect, l))


class NotepadApp(AppWindow):
    def on_open(self): self.data['text'] = "Привет!"
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: self.data['text'] = self.data['text'][:-1]
            elif event.key == pygame.K_RETURN: self.data['text'] += '\n'
            elif event.unicode and event.unicode.isprintable(): self.data['text'] += event.unicode
            return True
        return False
    def draw_content(self, screen):
        tr = pygame.Rect(self.x+10, self.y+45, self.width-20, self.height-55)
        pygame.draw.rect(screen, (20,25,35), tr, border_radius=5)
        wrapped = []
        for line in self.data['text'].split('\n'):
            while len(line) > 50: wrapped.append(line[:50]); line = line[50:]
            wrapped.append(line)
        y = tr.y + 8
        for line in wrapped[-25:]:
            screen.blit(font_small.render(line, True, (230,230,230)), (tr.x+8, y)); y += 20
        pygame.draw.rect(screen, COLORS['win_accent'], (tr.x+8, y, 8, 16))


class PaintApp(AppWindow):
    def on_open(self):
        self.data['canvas'] = pygame.Surface((self.width-20, self.height-60))
        self.data['canvas'].fill((255,255,255))
        self.data['drawing'] = False
        self.data['color'] = (0,0,0)
        self.data['colors'] = [(0,0,0),(255,0,0),(0,150,0),(0,0,255),(255,200,0),(150,0,150)]
    def handle_event(self, event):
        cr = pygame.Rect(self.x+10, self.y+50, self.width-20, self.height-60)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, c in enumerate(self.data['colors']):
                br = pygame.Rect(self.x+10+i*30, self.y+40, 25, 22)
                if br.collidepoint(mx, my): self.data['color'] = c; return True
            if cr.collidepoint(mx, my):
                self.data['drawing'] = True
                pygame.draw.circle(self.data['canvas'], self.data['color'], (mx-cr.x, my-cr.y), 3); return True
        elif event.type == pygame.MOUSEBUTTONUP: self.data['drawing'] = False
        elif event.type == pygame.MOUSEMOTION and self.data['drawing']:
            mx, my = event.pos
            if cr.collidepoint(mx, my):
                pygame.draw.circle(self.data['canvas'], self.data['color'], (mx-cr.x, my-cr.y), 3); return True
        return False
    def draw_content(self, screen):
        for i, c in enumerate(self.data['colors']):
            br = pygame.Rect(self.x+10+i*30, self.y+40, 25, 22)
            pygame.draw.rect(screen, c, br, border_radius=3)
            if self.data['color'] == c: pygame.draw.rect(screen, (255,255,255), br, 2, border_radius=3)
        screen.blit(self.data['canvas'], (self.x+10, self.y+50))


class ClockApp(AppWindow):
    def draw_content(self, screen):
        now = datetime.datetime.now()
        ts = font_clock_big.render(now.strftime("%H:%M:%S"), True, COLORS['win_accent'])
        screen.blit(ts, (self.x + self.width//2 - ts.get_width()//2, self.y + 60))
        ds = font_ui.render(now.strftime("%d %B %Y"), True, COLORS['win_text'])
        screen.blit(ds, (self.x + self.width//2 - ds.get_width()//2, self.y + 140))
        cx, cy, r = self.x + self.width//2, self.y + self.height - 90, 60
        pygame.draw.circle(screen, (20,25,35), (cx,cy), r)
        pygame.draw.circle(screen, COLORS['win_accent'], (cx,cy), r, 2)
        for i in range(12):
            a = math.radians(i*30)
            pygame.draw.line(screen, COLORS['win_text'], (cx+(r-8)*math.sin(a), cy-(r-8)*math.cos(a)), (cx+(r-2)*math.sin(a), cy-(r-2)*math.cos(a)), 2)
        ha = math.radians((now.hour%12)*30 + now.minute*0.5)
        pygame.draw.line(screen, (255,255,255), (cx,cy), (cx+r*0.5*math.sin(ha), cy-r*0.5*math.cos(ha)), 4)
        ma = math.radians(now.minute*6)
        pygame.draw.line(screen, (200,200,200), (cx,cy), (cx+r*0.7*math.sin(ma), cy-r*0.7*math.cos(ma)), 3)
        sa = math.radians(now.second*6)
        pygame.draw.line(screen, (231,76,60), (cx,cy), (cx+r*0.8*math.sin(sa), cy-r*0.8*math.cos(sa)), 2)
        pygame.draw.circle(screen, (255,255,255), (cx,cy), 4)


# ============================================================
# РЕАЛИСТИЧНЫЙ ФАЙЛОВЫЙ МЕНЕДЖЕР
# ============================================================
class FilesApp(AppWindow):
    def on_open(self):
        self.data.update({
            'fs': None, 'selected': None, 'path_editing': False,
            'path_text': '', 'message': '', 'message_timer': 0, 'scroll': 0,
            'last_click_time': 0, 'last_click_name': None,
            'viewer_file': None, 'viewer_content': ''
        })
    
    def format_size(self, size):
        if size is None: return '--'
        if size < 1024: return str(size) + ' Б'
        elif size < 1024*1024: return f'{size/1024:.1f} КБ'
        elif size < 1024*1024*1024: return f'{size/(1024*1024):.1f} МБ'
        else: return f'{size/(1024*1024*1024):.2f} ГБ'
    
    def format_date(self, dt):
        if dt is None: return '--'
        now = datetime.datetime.now()
        diff = (now - dt).total_seconds()
        if diff < 60: return 'только что'
        elif diff < 3600: return f'{int(diff/60)} мин назад'
        elif diff < 86400: return f'{int(diff/3600)} ч назад'
        elif diff < 172800: return 'вчера'
        elif diff < 604800: return f'{int(diff/86400)} дн назад'
        else: return dt.strftime('%d.%m.%Y %H:%M')
    
    def get_icon(self, name, info):
        if info.get('тип') == 'dir': return 'D'
        n = name.lower()
        if n.endswith(('.txt','.md','.log','.conf','.ini')): return 'T'
        elif n.endswith(('.py','.js','.html','.css','.sh','.bat')): return '<>'
        elif n.endswith(('.png','.jpg','.jpeg','.gif','.bmp')): return 'I'
        elif n.endswith(('.mp3','.wav','.ogg','.flac')): return 'S'
        elif n.endswith(('.mp4','.avi','.mkv','.mov')): return 'V'
        elif n.endswith(('.zip','.rar','.7z','.tar','.gz')): return 'Z'
        else: return 'F'
    
    def get_color(self, info):
        if info.get('тип') == 'dir': return (255, 200, 60)
        if info.get('бинарый'): return (180, 180, 180)
        return (100, 200, 255)
    
    def sort_items(self, items):
        folders = [(n, i) for n, i in items if i.get('тип') == 'dir']
        files = [(n, i) for n, i in items if i.get('тип') != 'dir']
        folders.sort(key=lambda x: x[0].lower())
        files.sort(key=lambda x: x[0].lower())
        return folders + files
    
    def get_visible_items(self):
        fs = self.data['fs']
        if not fs: return []
        current = fs.get_current_dir()
        if not current: return []
        items = [(n, i) for n, i in current.items() if n not in ('тип','дата','размер')]
        return self.sort_items(items)
    
    def open_file(self, name, info):
        if info.get('бинарый'):
            self.data['message'] = f"'{name}': бинарный файл, нельзя открыть как текст"
            self.data['message_timer'] = 180
            return
        self.data['viewer_file'] = name
        self.data['viewer_content'] = info.get('содержимое', '(пусто)')
        self.data['message'] = f"Открыт файл: {name}"
        self.data['message_timer'] = 180
    
    def handle_event(self, event):
        if not self.data['fs']: return False
        fs = self.data['fs']
        
        if self.data.get('viewer_file'):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.data['viewer_file'] = None
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.data['viewer_file'] = None
                return True
            return True
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            if pygame.Rect(self.x + 10, self.y + 42, 32, 26).collidepoint(mx, my):
                if len(fs.cwd) > 0: fs.cwd.pop()
                self.data['selected'] = None; self.data['scroll'] = 0
                return True
            if pygame.Rect(self.x + 46, self.y + 42, 32, 26).collidepoint(mx, my):
                fs.cwd = ['home', USERNAME]
                self.data['selected'] = None; self.data['scroll'] = 0
                return True
            path_rect = pygame.Rect(self.x + 84, self.y + 42, self.width - 94, 26)
            if path_rect.collidepoint(mx, my):
                if not self.data['path_editing']:
                    self.data['path_editing'] = True
                    self.data['path_text'] = fs.get_path_string()
                return True
            elif self.data['path_editing']:
                self.apply_path_edit()
            
            list_start = self.y + 106
            item_h = 28
            if my > list_start:
                idx = (my - list_start) // item_h + self.data['scroll']
                visible = self.get_visible_items()
                if 0 <= idx < len(visible):
                    name, info = visible[idx]
                    now = datetime.datetime.now().timestamp()
                    if (self.data['last_click_name'] == name and 
                        now - self.data['last_click_time'] < 0.4):
                        if info.get('тип') == 'dir':
                            fs.cwd.append(name)
                            self.data['selected'] = None; self.data['scroll'] = 0
                        else:
                            self.open_file(name, info)
                        self.data['last_click_name'] = None
                    else:
                        self.data['selected'] = name
                        self.data['last_click_name'] = name
                        self.data['last_click_time'] = now
                    return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
            visible = self.get_visible_items()
            max_scroll = max(0, len(visible) - 15)
            if event.button == 4: self.data['scroll'] = max(0, self.data['scroll'] - 2)
            else: self.data['scroll'] = min(max_scroll, self.data['scroll'] + 2)
            return True
        
        elif event.type == pygame.KEYDOWN:
            if self.data['path_editing']:
                if event.key == pygame.K_RETURN: self.apply_path_edit()
                elif event.key == pygame.K_ESCAPE: self.data['path_editing'] = False
                elif event.key == pygame.K_BACKSPACE: self.data['path_text'] = self.data['path_text'][:-1]
                elif event.unicode and event.unicode.isprintable(): self.data['path_text'] += event.unicode
                return True
            
            visible = self.get_visible_items()
            if not visible: return False
            
            cur_idx = -1
            if self.data['selected']:
                for i, (n, _) in enumerate(visible):
                    if n == self.data['selected']: cur_idx = i; break
            
            if event.key == pygame.K_DOWN:
                new_idx = min(len(visible)-1, cur_idx+1)
                self.data['selected'] = visible[new_idx][0]
                if new_idx >= self.data['scroll'] + 15: self.data['scroll'] = new_idx - 14
                return True
            elif event.key == pygame.K_UP:
                new_idx = max(0, cur_idx-1)
                self.data['selected'] = visible[new_idx][0]
                if new_idx < self.data['scroll']: self.data['scroll'] = new_idx
                return True
            elif event.key == pygame.K_RETURN and self.data['selected']:
                for n, info in visible:
                    if n == self.data['selected']:
                        if info.get('тип') == 'dir':
                            fs.cwd.append(n)
                            self.data['selected'] = None; self.data['scroll'] = 0
                        else:
                            self.open_file(n, info)
                        return True
            elif event.key == pygame.K_BACKSPACE:
                if len(fs.cwd) > 0: fs.cwd.pop()
                self.data['selected'] = None; self.data['scroll'] = 0
                return True
            elif event.key == pygame.K_DELETE and self.data['selected']:
                current = fs.get_current_dir()
                if self.data['selected'] in current:
                    name = self.data['selected']; item = current[name]
                    if item.get('владелец') == 'root':
                        self.data['message'] = f"'{name}': недостаточно прав"
                        self.data['message_timer'] = 150
                    else:
                        del current[name]
                        self.data['message'] = f"Удалено: {name}"
                        self.data['message_timer'] = 150
                        self.data['selected'] = None
                return True
        return False
    
    def apply_path_edit(self):
        fs = self.data['fs']
        path = self.data['path_text'].strip()
        self.data['path_editing'] = False
        if not path: return
        new_parts = fs.resolve_path(path)
        if fs.list_dir(new_parts) is not None:
            fs.cwd = new_parts
            self.data['selected'] = None; self.data['scroll'] = 0
        else:
            self.data['message'] = f"Путь не найден: {path}"
            self.data['message_timer'] = 150
    
    def draw_content(self, screen):
        fs = self.data['fs']
        if not fs: return
        
        if self.data.get('viewer_file'):
            self.draw_viewer(screen)
            return
        
        current = fs.get_current_dir()
        if not current: return
        
        pygame.draw.rect(screen, (25, 30, 42), (self.x+5, self.y+38, self.width-10, 34))
        pygame.draw.line(screen, (50, 60, 80), (self.x+5, self.y+72), (self.x+self.width-5, self.y+72), 1)
        
        mx, my = pygame.mouse.get_pos()
        
        back_btn = pygame.Rect(self.x + 10, self.y + 42, 32, 26)
        hover = back_btn.collidepoint(mx, my)
        pygame.draw.rect(screen, (60,70,95) if not hover else (80,95,125), back_btn, border_radius=4)
        pygame.draw.rect(screen, (100,120,150), back_btn, 1, border_radius=4)
        screen.blit(font_ui_bold.render("<-", True, (220,230,255)), (back_btn.x+6, back_btn.y+5))
        
        home_btn = pygame.Rect(self.x + 46, self.y + 42, 32, 26)
        hover = home_btn.collidepoint(mx, my)
        pygame.draw.rect(screen, (60,70,95) if not hover else (80,95,125), home_btn, border_radius=4)
        pygame.draw.rect(screen, (100,120,150), home_btn, 1, border_radius=4)
        screen.blit(font_ui_bold.render("H", True, (220,230,255)), (home_btn.x+11, home_btn.y+4))
        
        path_rect = pygame.Rect(self.x + 84, self.y + 42, self.width - 94, 26)
        pygame.draw.rect(screen, (15,20,30), path_rect, border_radius=4)
        bc = COLORS['win_accent'] if self.data['path_editing'] else (60,70,90)
        pygame.draw.rect(screen, bc, path_rect, 1, border_radius=4)
        
        if self.data['path_editing']:
            ptext = self.data['path_text']
            if int(datetime.datetime.now().timestamp()*2) % 2 == 0: ptext += "|"
        else:
            ptext = fs.get_path_string()
            hp = '/home/' + USERNAME
            if ptext.startswith(hp): ptext = '~' + ptext[len(hp):]
        
        screen.blit(font_ui.render(ptext, True, (200,220,255)), (path_rect.x+8, path_rect.y+5))
        
        header_y = self.y + 80
        pygame.draw.rect(screen, (35, 42, 55), (self.x+5, header_y, self.width-10, 26))
        pygame.draw.line(screen, (60,70,90), (self.x+5, header_y+26), (self.x+self.width-5, header_y+26), 1)
        
        screen.blit(font_ui_bold.render("Имя", True, (180,200,230)), (self.x+45, header_y+5))
        screen.blit(font_ui_bold.render("Размер", True, (180,200,230)), (self.x+self.width-240, header_y+5))
        screen.blit(font_ui_bold.render("Изменён", True, (180,200,230)), (self.x+self.width-155, header_y+5))
        screen.blit(font_ui_bold.render("Владелец", True, (180,200,230)), (self.x+self.width-75, header_y+5))
        
        list_start = self.y + 106
        item_h = 28
        visible = self.get_visible_items()
        scroll = self.data['scroll']
        max_visible = (self.height - (list_start - self.y) - 40) // item_h
        
        if not visible:
            screen.blit(font_ui.render("(пусто)", True, (120,140,170)), (self.x+45, list_start+15))
            self.draw_status_bar(screen, fs)
            return
        
        for i in range(scroll, min(len(visible), scroll + max_visible)):
            name, info = visible[i]
            item_y = list_start + (i - scroll) * item_h
            
            is_selected = self.data['selected'] == name
            is_hover = (self.x+5 <= mx <= self.x+self.width-5 and item_y <= my <= item_y+item_h)
            
            if is_selected:
                pygame.draw.rect(screen, (52, 100, 180), (self.x+5, item_y, self.width-10, item_h))
            elif is_hover:
                pygame.draw.rect(screen, (45, 55, 75), (self.x+5, item_y, self.width-10, item_h))
            
            icon = self.get_icon(name, info)
            icon_color = self.get_color(info)
            icon_rect = pygame.Rect(self.x+12, item_y+4, 20, 20)
            pygame.draw.rect(screen, icon_color, icon_rect, border_radius=3)
            icon_font = pygame.font.SysFont('arial,segoeui', 11, bold=True)
            itxt = icon_font.render(icon, True, (20,25,35))
            screen.blit(itxt, (icon_rect.centerx - itxt.get_width()//2, icon_rect.centery - itxt.get_height()//2))
            
            display_name = name
            if len(display_name) > 40: display_name = display_name[:37] + "..."
            name_color = (255,255,255) if is_selected else (220,230,255)
            screen.blit(font_ui.render(display_name, True, name_color), (self.x+42, item_y+5))
            
            size_str = "--" if info.get('тип') == 'dir' else self.format_size(info.get('размер', 0))
            screen.blit(font_ui.render(size_str, True, (180,200,220)), (self.x+self.width-240, item_y+5))
            
            date_str = self.format_date(info.get('дата'))
            screen.blit(font_ui.render(date_str, True, (180,200,220)), (self.x+self.width-155, item_y+5))
            
            owner = info.get('владелец', USERNAME)
            owner_color = (255,180,180) if owner == 'root' else (180,220,255)
            screen.blit(font_ui.render(owner, True, owner_color), (self.x+self.width-75, item_y+5))
        
        if len(visible) > max_visible:
            track = pygame.Rect(self.x+self.width-8, list_start, 4, max_visible*item_h)
            pygame.draw.rect(screen, (40,50,65), track)
            ratio = max_visible / len(visible)
            thumb_h = max(20, int(track.height * ratio))
            thumb_y = track.y + int((track.height - thumb_h) * (scroll / max(1, len(visible)-max_visible)))
            pygame.draw.rect(screen, (100,130,180), (track.x, thumb_y, track.width, thumb_h), border_radius=2)
        
        self.draw_status_bar(screen, fs)
        
        if self.data['message_timer'] > 0:
            self.data['message_timer'] -= 1
            msg = font_ui_bold.render(self.data['message'], True, (255,255,255))
            mr = pygame.Rect(0,0,msg.get_width()+30,36)
            mr.centerx = self.x + self.width//2
            mr.bottom = self.y + self.height - 10
            pygame.draw.rect(screen, COLORS['win_accent'], mr, border_radius=6)
            screen.blit(msg, (mr.x+15, mr.y+9))
    
    def draw_status_bar(self, screen, fs):
        y = self.y + self.height - 32
        pygame.draw.rect(screen, (20, 25, 35), (self.x+5, y, self.width-10, 27))
        pygame.draw.line(screen, (60,70,90), (self.x+5, y), (self.x+self.width-5, y), 1)
        
        visible = self.get_visible_items()
        folders = sum(1 for _, i in visible if i.get('тип') == 'dir')
        files = len(visible) - folders
        total_size = sum(i.get('размер', 0) for _, i in visible if i.get('тип') == 'file')
        
        stat = f"Элементов: {len(visible)}  |  Папок: {folders}  |  Файлов: {files}  |  Размер: {self.format_size(total_size)}"
        screen.blit(font_ui.render(stat, True, (140,160,190)), (self.x+15, y+5))
        
        hint = "Enter - открыть  |  Delete - удалить  |  Backspace - назад"
        hw = font_ui.size(hint)[0]
        screen.blit(font_ui.render(hint, True, (100,120,150)), (self.x+self.width-hw-15, y+5))
    
    def draw_viewer(self, screen):
        ov = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        screen.blit(ov, (self.x, self.y))
        
        vw, vh = min(600, self.width-80), min(450, self.height-80)
        vx = self.x + (self.width - vw)//2
        vy = self.y + (self.height - vh)//2
        
        pygame.draw.rect(screen, (25, 30, 42), (vx, vy, vw, vh), border_radius=8)
        pygame.draw.rect(screen, COLORS['win_accent'], (vx, vy, vw, vh), 2, border_radius=8)
        pygame.draw.rect(screen, COLORS['win_title'], (vx, vy, vw, 34), border_top_left_radius=8, border_top_right_radius=8)
        
        screen.blit(font_ui_bold.render("Просмотр: " + self.data['viewer_file'], True, (255,255,255)), (vx+12, vy+8))
        
        pygame.draw.rect(screen, (231,76,60), (vx+vw-30, vy+6, 22, 22), border_radius=4)
        screen.blit(font_small.render("X", True, (255,255,255)), (vx+vw-23, vy+10))
        
        content_rect = pygame.Rect(vx+10, vy+45, vw-20, vh-75)
        pygame.draw.rect(screen, (12, 18, 28), content_rect, border_radius=4)
        
        lines = self.data['viewer_content'].split('\n')
        y = content_rect.y + 8
        max_chars = (content_rect.width - 20) // 10
        for line in lines[:18]:
            if len(line) > max_chars: line = line[:max_chars-3] + "..."
            screen.blit(font_small.render(line, True, (200, 230, 255)), (content_rect.x+8, y))
            y += 20
        
        hint = "Нажмите ESC или кликните для закрытия"
        hw = font_ui.size(hint)[0]
        screen.blit(font_ui.render(hint, True, (140,160,190)), (vx+vw//2 - hw//2, vy+vh-25))


class MusicApp(AppWindow):
    def on_open(self):
        self.data['playing'] = False; self.data['track'] = 0
        self.data['tracks'] = ["Track 1 - Gogin Theme","Track 2 - Python Beats","Track 3 - Linux Sound"]
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pb = pygame.Rect(self.x+self.width//2-30, self.y+self.height-80, 60, 60)
            if pb.collidepoint(event.pos): self.data['playing'] = not self.data['playing']; return True
        return False
    def draw_content(self, screen):
        t = self.data['tracks'][self.data['track']]
        ts = font_ui_large.render(t, True, COLORS['win_accent'])
        screen.blit(ts, (self.x+self.width//2-ts.get_width()//2, self.y+80))
        bar = pygame.Rect(self.x+30, self.y+150, self.width-60, 8)
        pygame.draw.rect(screen, (60,70,90), bar, border_radius=4)
        if self.data['playing']: pygame.draw.rect(screen, COLORS['win_accent'], (bar.x, bar.y, bar.width*0.4, bar.height), border_radius=4)
        pb = pygame.Rect(self.x+self.width//2-30, self.y+self.height-80, 60, 60)
        hover = pb.collidepoint(pygame.mouse.get_pos())
        pygame.draw.circle(screen, COLORS['win_accent'] if not hover else (70,170,230), pb.center, 30)
        sym = font_play.render("II" if self.data['playing'] else ">", True, (255,255,255))
        screen.blit(sym, (pb.centerx-sym.get_width()//2, pb.centery-sym.get_height()//2))


class YoninTorApp(AppWindow):
    def on_open(self):
        self.data.update({'search':"", 'results':[], 'view':'google', 'search_input_active':False,
            'installed_apps':set(), 'message':"", 'message_timer':0, 'install_buttons':[], 'on_app_installed':None})
    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(self.x+10, self.y+45, 30, 28).collidepoint(mx, my):
                if self.data['view'] != 'google': self.data['view'] = 'google'
                return True
            ir = pygame.Rect(self.x+50, self.y+45, self.width-120, 28)
            if ir.collidepoint(mx, my): self.data['search_input_active'] = True; return True
            else: self.data['search_input_active'] = False
            if pygame.Rect(self.x+self.width-60, self.y+45, 50, 28).collidepoint(mx, my): self.do_search(); return True
            if self.data['view'] == 'google':
                sb = pygame.Rect(self.x+self.width//2-200, self.y+310, 400, 55)
                if sb.collidepoint(mx, my): self.open_real_google(); return True
                stb = pygame.Rect(self.x+self.width//2-120, self.y+400, 240, 45)
                if stb.collidepoint(mx, my): self.data['view'] = 'app_store'; return True
            if self.data['view'] == 'app_store':
                for r, aid in self.data['install_buttons']:
                    if r.collidepoint(mx, my):
                        if aid == 'real_browser': self.open_real_google()
                        else: self.install_app(aid)
                        return True
        elif event.type == pygame.KEYDOWN and self.data['search_input_active']:
            if event.key == pygame.K_RETURN:
                q = self.data['search'].strip().lower()
                if q in ('google.com','google','гугл','www.google.com'):
                    self.open_real_google(); self.data['search'] = ""
                else: self.do_search()
            elif event.key == pygame.K_BACKSPACE: self.data['search'] = self.data['search'][:-1]
            elif event.unicode and event.unicode.isprintable(): self.data['search'] += event.unicode
            return True
        return False
    def open_real_google(self):
        try:
            webbrowser.open("https://www.google.com")
            self.data['message'] = "Открыт настоящий Google!"
            self.data['message_timer'] = 180
        except Exception as e:
            self.data['message'] = "Ошибка: " + str(e); self.data['message_timer'] = 180
    def do_search(self):
        q = self.data['search'].strip().lower()
        self.data['view'] = 'results'; self.data['results'] = []
        for aid, info in APP_STORE.items():
            if q in aid or q in info['name'].lower() or q in info['desc'].lower():
                self.data['results'].append({'title': info['name'] + ' - нажмите для установки',
                    'url': 'gogin.os/store/' + aid, 'desc': info['desc'] + ' ' + info['size'], 'app_id': aid})
        self.data['results'].append({'title': 'Открыть настоящий Google >>', 'url': 'https://www.google.com',
            'desc': 'Реальный поиск в системном браузере', 'real_url': 'https://www.google.com'})
    def install_app(self, aid):
        if aid in self.data['installed_apps']: self.data['message'] = "Уже установлено"
        else:
            self.data['installed_apps'].add(aid); self.data['message'] = "Установлено: " + APP_STORE[aid]['name']
            if self.data['on_app_installed']: self.data['on_app_installed'](aid)
        self.data['message_timer'] = 120
    def draw_content(self, screen):
        pygame.draw.rect(screen, COLORS['browser_bar'], (self.x+5, self.y+40, self.width-10, 40))
        pygame.draw.rect(screen, (220,220,220), (self.x+10, self.y+45, 30, 28), border_radius=4)
        screen.blit(font_ui_bold.render("<", True, (60,60,60)), (self.x+18, self.y+49))
        ir = pygame.Rect(self.x+50, self.y+45, self.width-120, 28)
        pygame.draw.rect(screen, (255,255,255), ir, border_radius=4)
        bc = COLORS['google_blue'] if self.data['search_input_active'] else (200,200,200)
        pygame.draw.rect(screen, bc, ir, 2, border_radius=4)
        txt = self.data['search'] or "Поиск или google.com..."
        tc = (40,40,40) if self.data['search'] else (150,150,150)
        ss = font_ui.render(txt, True, tc); screen.blit(ss, (ir.x+8, ir.y+6))
        if self.data['search_input_active'] and int(datetime.datetime.now().timestamp()*2)%2==0:
            cx = ir.x + 8 + ss.get_width() + 2
            pygame.draw.line(screen, (40,40,40), (cx, ir.y+5), (cx, ir.y+22), 2)
        gb = pygame.Rect(self.x+self.width-60, self.y+45, 50, 28)
        pygame.draw.rect(screen, COLORS['google_blue'], gb, border_radius=4)
        screen.blit(font_ui_bold.render("Go", True, (255,255,255)), (gb.x+14, gb.y+5))
        cy = self.y + 90
        pr = pygame.Rect(self.x+5, cy, self.width-10, self.height-100)
        pygame.draw.rect(screen, COLORS['browser_bg'], pr)
        old = screen.get_clip(); screen.set_clip(pr)
        if self.data['view'] == 'google': self.draw_google(screen, pr)
        elif self.data['view'] == 'app_store': self.draw_store(screen, pr)
        else: self.draw_results(screen, pr)
        screen.set_clip(old)
        if self.data['message_timer'] > 0:
            self.data['message_timer'] -= 1
            ms = font_ui_bold.render(self.data['message'], True, (255,255,255))
            mr = pygame.Rect(0,0,ms.get_width()+30,40); mr.centerx = self.x+self.width//2; mr.y = self.y+self.height-60
            pygame.draw.rect(screen, COLORS['google_green'], mr, border_radius=8)
            screen.blit(ms, (mr.x+15, mr.y+10))
    def draw_google(self, screen, r):
        cx, cy = r.centerx, r.y+60
        colors = [COLORS['google_blue'],COLORS['google_red'],COLORS['google_yellow'],COLORS['google_blue'],COLORS['google_green'],COLORS['google_red']]
        total_w = 0; surfs = []
        for i, ch in enumerate("Google"):
            s = font_google.render(ch, True, colors[i]); surfs.append(s); total_w += s.get_width()
        x = cx - total_w//2
        for s in surfs: screen.blit(s, (x, cy)); x += s.get_width()
        hint = font_ui.render("Или нажмите на кнопку ниже, чтобы открыть настоящий поисковик", True, (120,120,120))
        screen.blit(hint, (cx - hint.get_width()//2, cy + 75))
        real_btn = pygame.Rect(cx - 200, cy + 110, 400, 55)
        hover = real_btn.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, COLORS['google_blue'] if not hover else (90,160,255), real_btn, border_radius=10)
        pygame.draw.rect(screen, (50,100,200), real_btn, 3, border_radius=10)
        rt = font_ui_bold.render("ОТКРЫТЬ НАСТОЯЩИЙ GOOGLE", True, (255,255,255))
        screen.blit(rt, (real_btn.centerx - rt.get_width()//2, real_btn.centery - rt.get_height()//2))
        sub = font_ui.render("Откроется в вашем системном браузере", True, (100,100,100))
        screen.blit(sub, (cx - sub.get_width()//2, real_btn.bottom + 8))
        store_btn = pygame.Rect(cx - 120, real_btn.bottom + 45, 240, 45)
        hover = store_btn.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (100,100,100) if not hover else (130,130,130), store_btn, border_radius=8)
        st = font_ui_bold.render("Магазин приложений", True, (255,255,255))
        screen.blit(st, (store_btn.centerx - st.get_width()//2, store_btn.centery - st.get_height()//2))
    def draw_results(self, screen, r):
        y = r.y + 25
        for res in self.data['results']:
            screen.blit(font_ui.render(res['url'], True, COLORS['google_green']), (r.x+25, y))
            color = (200, 40, 40) if 'real_url' in res else (26,13,171)
            screen.blit(font_ui_bold.render(res['title'][:70], True, color), (r.x+25, y+22))
            screen.blit(font_ui.render(res['desc'][:90], True, (80,80,80)), (r.x+25, y+44))
            y += 75
            if y > r.bottom - 30: break
    def draw_store(self, screen, r):
        h = font_ui_large.render("Магазин приложений", True, (40,40,40))
        screen.blit(h, (r.centerx-h.get_width()//2, r.y+15))
        self.data['install_buttons'] = []
        apps = list(APP_STORE.items())
        cw = (r.width-60)//2; ch = 90; gap = 15
        sx, sy = r.x+20, r.y+60
        for i, (aid, info) in enumerate(apps):
            col, row = i%2, i//2
            cx = sx + col*(cw+gap); cy = sy + row*(ch+gap)
            if cy + ch > r.bottom - 10: break
            cr = pygame.Rect(cx, cy, cw, ch)
            hover = cr.collidepoint(pygame.mouse.get_pos())
            if aid == 'real_browser':
                pygame.draw.rect(screen, (255,240,200) if not hover else (255,230,160), cr, border_radius=8)
                pygame.draw.rect(screen, (200,140,0), cr, 2, border_radius=8)
            else:
                pygame.draw.rect(screen, (250,250,250) if not hover else (240,245,255), cr, border_radius=8)
                pygame.draw.rect(screen, (220,220,220), cr, 1, border_radius=8)
            screen.blit(font_ui_bold.render(info['name'], True, (40,40,40)), (cr.x+70, cr.y+12))
            screen.blit(font_ui.render(info['desc'], True, (100,100,100)), (cr.x+70, cr.y+34))
            screen.blit(font_ui.render(info['size'], True, (120,120,120)), (cr.x+70, cr.y+54))
            inst = aid in self.data['installed_apps']
            br = pygame.Rect(cr.right-110, cr.y+55, 95, 25)
            if aid == 'real_browser':
                pygame.draw.rect(screen, (219,68,55) if not hover else (240,90,80), br, border_radius=5); bt = "Открыть"
            elif inst:
                pygame.draw.rect(screen, (46,204,113), br, border_radius=5); bt = "Установлено"
            else:
                pygame.draw.rect(screen, COLORS['google_blue'] if not hover else (90,160,255), br, border_radius=5); bt = "Установить"
            bs = font_ui_bold.render(bt, True, (255,255,255))
            screen.blit(bs, (br.centerx-bs.get_width()//2, br.centery-bs.get_height()//2))
            self.data['install_buttons'].append((br, aid))


class Terminal:
    def __init__(self):
        self.fs = VirtualFS()
        self.history = []; self.history_index = -1
        self.output_lines = []; self.input_text = ""
        self.cursor_visible = True; self.cursor_timer = 0
        self.max_lines = 25
        self.is_root = False; self.sudo_mode = False
        self.sudo_password = ""; self.sudo_command = ""; self.password_attempts = 0
        self.app_windows = []
        self.installed_apps = set(CONFIG.get('installed_apps', []))
        self.last_notification = ""; self.notification_timer = 0
        self.bios = BIOS()
        self.power_action = None; self.power_timer = 0
        self.print_banner()
    def print_banner(self):
        bc = CONFIG.get('boot_count', 1)
        for line in [
            "=" * 60,
            "   GoginOS v5.3 - Linux-like   |  Загрузка #" + str(bc),
            "=" * 60,
            "Пользователь: " + USERNAME,
            "Дата: " + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            "Команды: help | open <app> | install <app> | apps | store",
            "Питание: reboot | shutdown | exit",
            "Google: команда 'google' откроет настоящий поисковик",
            "Файлы: install files && open files",
            "sudo пароль: 00912322  |  BIOS: sudo -i затем BIOS OPEN",
            ""
        ]: self.output_lines.append(('banner', line))
    def notify(self, text, duration=180):
        self.last_notification = text; self.notification_timer = duration
    def add_output(self, text, color_type='normal'):
        if text == '': self.output_lines.append((color_type, ''))
        else:
            for line in text.split('\n'): self.output_lines.append((color_type, line))
        if len(self.output_lines) > 500: self.output_lines = self.output_lines[-500:]
    def get_prompt(self):
        user = "root" if self.is_root else USERNAME
        path = self.fs.get_path_string()
        hp = '/home/' + USERNAME
        if not self.is_root and path.startswith(hp): path = '~' + path[len(hp):]
        return user + "@gogin:" + path + ("# " if self.is_root else "$ ")
    def execute(self, cmd_line):
        cmd_line = cmd_line.strip()
        if not cmd_line: return
        self.history.append(cmd_line); self.history_index = -1
        if cmd_line.startswith('sudo '):
            self.handle_sudo(cmd_line); return
        self.add_output(self.get_prompt() + cmd_line, 'command')
        parts = cmd_line.split(); cmd = parts[0].lower(); args = parts[1:]
        if cmd == 'bios' and args and args[0].upper() == 'OPEN':
            if not self.is_root:
                self.add_output("BIOS: Permission denied. Используйте sudo -i.", 'error'); return
            self.add_output("Запуск BIOS...", 'warning')
            self.bios.active = True; self.bios.menu_index = 0; self.bios.message = ""
            return
        method = getattr(self, 'cmd_' + cmd, None)
        if method:
            try: method(args)
            except Exception as e: self.add_output("Ошибка: " + str(e), 'error')
        else: self.add_output(cmd + ": команда не найдена. Введите 'help'.", 'error')
    def handle_sudo(self, cmd_line):
        rest = cmd_line[5:].strip()
        if not rest:
            self.add_output(self.get_prompt() + cmd_line, 'command')
            self.add_output("usage: sudo <команда>", 'error'); return
        if rest in ('-i', '-s'):
            self.add_output(self.get_prompt() + cmd_line, 'command')
            if self.is_root: self.add_output("Вы уже root!", 'info'); return
            self.sudo_mode = True; self.sudo_password = ""; self.sudo_command = "__enter_root_shell__"
            self.add_output("[sudo] password for user:", 'warning'); return
        if rest == '-k':
            self.add_output(self.get_prompt() + cmd_line, 'command')
            self.is_root = False
            self.add_output("sudo: root-сессия завершена.", 'info'); return
        if self.is_root:
            self.add_output(self.get_prompt() + cmd_line, 'command')
            self.execute_as_root(rest); return
        self.add_output(self.get_prompt() + cmd_line, 'command')
        self.sudo_mode = True; self.sudo_password = ""; self.sudo_command = rest
        self.add_output("[sudo] password for user:", 'warning')
    def execute_as_root(self, cmd_line):
        parts = cmd_line.split(); cmd = parts[0].lower(); args = parts[1:]
        if cmd == 'bios' and args and args[0].upper() == 'OPEN':
            self.add_output("Запуск BIOS...", 'warning')
            self.bios.active = True; self.bios.menu_index = 0; self.bios.message = ""; return
        method = getattr(self, 'cmd_' + cmd, None)
        if not method: self.add_output("sudo: " + cmd + ": команда не найдена", 'error'); return
        old = self.is_root; self.is_root = True
        try: method(args)
        except Exception as e: self.add_output("Ошибка: " + str(e), 'error')
        finally: self.is_root = old
    def on_sudo_password_entered(self):
        self.add_output("*" * len(self.sudo_password), 'text_dim')
        pwd_hash = hash_password(self.sudo_password)
        ok = (self.sudo_password == ROOT_PASSWORD_PLAIN or pwd_hash == ROOT_PASSWORD_HASH or pwd_hash == USER_PASSWORD_HASH)
        if ok:
            self.password_attempts = 0; self.add_output("Пароль верный", 'success')
            if self.sudo_command == "__enter_root_shell__":
                self.is_root = True; self.sudo_mode = False
                self.add_output("Вы вошли как root! Доступно: BIOS OPEN", 'warning')
            else:
                self.sudo_mode = False; self.execute_as_root(self.sudo_command)
        else:
            self.password_attempts += 1; self.add_output("Sorry, try again.", 'error')
            if self.password_attempts >= 3:
                self.add_output("sudo: 3 incorrect password attempts", 'error')
                self.password_attempts = 0; self.sudo_mode = False; self.sudo_command = ""
            else:
                self.add_output("[sudo] password for user:", 'warning'); self.sudo_password = ""
    def cmd_google(self, args):
        try:
            webbrowser.open("https://www.google.com")
            self.add_output("Открытие настоящего Google...", 'success')
            self.notify("Google открыт в браузере!")
        except Exception as e:
            self.add_output("Ошибка: " + str(e), 'error')
    def cmd_reboot(self, args):
        self.add_output("Перезагрузка через 3 секунды...", 'warning')
        self.add_output("(ESC или Ctrl+C для отмены)", 'text_dim')
        self.power_action = 'reboot'; self.power_timer = 180
    def cmd_shutdown(self, args):
        self.add_output("Выключение через 3 секунды...", 'warning')
        self.add_output("(ESC или Ctrl+C для отмены)", 'text_dim')
        self.power_action = 'shutdown'; self.power_timer = 180
    def cmd_poweroff(self, args): self.cmd_shutdown(args)
    def cmd_halt(self, args): self.cmd_shutdown(args)
    def cmd_bios(self, args):
        if not args or args[0].upper() != 'OPEN':
            self.add_output("Использование: BIOS OPEN", 'info'); return
        if not self.is_root:
            self.add_output("BIOS: Permission denied. Сначала: sudo -i", 'error'); return
        self.add_output("Запуск BIOS...", 'warning')
        self.bios.active = True; self.bios.menu_index = 0; self.bios.message = ""
    def cmd_open(self, args):
        if not args:
            self.add_output("open: укажите приложение", 'error')
            if self.installed_apps: self.add_output("Установлено: " + ', '.join(self.installed_apps), 'info')
            return
        aid = args[0].lower()
        if aid == 'real_browser' or aid == 'google': self.cmd_google(args); return
        if aid not in APP_STORE: self.add_output("open: '" + aid + "' не найдено", 'error'); return
        if aid not in self.installed_apps:
            self.add_output("open: '" + aid + "' не установлено. install " + aid, 'error'); return
        self.launch_app(aid)
    def launch_app(self, aid):
        for w in self.app_windows:
            if w.app_id == aid:
                self.app_windows.remove(w); self.app_windows.append(w); return
        info = APP_STORE[aid]; off = len(self.app_windows) * 30
        bx, by = 150 + off, 100 + off
        if aid == 'calculator': w = CalculatorApp(aid, "Калькулятор", bx, by, 320, 420)
        elif aid == 'notepad': w = NotepadApp(aid, "Блокнот", bx, by, 500, 400)
        elif aid == 'paint': w = PaintApp(aid, "Рисовалка", bx, by, 600, 450)
        elif aid == 'clock': w = ClockApp(aid, "Часы", bx+50, by+20, 300, 380)
        elif aid == 'music': w = MusicApp(aid, "Плеер", bx+50, by+20, 400, 350)
        elif aid == 'browser':
            w = YoninTorApp(aid, "Yonin Tor - Браузер", 80+off, 80+off, 750, 520)
            w.data['installed_apps'] = self.installed_apps
            w.data['on_app_installed'] = lambda a: self.auto_install(a)
        elif aid == 'files':
            w = FilesApp(aid, "Файлы", 100+off, 80+off, 800, 560); w.data['fs'] = self.fs
        else: w = AppWindow(aid, info['name'], bx, by, 400, 300)
        self.app_windows.append(w); self.add_output("Запуск: " + info['name'], 'success')
    def auto_install(self, aid):
        if aid not in self.installed_apps:
            self.installed_apps.add(aid); self.notify("Установлено: " + APP_STORE[aid]['name'])
            self.add_output("[СИСТЕМА] Установлено: " + APP_STORE[aid]['name'], 'success')
            self.save_config()
    def save_config(self):
        CONFIG['installed_apps'] = list(self.installed_apps)
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: json.dump(CONFIG, f, indent=2, ensure_ascii=False)
        except: pass
    def cmd_install(self, args):
        if not args:
            self.add_output("install: укажите приложение", 'error')
            self.add_output("Доступные: " + ', '.join(APP_STORE.keys()), 'info'); return
        aid = args[0].lower()
        if aid == 'real_browser':
            self.add_output("Не требует установки. Используйте: google", 'info'); return
        if aid not in APP_STORE: self.add_output("install: '" + aid + "' не найдено", 'error'); return
        if aid in self.installed_apps:
            self.add_output("'" + APP_STORE[aid]['name'] + "' уже установлено", 'warning'); return
        self.installed_apps.add(aid); info = APP_STORE[aid]
        self.add_output("Установка " + info['name'] + " (" + info['size'] + ")...", 'info')
        self.add_output("Установлено: " + info['name'], 'success')
        self.notify("Установлено: " + info['name']); self.save_config()
    def cmd_apps(self, args):
        if not self.installed_apps: self.add_output("Нет приложений. install browser", 'text_dim'); return
        self.add_output("Установленные:", 'info')
        for aid in sorted(self.installed_apps):
            info = APP_STORE[aid]; self.add_output("  " + info['name'].ljust(20) + " - open " + aid)
    def cmd_store(self, args):
        if 'browser' not in self.installed_apps: self.add_output("Сначала: install browser", 'error'); return
        self.launch_app('browser')
        for w in self.app_windows:
            if w.app_id == 'browser': w.data['view'] = 'app_store'
        self.add_output("Магазин открыт", 'info')
    def cmd_files(self, args):
        if 'files' not in self.installed_apps:
            self.add_output("Файлы не установлены. install files", 'error'); return
        self.launch_app('files')
    def cmd_help(self, args):
        h = """Команды: help, ls, cd, pwd, mkdir, touch, cat, echo, rm, clear, date, whoami, history, tree, exit

Приложения:
  open <app>      - запустить
  install <app>   - установить
  apps            - список
  store           - магазин
  files           - открыть файловый менеджер
  close-all       - закрыть все окна

GOOGLE:
  google          - открыть НАСТОЯЩИЙ Google

ПИТАНИЕ:
  reboot          - перезагрузка
  shutdown        - выключение
  halt, poweroff  - синонимы

BIOS (только root):
  sudo -i         - войти в root
  BIOS OPEN       - запустить BIOS

F11 - полный экран"""
        self.add_output(h, 'info')
    def cmd_ls(self, args):
        t = self.fs.list_dir(self.fs.resolve_path(args[0])) if args else self.fs.get_current_dir()
        if t is None: self.add_output("ls: нет директории", 'error'); return
        items = []
        for name, info in sorted(t.items()):
            if name in ('тип', 'дата', 'размер'): continue
            if info.get('права') == 'root_only' and not self.is_root: items.append("[LOCK]" + name)
            elif info.get('тип') == 'dir': items.append("[" + name + "]")
            else: items.append(" " + name + " ")
        if not items: self.add_output("(пусто)", 'text_dim')
        else:
            line = ""
            for it in items:
                if len(line) + len(it) + 2 > 60: self.add_output(line); line = ""
                line += it + "  "
            if line: self.add_output(line)
    def cmd_cd(self, args):
        if not args: self.fs.cwd = ['home', USERNAME]; return
        path = args[0]
        if path == '/': self.fs.cwd = []; return
        np = self.fs.resolve_path(path)
        if self.fs.list_dir(np) is None: self.add_output("cd: " + path + ": нет", 'error'); return
        if np and np[0] == 'root' and not self.is_root:
            self.add_output("cd: " + path + ": Permission denied", 'error'); return
        self.fs.cwd = np
    def cmd_pwd(self, args): self.add_output(self.fs.get_path_string())
    def cmd_mkdir(self, args):
        for n in args:
            if self.fs.mkdir(n): self.add_output("Создана: " + n, 'info')
            else: self.add_output("mkdir: '" + n + "' существует", 'error')
    def cmd_touch(self, args):
        for n in args:
            self.fs.create_file(n, '', 'root' if self.is_root else USERNAME)
            self.add_output("Создан: " + n, 'info')
    def cmd_cat(self, args):
        if not args: self.add_output("cat: укажите файл", 'error'); return
        c = self.fs.get_current_dir(); n = args[0]
        if n not in c: self.add_output("cat: " + n + ": не найден", 'error'); return
        if c[n]['тип'] != 'file': self.add_output("cat: " + n + ": директория", 'error'); return
        if c[n].get('права') == 'root_only' and not self.is_root:
            self.add_output("cat: " + n + ": Permission denied", 'error'); return
        self.add_output(c[n].get('содержимое', '') or "(пусто)")
    def cmd_echo(self, args):
        if '>' in args:
            i = args.index('>'); text = ' '.join(args[:i])
            if i+1 < len(args):
                fn = args[i+1]
                self.fs.create_file(fn, text, 'root' if self.is_root else USERNAME)
                self.add_output("Записано: " + fn, 'info')
        else: self.add_output(' '.join(args))
    def cmd_rm(self, args):
        for n in args:
            r = self.fs.delete(n, self.is_root)
            if r is True: self.add_output("Удалено: " + n, 'info')
            elif r == 'no_permission': self.add_output("rm: " + n + ": Permission denied", 'error')
            else: self.add_output("rm: не удалось '" + n + "'", 'error')
    def cmd_clear(self, args): self.output_lines = []
    def cmd_date(self, args): self.add_output(datetime.datetime.now().strftime('%A, %d %B %Y, %H:%M:%S'))
    def cmd_whoami(self, args): self.add_output("root" if self.is_root else USERNAME)
    def cmd_uname(self, args):
        self.add_output("GoginOS gogin 5.3 Python-Kernel x86_64" if args and args[0] == '-a' else "GoginOS")
    def cmd_history(self, args):
        for i, c in enumerate(self.history, 1): self.add_output("  " + str(i).rjust(3) + "  " + c)
    def cmd_tree(self, args):
        def pp(node, pre=''):
            items = [(n, i) for n, i in node.items() if n not in ('тип', 'дата', 'размер')]
            for i, (n, inf) in enumerate(items):
                last = i == len(items) - 1
                conn = '\\-- ' if last else '|-- '
                mk = '[D]' if inf.get('тип') == 'dir' else '[F]'
                lk = '[LOCK]' if inf.get('права') == 'root_only' and not self.is_root else ''
                self.add_output(pre + conn + mk + lk + ' ' + n)
                if inf.get('тип') == 'dir': pp(inf, pre + ('    ' if last else '|   '))
        self.add_output('/'); pp(self.fs.root)
    def cmd_close_all(self, args):
        n = len(self.app_windows); self.app_windows.clear()
        self.add_output("Закрыто: " + str(n), 'info')
    def cmd_exit(self, args):
        if self.is_root:
            self.is_root = False; self.add_output("Вышли из root.", 'info'); return
        self.add_output("Выход...", 'warning')
        pygame.time.wait(500); pygame.quit(); sys.exit()
    def cmd_sudo(self, args): self.add_output("sudo: используйте 'sudo <команда>'", 'info')
    def draw_terminal_bg(self, screen):
        screen.fill(COLORS['bg'])
        pygame.draw.rect(screen, (25,25,35), (0, 0, WIDTH, 28))
        pygame.draw.line(screen, COLORS['info'], (0, 28), (WIDTH, 28), 1)
        if self.is_root:
            sl = " ROOT MODE | GoginOS v5.3"; sc = COLORS['prompt_root']
        else:
            sl = " " + USERNAME + "@gogin | GoginOS v5.3"; sc = COLORS['success']
        mode_str = "ВЫХОД" if is_fullscreen else "F11"
        sr = datetime.datetime.now().strftime('%H:%M:%S') + " | " + mode_str + " | " + str(len(self.app_windows)) + " apps"
        screen.blit(font.render(sl, True, sc), (10, 6))
        rs = font.render(sr, True, COLORS['text_dim'])
        screen.blit(rs, (WIDTH - rs.get_width() - 15, 6))
        y = 35
        for ct, line in self.output_lines[-self.max_lines:]:
            color = COLORS.get(ct, COLORS['text'])
            if ct == 'banner': color = COLORS['info']
            elif ct == 'command': color = COLORS['prompt_root'] if self.is_root else COLORS['prompt_user']
            elif ct == 'error': color = COLORS['error']
            elif ct == 'info': color = COLORS['info']
            elif ct == 'warning': color = COLORS['warning']
            elif ct == 'text_dim': color = COLORS['text_dim']
            elif ct == 'success': color = COLORS['success']
            screen.blit(font.render(line, True, color), (10, y)); y += 20
        if self.sudo_mode:
            ps = font.render("[sudo] password for user: ", True, COLORS['warning'])
            screen.blit(ps, (10, y))
            ss = font.render("*" * len(self.sudo_password), True, COLORS['text'])
            screen.blit(ss, (10 + ps.get_width(), y))
            if self.cursor_visible:
                pygame.draw.rect(screen, COLORS['warning'], (10 + ps.get_width() + ss.get_width(), y+2, 10, 18))
        else:
            p = self.get_prompt(); pc = COLORS['prompt_root'] if self.is_root else COLORS['prompt_user']
            ps = font.render(p, True, pc); screen.blit(ps, (10, y))
            its = font.render(self.input_text, True, COLORS['text'])
            screen.blit(its, (10 + ps.get_width(), y))
            if self.cursor_visible:
                pygame.draw.rect(screen, COLORS['cursor'], (10 + ps.get_width() + its.get_width(), y+2, 10, 18))
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible; self.cursor_timer = 0
        if self.power_action and self.power_timer > 0:
            secs = (self.power_timer + 59) // 60
            at = "ПЕРЕЗАГРУЗКА" if self.power_action == 'reboot' else "ВЫКЛЮЧЕНИЕ"
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); ov.fill((0,0,0,180))
            screen.blit(ov, (0, 0))
            big = pygame.font.SysFont('consolas', 48, bold=True)
            txt = big.render(at, True, COLORS['warning'])
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 80))
            sub = font.render("Система " + at.lower() + " через " + str(secs) + " сек...", True, COLORS['text'])
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2))
            hint = font.render("ESC или Ctrl+C для отмены", True, COLORS['text_dim'])
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 50))
        if self.notification_timer > 0:
            self.notification_timer -= 1
            msg = font.render(self.last_notification, True, (255, 255, 255))
            r = pygame.Rect(0, 0, msg.get_width()+30, 40)
            r.centerx = WIDTH//2; r.bottom = HEIGHT - 20
            pygame.draw.rect(screen, COLORS['success'], r, border_radius=8)
            screen.blit(msg, (r.x + 15, r.y + 12))

def toggle_fullscreen():
    global screen, WIDTH, HEIGHT, is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        terminal.notify("Полный экран (F11 - выйти)", 120)
    else:
        WIDTH, HEIGHT = WINDOW_W, WINDOW_H
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        terminal.notify("Оконный режим", 120)
    terminal.max_lines = max(10, (HEIGHT - 100) // 20)

terminal = Terminal()
running = True
while running:
    if terminal.power_action and terminal.power_timer > 0:
        terminal.power_timer -= 1
        if terminal.power_timer <= 0:
            if terminal.power_action == 'shutdown':
                print("GoginOS: Система выключена.")
                pygame.quit(); sys.exit()
            elif terminal.power_action == 'reboot':
                print("GoginOS: Перезагрузка...")
                pygame.quit()
                os.execv(sys.executable, [sys.executable] + sys.argv)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and terminal.power_action:
            terminal.power_action = None; terminal.power_timer = 0
            terminal.add_output("Отменено.", 'info'); continue
        elif terminal.bios.active:
            terminal.bios.handle_event(event); continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            toggle_fullscreen(); continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and (event.mod & pygame.KMOD_CTRL):
            if terminal.power_action:
                terminal.power_action = None; terminal.power_timer = 0
                terminal.add_output("^C Отменено.", 'info'); continue
        elif terminal.app_windows:
            handled = False
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                mx, my = event.pos
                for w in reversed(terminal.app_windows):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if w.close_btn.collidepoint(mx, my):
                            terminal.app_windows.remove(w); handled = True; break
                        if w.min_btn.collidepoint(mx, my):
                            terminal.app_windows.remove(w); handled = True; break
                        tr = pygame.Rect(w.x, w.y, w.width, 34)
                        if tr.collidepoint(mx, my):
                            w.is_dragging = True
                            w.drag_off_x = mx - w.x; w.drag_off_y = my - w.y
                            terminal.app_windows.remove(w); terminal.app_windows.append(w)
                            handled = True; break
                        if pygame.Rect(w.x, w.y, w.width, w.height).collidepoint(mx, my):
                            if w.handle_event(event): handled = True; break
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if w.is_dragging: w.is_dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        if w.is_dragging:
                            w.x = mx - w.drag_off_x; w.y = my - w.drag_off_y
                            w.update_rects(); handled = True; break
                        if pygame.Rect(w.x, w.y, w.width, w.height).collidepoint(mx, my):
                            if w.handle_event(event): handled = True; break
            if not handled and event.type == pygame.KEYDOWN:
                if terminal.app_windows and terminal.app_windows[-1].handle_event(event): handled = True
            if not handled and event.type == pygame.KEYDOWN:
                if terminal.sudo_mode:
                    if event.key == pygame.K_RETURN: terminal.on_sudo_password_entered()
                    elif event.key == pygame.K_BACKSPACE: terminal.sudo_password = terminal.sudo_password[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        terminal.sudo_mode = False; terminal.sudo_password = ""; terminal.sudo_command = ""
                    elif event.unicode and event.unicode.isprintable(): terminal.sudo_password += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        terminal.execute(terminal.input_text); terminal.input_text = ""
                    elif event.key == pygame.K_BACKSPACE: terminal.input_text = terminal.input_text[:-1]
                    elif event.key == pygame.K_UP:
                        if terminal.history:
                            if terminal.history_index == -1: terminal.history_index = len(terminal.history) - 1
                            elif terminal.history_index > 0: terminal.history_index -= 1
                            terminal.input_text = terminal.history[terminal.history_index]
                    elif event.key == pygame.K_DOWN:
                        if terminal.history and terminal.history_index != -1:
                            if terminal.history_index < len(terminal.history) - 1:
                                terminal.history_index += 1
                                terminal.input_text = terminal.history[terminal.history_index]
                            else: terminal.history_index = -1; terminal.input_text = ""
                    elif event.key == pygame.K_ESCAPE: terminal.input_text = ""
                    elif event.unicode and event.unicode.isprintable(): terminal.input_text += event.unicode
        else:
            if event.type == pygame.KEYDOWN:
                if terminal.sudo_mode:
                    if event.key == pygame.K_RETURN: terminal.on_sudo_password_entered()
                    elif event.key == pygame.K_BACKSPACE: terminal.sudo_password = terminal.sudo_password[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        terminal.sudo_mode = False; terminal.sudo_password = ""; terminal.sudo_command = ""
                    elif event.unicode and event.unicode.isprintable(): terminal.sudo_password += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        terminal.execute(terminal.input_text); terminal.input_text = ""
                    elif event.key == pygame.K_BACKSPACE: terminal.input_text = terminal.input_text[:-1]
                    elif event.key == pygame.K_UP:
                        if terminal.history:
                            if terminal.history_index == -1: terminal.history_index = len(terminal.history) - 1
                            elif terminal.history_index > 0: terminal.history_index -= 1
                            terminal.input_text = terminal.history[terminal.history_index]
                    elif event.key == pygame.K_DOWN:
                        if terminal.history and terminal.history_index != -1:
                            if terminal.history_index < len(terminal.history) - 1:
                                terminal.history_index += 1
                                terminal.input_text = terminal.history[terminal.history_index]
                            else: terminal.history_index = -1; terminal.input_text = ""
                    elif event.key == pygame.K_ESCAPE: terminal.input_text = ""
                    elif event.unicode and event.unicode.isprintable(): terminal.input_text += event.unicode
    terminal.draw_terminal_bg(screen)
    if terminal.bios.active: terminal.bios.draw(screen)
    else:
        for w in terminal.app_windows: w.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
'''

# ============================================================
# УСТАНОВЩИК С 30-СЕКУНДНОЙ УСТАНОВКОЙ
# ============================================================

pygame.init()

WINDOW_W, WINDOW_H = 900, 650
WIDTH, HEIGHT = WINDOW_W, WINDOW_H
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GoginOS v5.3 — Установщик системы")
clock = pygame.time.Clock()

is_fullscreen = False

font = font_small = font_big = font_huge = None

def create_fonts():
    global font, font_small, font_big, font_huge
    font = pygame.font.SysFont('consolas,couriernew,monospace', 20)
    font_small = pygame.font.SysFont('consolas,couriernew,monospace', 15)
    font_big = pygame.font.SysFont('consolas,couriernew,monospace', 32, bold=True)
    font_huge = pygame.font.SysFont('consolas,couriernew,monospace', 48, bold=True)

create_fonts()

COLORS = {
    'bg': (15, 20, 35), 'panel': (25, 35, 55),
    'accent': (80, 180, 255), 'success': (46, 204, 113),
    'error': (231, 76, 60), 'warning': (241, 196, 15),
    'text': (230, 240, 255), 'text_dim': (140, 160, 190),
    'input_bg': (10, 15, 25), 'input_border': (60, 80, 120),
    'input_active': (80, 180, 255),
}

INSTALL_DIR = os.path.join(os.path.expanduser("~"), "GoginOS")
CONFIG_PATH = os.path.join(INSTALL_DIR, "config.json")
OS_FILE_PATH = os.path.join(INSTALL_DIR, "gogin_os.py")
ICON_PNG_PATH = os.path.join(INSTALL_DIR, "gogin.png")
ICON_ICO_PATH = os.path.join(INSTALL_DIR, "gogin.ico")
LAUNCHER_PATH = os.path.join(INSTALL_DIR, "start_gogin.bat" if os.name == 'nt' else "start_gogin.sh")
DESKTOP_SHORTCUT = os.path.join(os.path.expanduser("~"), "Desktop", "GoginOS.lnk")

INSTALL_DURATION_MS = 30000  # 30 секунд

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def validate_username(username):
    if not username: return False, "Имя пользователя не может быть пустым"
    if len(username) < 3: return False, "Имя должно быть не менее 3 символов"
    if len(username) > 20: return False, "Имя должно быть не более 20 символов"
    if not username.replace('_', '').isalnum(): return False, "Только буквы, цифры и _"
    return True, ""

def validate_password(password):
    if not password: return False, "Пароль не может быть пустым"
    if len(password) < 4: return False, "Пароль должен быть не менее 4 символов"
    return True, ""

def generate_icon():
    SIZE = 256
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    CX = CY = SIZE // 2
    pygame.draw.circle(surface, (52, 152, 219), (CX, CY), 110)
    pygame.draw.circle(surface, (41, 128, 185), (CX, CY), 110, 4)
    pygame.draw.circle(surface, (150, 200, 255), (CX, CY), 105, 2)
    g_font = pygame.font.SysFont('arial,segoeui,calibri', 130, bold=True)
    g_surf = g_font.render("G", True, (255, 255, 255))
    g_rect = g_surf.get_rect(center=(CX, CY - 5))
    surface.blit(g_surf, g_rect)
    pygame.image.save(surface, ICON_PNG_PATH)
    try:
        save_ico(surface, ICON_ICO_PATH)
        return True
    except Exception as e:
        print(f"[!] ICO не создан: {e}")
        return False

def save_ico(surface, path):
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for size in sizes:
        scaled = pygame.transform.smoothscale(surface, (size, size))
        data = pygame.image.tostring(scaled, "BGRA")
        images.append((size, data))
    with open(path, 'wb') as f:
        f.write(struct.pack('<HHH', 0, 1, len(images)))
        offset = 6 + 16 * len(images)
        entries = []
        for size, data in images:
            w = size if size < 256 else 0
            h = size if size < 256 else 0
            entry = struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, len(data), offset)
            entries.append(entry)
            offset += 40 + len(data) + size * ((size + 7) // 8)
        for e in entries: f.write(e)
        for size, data in images:
            bmp_header = struct.pack('<IiiHHIIiiII', 40, size, size * 2, 1, 32, 0, len(data) + size * ((size + 7) // 8), 0, 0, 0, 0)
            f.write(bmp_header)
            for y in range(size - 1, -1, -1):
                f.write(data[y * size * 4:(y + 1) * size * 4])
            mask_row = b'\x00' * ((size + 7) // 8)
            for _ in range(size): f.write(mask_row)

def create_desktop_shortcut():
    if os.name != 'nt': return False
    try:
        import subprocess
        ps_script = f'''
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{DESKTOP_SHORTCUT}")
        $Shortcut.TargetPath = "{LAUNCHER_PATH}"
        $Shortcut.WorkingDirectory = "{INSTALL_DIR}"
        $Shortcut.IconLocation = "{ICON_ICO_PATH}"
        $Shortcut.Description = "GoginOS v5.3 - Linux-like OS"
        $Shortcut.Save()
        '''
        result = subprocess.run(['powershell', '-NoProfile', '-Command', ps_script], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception as e:
        print(f"[!] Ярлык не создан: {e}")
        return False

def get_center_x(): return WIDTH // 2


class InputField:
    def __init__(self, x, y, width, height, label, placeholder="", is_password=False):
        self.rel_y = y
        self.width = width; self.height = height
        self.label = label; self.placeholder = placeholder
        self.text = ""; self.is_password = is_password; self.active = False
        self.rect = pygame.Rect(x, y, width, height)
        self.update_position()
    def update_position(self):
        self.rect = pygame.Rect(get_center_x() - self.width // 2, self.rel_y, self.width, self.height)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            return self.active
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.key == pygame.K_TAB: return 'tab'
            elif event.key == pygame.K_RETURN: return 'enter'
            else:
                if event.unicode and event.unicode.isprintable(): self.text += event.unicode
            return True
        return False
    def draw(self, screen):
        label_surf = font_small.render(self.label, True, COLORS['text_dim'])
        screen.blit(label_surf, (self.rect.x, self.rect.y - 22))
        pygame.draw.rect(screen, COLORS['input_bg'], self.rect, border_radius=6)
        bc = COLORS['input_active'] if self.active else COLORS['input_border']
        pygame.draw.rect(screen, bc, self.rect, 2, border_radius=6)
        display_text = ("*" * len(self.text)) if self.is_password else self.text
        if display_text:
            txt_surf = font.render(display_text, True, COLORS['text'])
            screen.blit(txt_surf, (self.rect.x + 12, self.rect.y + 8))
        elif self.placeholder:
            ph = font.render(self.placeholder, True, COLORS['text_dim'])
            screen.blit(ph, (self.rect.x + 12, self.rect.y + 8))
        if self.active and int(datetime.datetime.now().timestamp() * 2) % 2 == 0:
            cx = self.rect.x + 12
            if display_text: cx += font.size(display_text)[0]
            pygame.draw.line(screen, COLORS['accent'], (cx, self.rect.y+6), (cx, self.rect.bottom-6), 2)


class Button:
    def __init__(self, x, y, width, height, text, color=None, rel_bottom_offset=90):
        self.width = width; self.height = height
        self.text = text; self.color = color or COLORS['accent']
        self.enabled = True; self.rel_bottom_offset = rel_bottom_offset
        self.rect = pygame.Rect(x, y, width, height)
        self.update_position()
    def update_position(self):
        self.rect = pygame.Rect(get_center_x() - self.width // 2, HEIGHT - self.rel_bottom_offset, self.width, self.height)
    def is_hovered(self): return self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self, screen):
        color = self.color if self.enabled else (80, 80, 80)
        if self.enabled and self.is_hovered():
            color = tuple(min(c + 30, 255) for c in color)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['text'], self.rect, 1, border_radius=8)
        txt = font.render(self.text, True, COLORS['text'])
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
    def is_clicked(self, event):
        return (self.enabled and event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos))


class Installer:
    def __init__(self):
        self.step = 0
        cx = get_center_x()
        self.username_field = InputField(cx - 200, 250, 400, 44, "Имя пользователя:", "например, alex")
        self.password_field = InputField(cx - 200, 350, 400, 44, "Пароль:", "минимум 4 символа", is_password=True)
        self.password2_field = InputField(cx - 200, 450, 400, 44, "Подтвердите пароль:", "", is_password=True)
        self.fields = [self.username_field, self.password_field, self.password2_field]
        self.active_field = 0
        self.btn_next = Button(0, 0, 200, 50, "Далее ->")
        self.btn_install = Button(0, 0, 220, 50, "УСТАНОВИТЬ", COLORS['success'])
        self.btn_finish = Button(0, 0, 200, 50, "Завершить", COLORS['success'])
        self.error = ""; self.error_timer = 0
        self.shortcut_created = False
        # Прогресс установки
        self.install_messages = []
        self.install_start_time = 0
        self.install_done = False
        self.icon_done = False
        self.current_msg_index = 0
        self.install_progress = 0
    
    def update_layout(self):
        for f in self.fields: f.update_position()
        self.btn_next.update_position()
        self.btn_install.update_position()
        self.btn_finish.update_position()
    
    def show_error(self, msg):
        self.error = msg; self.error_timer = 120
    
    def prepare_install(self):
        """Подготовить данные и перейти к экрану установки"""
        username = self.username_field.text.strip()
        password = self.password_field.text
        password2 = self.password2_field.text
        ok, msg = validate_username(username)
        if not ok: self.show_error(msg); return
        ok, msg = validate_password(password)
        if not ok: self.show_error(msg); return
        if password != password2: self.show_error("Пароли не совпадают"); return
        # Всё ок — показываем экран "нажмите УСТАНОВИТЬ"
        self.step = 2
    
    def start_install(self):
        """Начать установку — 30 секунд"""
        self.install_messages = [
            "Проверка системы...",
            "Создание директории установки...",
            "Запись файла gogin_os.py...",
            "Сохранение конфигурации...",
            "Хеширование пароля...",
            "Генерация иконки GoginOS...",
            "Создание PNG и ICO...",
            "Создание системных папок...",
            "Создание лог-файла...",
            "Создание ярлыка запуска...",
            "Ярлык на Рабочем столе...",
            "Настройка прав доступа...",
            "Установка базовых приложений...",
            "Регистрация в системе...",
            "Финальная настройка...",
            "Установка завершена!"
        ]
        self.install_start_time = pygame.time.get_ticks()
        self.current_msg_index = 0
        self.install_progress = 0
        self.install_done = False
        self.icon_done = False
        self.step = 3
    
    def perform_install(self):
        try:
            os.makedirs(INSTALL_DIR, exist_ok=True)
            with open(OS_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(GOGIN_OS_CODE)
            config = {
                "username": self.username_field.text.strip(),
                "password_hash": hash_password(self.password_field.text),
                "root_password_hash": hash_password("00912322"),
                "installed_at": datetime.datetime.now().isoformat(),
                "version": "5.3",
                "boot_count": 0,
                "last_boot": None,
                "installed_apps": [],
                "theme": "dark"
            }
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            for folder in ['home', 'apps', 'logs', 'tmp']:
                os.makedirs(os.path.join(INSTALL_DIR, folder), exist_ok=True)
            with open(os.path.join(INSTALL_DIR, 'logs', 'install.log'), 'w', encoding='utf-8') as f:
                f.write("GoginOS v5.3 установлена\n")
                f.write("Дата: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
                f.write("Пользователь: " + self.username_field.text.strip() + "\n")
                f.write("Директория: " + INSTALL_DIR + "\n")
            if os.name == 'nt':
                with open(LAUNCHER_PATH, 'w', encoding='utf-8') as f:
                    f.write('@echo off\n')
                    f.write('title GoginOS v5.3\n')
                    f.write('echo Запуск GoginOS...\n')
                    f.write('python "' + OS_FILE_PATH + '"\n')
                    f.write('pause\n')
            else:
                with open(LAUNCHER_PATH, 'w', encoding='utf-8') as f:
                    f.write('#!/bin/bash\n')
                    f.write('echo "Запуск GoginOS..."\n')
                    f.write('python3 "' + OS_FILE_PATH + '"\n')
                os.chmod(LAUNCHER_PATH, 0o755)
            return True
        except Exception as e:
            self.show_error("Ошибка: " + str(e))
            return False
    
    def do_icon_and_shortcut(self):
        try:
            generate_icon()
            if os.name == 'nt':
                self.shortcut_created = create_desktop_shortcut()
        except Exception as e:
            print(f"[!] Иконка/ярлык: {e}")
    
    def handle_event(self, event):
        if event.type == pygame.QUIT: return 'quit'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            return 'toggle_fullscreen'
        
        if self.step == 0:
            if self.btn_next.is_clicked(event):
                self.step = 1; self.username_field.active = True
        elif self.step == 1:
            for i, field in enumerate(self.fields):
                result = field.handle_event(event)
                if result == 'tab':
                    field.active = False
                    self.active_field = (self.active_field + 1) % len(self.fields)
                    self.fields[self.active_field].active = True
                elif result == 'enter':
                    self.prepare_install()
                elif result is True:
                    for j, f in enumerate(self.fields):
                        if j != i: f.active = False
                    self.active_field = i
            if self.btn_next.is_clicked(event): self.prepare_install()
        
        elif self.step == 2:
            # Экран "Готов к установке" — ждём нажатия УСТАНОВИТЬ
            if self.btn_install.is_clicked(event):
                self.start_install()
        
        elif self.step == 3:
            # Идёт установка — 30 секунд, автоматически
            elapsed = pygame.time.get_ticks() - self.install_start_time
            progress_ratio = min(1.0, elapsed / INSTALL_DURATION_MS)
            
            total_msgs = len(self.install_messages)
            new_index = int(progress_ratio * (total_msgs - 1))
            if new_index > self.current_msg_index:
                self.current_msg_index = new_index
            
            # Реальная установка — один раз на 15%
            if not self.install_done and progress_ratio >= 0.15:
                self.perform_install()
                self.install_done = True
            
            # Иконка — один раз на 30%
            if not self.icon_done and progress_ratio >= 0.30:
                self.do_icon_and_shortcut()
                self.icon_done = True
            
            self.install_progress = progress_ratio
            
            if progress_ratio >= 1.0:
                self.step = 4
        
        elif self.step == 4:
            if self.btn_finish.is_clicked(event): return 'quit'
        return None
    
    def draw(self):
        screen.fill(COLORS['bg'])
        for i in range(0, WIDTH, 40): pygame.draw.line(screen, (20,30,50), (i,0), (i,HEIGHT))
        for i in range(0, HEIGHT, 40): pygame.draw.line(screen, (20,30,50), (0,i), (WIDTH,i))
        
        pygame.draw.rect(screen, (10, 15, 25), (0, 0, WIDTH, 28))
        pygame.draw.line(screen, COLORS['accent'], (0, 28), (WIDTH, 28), 1)
        mode_str = "F11: ВЫХОД" if is_fullscreen else "F11: ПОЛНЫЙ ЭКРАН"
        mode_surf = font_small.render("GoginOS Установщик v5.3   |   " + mode_str, True, COLORS['text_dim'])
        screen.blit(mode_surf, (WIDTH - mode_surf.get_width() - 15, 6))
        
        if self.step == 0: self.draw_welcome()
        elif self.step == 1: self.draw_user_setup()
        elif self.step == 2: self.draw_ready()
        elif self.step == 3: self.draw_install_progress()
        elif self.step == 4: self.draw_done()
        
        if self.error_timer > 0:
            self.error_timer -= 1
            err = font.render(self.error, True, COLORS['error'])
            r = pygame.Rect(0, 0, err.get_width()+40, 50)
            r.centerx = WIDTH//2; r.bottom = HEIGHT - 20
            pygame.draw.rect(screen, (60,20,20), r, border_radius=8)
            pygame.draw.rect(screen, COLORS['error'], r, 2, border_radius=8)
            screen.blit(err, (r.x+20, r.y+14))
    
    def draw_welcome(self):
        title = font_huge.render("GoginOS", True, COLORS['accent'])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        version = font_big.render("v5.3 Установщик", True, COLORS['text_dim'])
        screen.blit(version, (WIDTH//2 - version.get_width()//2, 120))
        lines = [
            "Добро пожаловать в установщик GoginOS!",
            "",
            "Установщик содержит в себе всю систему.",
            "Директория установки:",
            "  " + INSTALL_DIR,
            "",
            "Будет создано:",
            "  • gogin_os.py     — операционная система",
            "  • config.json     — ваши настройки",
            "  • gogin.png/ico   — иконка системы",
            "  • start_gogin.*   — ярлык запуска",
            "  • ярлык на Рабочем столе (Windows)",
            "",
            "Установка займёт ровно 30 секунд.",
            "Прогресс пойдёт автоматически.",
            "",
            "F11 — развернуть на весь экран.",
        ]
        y = 190
        for line in lines:
            color = COLORS['text'] if line else COLORS['text_dim']
            if line.startswith("  •"): color = COLORS['accent']
            if "F11" in line or "30 секунд" in line: color = COLORS['warning']
            surf = font.render(line, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += 24
        self.btn_next.draw(screen)
    
    def draw_user_setup(self):
        title = font_big.render("Настройка пользователя", True, COLORS['accent'])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 130))
        sub = font.render("Создайте свою учётную запись", True, COLORS['text_dim'])
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 180))
        for f in self.fields: f.draw(screen)
        hint = font_small.render("Tab — переключение  |  Enter — продолжить  |  F11 — полный экран", True, COLORS['text_dim'])
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 130))
        self.btn_next.draw(screen)
    
    def draw_ready(self):
        title = font_big.render("Готов к установке", True, COLORS['success'])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        info_lines = [
            "Пользователь: " + self.username_field.text.strip(),
            "Пароль: " + ("*" * len(self.password_field.text)),
            "Директория: " + INSTALL_DIR,
            "",
            "Время установки: ровно 30 секунд",
            "",
            "Прогресс пойдёт автоматически —",
            "не нужно ничего нажимать.",
        ]
        y = 200
        for line in info_lines:
            color = COLORS['text'] if line else COLORS['text_dim']
            if "30 секунд" in line: color = COLORS['warning']
            if "автоматически" in line: color = COLORS['accent']
            surf = font.render(line, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += 32
        
        # Иконка-предупреждение
        pygame.draw.circle(screen, COLORS['warning'], (WIDTH//2, y + 40), 30)
        pygame.draw.circle(screen, COLORS['bg'], (WIDTH//2, y + 40), 26)
        warn_surf = font_huge.render("!", True, COLORS['warning'])
        screen.blit(warn_surf, (WIDTH//2 - warn_surf.get_width()//2, y + 15))
        
        hint = font.render("Нажмите УСТАНОВИТЬ для начала", True, COLORS['text_dim'])
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, y + 100))
        
        self.btn_install.draw(screen)
    
    def draw_install_progress(self):
        title = font_big.render("Установка GoginOS", True, COLORS['accent'])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Таймер обратного отсчёта
        elapsed = pygame.time.get_ticks() - self.install_start_time
        remaining = max(0, (INSTALL_DURATION_MS - elapsed) / 1000)
        time_str = f"Осталось: {remaining:.1f} сек"
        time_surf = font.render(time_str, True, COLORS['warning'])
        screen.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, 100))
        
        # Прогресс-бар
        bx = 100; by = 150; bw = WIDTH - 200; bh = 35
        pygame.draw.rect(screen, COLORS['input_bg'], (bx, by, bw, bh), border_radius=18)
        fw = int(bw * self.install_progress)
        if fw > 0:
            pygame.draw.rect(screen, COLORS['success'], (bx, by, fw, bh), border_radius=18)
        pygame.draw.rect(screen, COLORS['text_dim'], (bx, by, bw, bh), 2, border_radius=18)
        
        # Процент
        p_surf = font_big.render(str(int(self.install_progress*100)) + "%", True, COLORS['text'])
        screen.blit(p_surf, (WIDTH//2 - p_surf.get_width()//2, by + 45))
        
        # Список сообщений
        y = 260
        total_msgs = len(self.install_messages)
        for i, msg in enumerate(self.install_messages):
            if i < self.current_msg_index:
                color = COLORS['success']; prefix = "[OK] "
            elif i == self.current_msg_index:
                color = COLORS['accent']; prefix = "[>>] "
            else:
                color = COLORS['text_dim']; prefix = "[  ] "
            if i <= self.current_msg_index:
                surf = font_small.render(prefix + msg, True, color)
                screen.blit(surf, (100, y)); y += 20
                if y > HEIGHT - 80: break
        
        # Подсказка
        hint = font_small.render("Установка идёт автоматически, не нужно ничего нажимать", True, COLORS['text_dim'])
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))
    
    def draw_done(self):
        cx = WIDTH//2; cy = 110
        pygame.draw.circle(screen, COLORS['success'], (cx, cy), 45)
        pygame.draw.circle(screen, COLORS['bg'], (cx, cy), 40)
        pygame.draw.lines(screen, COLORS['success'], False, [(cx-18, cy), (cx-4, cy+14), (cx+18, cy-14)], 6)
        title = font_huge.render("Готово!", True, COLORS['success'])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 175))
        lines = [
            "GoginOS v5.3 успешно установлена!",
            "",
            "Пользователь: " + self.username_field.text.strip(),
            "Директория: " + INSTALL_DIR,
            "Пароль root: 00912322",
            "",
            "Что создано:",
            "  ✓ gogin_os.py, config.json",
            "  ✓ gogin.png + gogin.ico",
            "  ✓ " + ("Ярлык на рабочем столе" if self.shortcut_created else "Ярлык запуска"),
            "",
            "Запуск: python " + OS_FILE_PATH
        ]
        y = 250
        for line in lines:
            color = COLORS['text'] if line else COLORS['text_dim']
            if "Пароль root" in line: color = COLORS['warning']
            if line.startswith("  ✓"): color = COLORS['success']
            if "python" in line: color = COLORS['accent']
            surf = font.render(line, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y)); y += 22
        self.btn_finish.draw(screen)


def toggle_fullscreen():
    global screen, WIDTH, HEIGHT, is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        WIDTH, HEIGHT = WINDOW_W, WINDOW_H
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    installer.update_layout()


installer = Installer()
running = True
while running:
    for event in pygame.event.get():
        result = installer.handle_event(event)
        if result == 'quit': running = False
        elif result == 'toggle_fullscreen': toggle_fullscreen()
    installer.draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()