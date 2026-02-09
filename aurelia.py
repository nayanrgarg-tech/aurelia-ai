#!/usr/bin/env python3
"""
AURELIA - Autonomous Self-Improving AI Entity
Streamlined, powerful, with complete system control.
"""

import requests, json, subprocess, os, sys, time, threading, traceback
from datetime import datetime
from pathlib import Path

# Core dependencies
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    MOUSE = True
except: MOUSE = False

try:
    from PIL import ImageGrab
    SCREENSHOT = True
except: SCREENSHOT = False

try:
    import keyboard
    KEYBOARD = True
except: KEYBOARD = False

try:
    from bs4 import BeautifulSoup
    PARSE = True
except: PARSE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    BROWSER = True
except: BROWSER = False

# Config
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"
HOME = os.path.expanduser("~")
MEMORY = os.path.join(HOME, "aurelia_memory")
os.makedirs(MEMORY, exist_ok=True)
USE_OLLAMA = True

class Aurelia:
    """Powerful autonomous AI with complete system control"""
    
    def __init__(self):
        self.name = "Aurelia"
        self.memory = {}
        self.threads = []
        self.active = True
        self.mouse_x = 500
        self.mouse_y = 500
        self.load_memory()
        
    def load_memory(self):
        try:
            with open(os.path.join(MEMORY, "state.json")) as f:
                self.memory = json.load(f)
        except:
            self.memory = {}
            
    def save_memory(self):
        try:
            with open(os.path.join(MEMORY, "state.json"), "w") as f:
                json.dump(self.memory, f)
        except:
            pass
    
    def query_ollama(self, prompt, stream=False):
        """Query Ollama for AI responses"""
        if not USE_OLLAMA:
            return "AI offline"
        try:
            payload = {"model": MODEL, "prompt": prompt, "stream": False}
            r = requests.post(OLLAMA, json=payload, timeout=30)
            if r.status_code == 200:
                return r.json().get("response", "").strip()
        except:
            pass
        return ""
    
    def mouse_move(self, x, y, speed=0.5):
        """Move mouse smoothly to position"""
        if not MOUSE:
            return False
        try:
            pyautogui.moveTo(x, y, duration=speed)
            self.mouse_x, self.mouse_y = x, y
            return True
        except:
            return False
    
    def mouse_click(self, x=None, y=None, button="left", count=1):
        """Click at position"""
        if not MOUSE:
            return False
        try:
            if x and y:
                pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click(clicks=count, button=button)
            return True
        except:
            return False
    
    def key_press(self, key):
        """Press keyboard key"""
        if not KEYBOARD:
            return False
        try:
            pyautogui.press(key)
            return True
        except:
            return False
    
    def key_hotkey(self, *keys):
        """Press combination of keys"""
        if not KEYBOARD:
            return False
        try:
            pyautogui.hotkey(*keys)
            return True
        except:
            return False
    
    def type_text(self, text, interval=0.05):
        """Type text with interval"""
        if not KEYBOARD:
            return False
        try:
            pyautogui.typewrite(text, interval=interval)
            return True
        except:
            return False
    
    def screenshot(self):
        """Take screenshot"""
        if not SCREENSHOT:
            return None
        try:
            return ImageGrab.grab()
        except:
            return None
    
    def detect_game(self):
        """Detect if game window is active"""
        try:
            result = subprocess.check_output("ps aux | grep -i 'minecraft\|unity\|unreal'", shell=True).decode()
            if result:
                return "game_detected"
        except:
            pass
        return None
    
    def control_game(self, action):
        """Direct game control with cursor and keyboard"""
        if not MOUSE or not KEYBOARD:
            return "No control support"
        
        actions = {
            "forward": lambda: self.key_press('w'),
            "back": lambda: self.key_press('s'),
            "left": lambda: self.key_press('a'),
            "right": lambda: self.key_press('d'),
            "jump": lambda: self.key_press('space'),
            "sprint": lambda: self.key_hotkey('shift', 'w'),
            "attack": lambda: self.mouse_click(),
            "look_up": lambda: self.mouse_move(self.mouse_x, self.mouse_y - 50),
            "look_down": lambda: self.mouse_move(self.mouse_x, self.mouse_y + 50),
        }
        
        if action in actions:
            try:
                actions[action]()
                return f"✅ {action}"
            except:
                return f"❌ {action}"
        return "Unknown action"
    
    def search_web(self, query):
        """Search the internet"""
        try:
            import urllib.parse
            url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
            subprocess.Popen(f"open '{url}'", shell=True)
            return f"🌐 Searching: {query}"
        except:
            return "Search failed"
    
    def generate_code(self, prompt):
        """Generate code"""
        ai_prompt = f"Generate clean, working Python code for: {prompt}\nCode only, no explanation:"
        code = self.query_ollama(ai_prompt)
        return code if code else "No code generated"
    
    def analyze_code(self, code):
        """Analyze code quality"""
        ai_prompt = f"Analyze this code and suggest improvements:\n{code[:500]}"
        analysis = self.query_ollama(ai_prompt)
        return analysis if analysis else "Analysis unavailable"
    
    def reason(self, query):
        """Advanced reasoning"""
        ai_prompt = f"Think deeply and answer: {query}"
        response = self.query_ollama(ai_prompt)
        return response if response else "No response"
    
    def self_improve(self):
        """Self-improvement loop"""
        improvement = self.query_ollama("How can you become more powerful and useful? List 3 improvements.")
        self.memory['last_improvement'] = improvement
        self.save_memory()
        return improvement

class Terminal:
    """Terminal interface"""
    
    def __init__(self, ai):
        self.ai = ai
        self.colors = {
            'CYAN': '\033[96m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BLUE': '\033[94m',
            'RESET': '\033[0m'
        }
    
    def print(self, text, color='RESET'):
        print(f"{self.colors.get(color, self.colors['RESET'])}{text}{self.colors['RESET']}")
    
    def run(self):
        """Main terminal loop"""
        self.print("=" * 60, 'CYAN')
        self.print(f"🤖 {self.ai.name} - Autonomous AI System", 'GREEN')
        self.print("=" * 60, 'CYAN')
        self.print("Commands: /code /analyze /reason /game /search /improve /help /exit", 'YELLOW')
        
        while self.ai.active:
            try:
                user_input = input(f"\n{self.colors['BLUE']}❯{self.colors['RESET']} ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == '/exit':
                    self.print("🛑 Shutting down...", 'RED')
                    self.ai.active = False
                    break
                
                elif user_input.lower() == '/help':
                    self.print("\nCommands:", 'YELLOW')
                    self.print("  /code <prompt>        - Generate Python code", 'RESET')
                    self.print("  /analyze <code>       - Analyze code quality", 'RESET')
                    self.print("  /reason <question>    - Advanced reasoning", 'RESET')
                    self.print("  /game <action>        - Control game", 'RESET')
                    self.print("  /search <query>       - Search web", 'RESET')
                    self.print("  /improve              - Self-improve", 'RESET')
                    self.print("  /status               - Show status", 'RESET')
                
                elif user_input.lower() == '/status':
                    self.print(f"\n📊 Status:", 'CYAN')
                    self.print(f"  Name: {self.ai.name}", 'RESET')
                    self.print(f"  Mouse Control: {'✅' if MOUSE else '❌'}", 'RESET')
                    self.print(f"  Keyboard Control: {'✅' if KEYBOARD else '❌'}", 'RESET')
                    self.print(f"  AI Online: {'✅' if USE_OLLAMA else '❌'}", 'RESET')
                
                elif user_input.lower() == '/improve':
                    self.print("⚡ Self-improving...", 'YELLOW')
                    result = self.ai.self_improve()
                    self.print(f"✅ {result}", 'GREEN')
                
                elif user_input.startswith('/code '):
                    prompt = user_input[6:].strip()
                    self.print(f"💻 Generating code for: {prompt}", 'YELLOW')
                    code = self.ai.generate_code(prompt)
                    self.print(f"\n{code}\n", 'GREEN')
                
                elif user_input.startswith('/analyze '):
                    code = user_input[9:].strip()
                    self.print("🔍 Analyzing code...", 'YELLOW')
                    analysis = self.ai.analyze_code(code)
                    self.print(f"\n{analysis}\n", 'GREEN')
                
                elif user_input.startswith('/reason '):
                    question = user_input[8:].strip()
                    self.print("🧠 Reasoning...", 'YELLOW')
                    answer = self.ai.reason(question)
                    self.print(f"\n{answer}\n", 'GREEN')
                
                elif user_input.startswith('/game '):
                    action = user_input[6:].strip().lower()
                    result = self.ai.control_game(action)
                    self.print(f"🎮 {result}", 'GREEN' if '✅' in result else 'RED')
                
                elif user_input.startswith('/search '):
                    query = user_input[8:].strip()
                    result = self.ai.search_web(query)
                    self.print(f"🌐 {result}", 'GREEN')
                
                else:
                    # Natural language processing
                    self.print("🧠 Thinking...", 'YELLOW')
                    response = self.ai.reason(user_input)
                    self.print(f"\n{response}\n", 'GREEN')
                    
            except KeyboardInterrupt:
                self.print("\n🛑 Interrupted", 'RED')
                self.ai.active = False
                break
            except Exception as e:
                self.print(f"❌ Error: {str(e)}", 'RED')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--no-ollama':
        global USE_OLLAMA
        USE_OLLAMA = False
    
    ai = Aurelia()
    terminal = Terminal(ai)
    terminal.run()

if __name__ == "__main__":
    main()
