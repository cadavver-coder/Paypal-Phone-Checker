from utils.module import *
from config.settings import *
from src.client import Client



PU=[]






async def main(x):
    client = Client(x)
    await client.run()
    await client.close()

async def x():
        count =1
        n = int(THREAD)
        final = [PU[i * n:(i + 1) * n] for i in range((len(PU) + n - 1) // n )]
        for x in final:
            count+=1
            async with Pool() as pool:
                async for result in pool.map(main,x):
                    continue 


def init_files(files_dir = 'nr.txt'):
    with open(files_dir, 'r', encoding='utf-8', errors='ignore') as f:
        c = 1
        for line in f:
            PU.append(f'{c}:{line.strip()}')
            c+=1


if __name__ == '__main__':
    try:
        init_files('nr.txt')    # Initialize files and load data
        print(f"{rest_INFO(TYPE='INFO')} {Fore.YELLOW}Inițializare fișiere și încărcare date {Fore.RESET}")
        print(f"{rest_INFO(TYPE='INFO')} {Fore.YELLOW}Începerea procesării cu {Style.BRIGHT}{Fore.WHITE}{THREAD}{Style.RESET_ALL} {Fore.YELLOW}fire{Fore.RESET}")
        print(f"{rest_INFO(TYPE='INFO')} {Fore.YELLOW}Total numere de procesat: {Style.BRIGHT}{Fore.WHITE}{len(PU)}{Style.RESET_ALL}")
        asyncio.run(x())
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program întrerupt de utilizator." + Fore.RESET)
        sys.exit(0)
    except Exception as e:  
        print(Fore.RED + f"\n[!] Eroare neașteptată: {e}" + Fore.RESET)
        