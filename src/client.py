from utils.module import *
from config.settings import USE_PROXY, TIMEOUT_PROXY, MAX_RETRIES


class Client:
    def __init__(self, number):
        self.ids, self.number = number.split(':')
        self.use_proxy = USE_PROXY

        self.session = aiohttp.ClientSession()
        self.cookies_init_session = {}
        self.cookie_file = Path(__file__).parent / "cookies_temp.json"
        self.lock = asyncio.Lock()
        self.token = None
        self.headers_init_session = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,ro;q=0.8',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"141.0.7390.54"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.54", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.54"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.11'
        }
        self.domain = 'https://www.paypal.com'

    async def set_proxy(self):
        self.proxy = None
        if self.use_proxy:
            try:
                with open('proxies.txt', 'r', encoding='utf-8') as file:
                    data = file.read().split()
                    self.proxy = 'http://' + random.choice(data)

                async with self.session.get('https://api.ipify.org?format=json', proxy=self.proxy, timeout=TIMEOUT_PROXY) as response:
                    result = await response.json()
                    self.ipsss = result.get('ip')
                    print(self.ipsss)
            except Exception as e:
                print(f'Please wait to change proxy... {e}')
                await self.set_proxy()

    async def load_cookies(self):
        async with self.lock:
            if self.cookie_file.exists():
                async with aiofiles.open(self.cookie_file, 'r') as f:
                    try:
                        data = await f.read()
                        return json.loads(data)
                    except json.JSONDecodeError:
                        return {}
            return {}

    async def save_cookies(self):
        async with self.lock:
            cookies = {name: morsel.value
                       for name, morsel in self.session.cookie_jar.filter_cookies('https://www.paypal.com').items()}
            async with aiofiles.open(self.cookie_file, 'w') as f:
                await f.write(json.dumps(cookies, indent=2))

    
    
    async def init_session(self, max_retries=MAX_RETRIES):
        if not self.cookies_init_session:
            self.cookies_init_session = await self.load_cookies()
        self.cookies_init_session.pop("nsid", None)
        
        
        try:
            async with self.session.get(
                f'{self.domain}/signin',
                cookies=self.cookies_init_session,
                headers=self.headers_init_session,
                proxy=self.proxy,
                timeout=TIMEOUT_PROXY
            ) as response:
                
                if response.status != 200:
                    print(f"Request failed with status {response.status}. Retrying...")
                    return False
                data = await response.text()
                soup = BeautifulSoup(data, 'html.parser')
                token_input = soup.find('input', id='token')
                token_value = token_input.get('value') if token_input else None

                if token_value:
                    self.token = token_value
                    # print(f"Token găsit: {token_value}")
                    await self.save_cookies()
                    return True
                else:
                    print("Token nu a fost găsit în pagina de autentificare.")
                    return False
        except Exception as e:
            return False


        



    async def check_phone(self, max_retries=MAX_RETRIES):
            try:
                headers = {
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.paypal.com',
                    'referer': 'https://www.paypal.com/signin?locale.x=en_CA',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.11',
                    'x-requested-with': 'XMLHttpRequest',
                }

                params = {'locale.x': 'en_CA'}
                nr = self.number  # folosește numărul real
                data = f'isSafariAutofill=false&_csrf={self.token}&locale.x=en_US&processSignin=main&intent=signin&ads-client-context=signin&isValidCtxId=&coBrand=us&signUpEndPoint=%2Fwebapps%2Fmpp%2Faccount-selection&showCountryDropDown=true&usePassKey=true&requestUrl=%2Fsignin%3Flocale.x%3Den_CA&forcePhonePasswordOptIn=&captchaCode=&login_phone={nr}&initialSplitLoginContext=inputEmail&isTpdOnboarded=&captcha=&splitLoginContext=inputPhone&allowPasskeyAutofill=true&isInIframe=false&passkeyAutoUpgradeEligible=true&phoneCode=US%20%2B1&_sessionID=null'
                async with self.session.post(
                    f'{self.domain}/signin',
                    headers=headers,
                    proxy=self.proxy,
                    timeout=TIMEOUT_PROXY,
                    params=params,
                    data=data
                ) as r:
                    if r.status != 200:
                        print(f"Request failed with status {r.status} while checking phone.")
                        return False
                    else:
                        response = await r.text()
                        if 'htmlResponse' in response:
                            print("Captcha or block detected — switching proxy...")
                            return False
                        elif 'cdnHostName' in response:
                            data_json = json.loads(response)
                            split_login = data_json.get('splitLoginContext', '')
                            print(f"Split login context: {split_login}")
                            return split_login
                        else:
                            print(f"Response:\n{response}")
                            return False

            except Exception as e:
                print(f"❌ Error checking {self.number}: {e}. Retrying...")
                return False
            

        


    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()



    async def run(self):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                await self.set_proxy()
                await self.init_session()
                nr = await self.check_phone()
                if nr != False:
                    if nr == 'inputPassword':
                        print(f'{Fore.GREEN}{self.number} Phone is valid {Fore.RESET}')
                        with open('valid.txt', 'a', encoding='utf-8' ) as f:
                            f.write(f'{self.number}\n')
                    elif nr == 'inputEmail':
                        print(f'{Fore.RED}{self.number} Phone is invalid  {Fore.RESET} ')
                        with open('invalid.txt', 'a', encoding='utf-8' ) as f:
                            f.write(f'{self.number}\n')
                    return

            except Exception as e:
                print(f"{rest_INFO(TYPE='ERROR')} {Fore.RED}Eroare la procesarea numărului {self.number}: {e}{Fore.RESET}")
                retries += 1
        await self.close()
# Exemplu de rulare
# asyncio.run(Client("12345:5551234567").run())
