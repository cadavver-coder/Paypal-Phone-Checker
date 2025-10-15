import sys
import subprocess
import tempfile
from pathlib import Path


# dacă lipsesc, le vom instala automat
required_modules = [ 
    "aiohttp",   # pentru cereri HTTP asincrone
    "colorama",  # pentru colorarea textului în terminal#    
    "aiomultiprocess", # pentru procesare paralelă asincronă
    "bs4",
    "aiofiles"  # pentru lucrul asincron cu fișiere
]

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"[!] Modulul '{module}' lipsește. Îl instalez automat...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Acum putem importa modulele necesare
try:
    import json # pentru lucrul cu fișiere JSON
    import time # pentru funcții legate de timp
    import asyncio # pentru programare asincronă
    import aiohttp # pentru cereri HTTP asincrone
    from datetime import datetime # pentru lucrul cu date și ore
    from colorama import Fore, Style,  init; init() # pentru colorarea textului în terminal
    from asyncio.exceptions import TimeoutError # pentru gestionarea erorilor de timeout
    from aiomultiprocess import Pool # pentru procesare paralelă asincronă
    import sqlite3  # pentru lucrul cu baze de date SQLite
    import random # pentru generarea de numere aleatoare
    import os # pentru lucrul cu sistemul de operare
    from bs4 import BeautifulSoup # pentru parsarea HTML
    import aiofiles

except Exception as e: # capturăm orice altă eroare de import
    print(f"Eroare la import: {e}")
    # ieșim din program dacă nu putem importa modulele necesare
    sys.exit(1)





def rest_INFO(TYPE = 'INFO'):
    if TYPE == 'INFO':
        return f'{Fore.MAGENTA}[ {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Fore.MAGENTA}] {Fore.CYAN}[ INFO ]{Fore.RESET}'
    elif TYPE == 'ERROR': 
        return f'{Fore.MAGENTA}[ {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Fore.MAGENTA}] {Fore.RED}[ ERROR ]{Fore.RESET}'
    elif TYPE == 'SUCCESS': 
        return f'{Fore.MAGENTA}[ {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Fore.MAGENTA}] {Fore.GREEN}[ SUCCESS ]{Fore.RESET}'
    elif TYPE == 'WARNING': 
        return f'{Fore.MAGENTA}[ {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Fore.MAGENTA}] {Fore.YELLOW}[ WARNING ]{Fore.RESET}'
