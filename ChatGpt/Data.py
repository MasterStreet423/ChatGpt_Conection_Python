PRIMERBOTON = '//*[@id="radix-:re:"]/div[2]/div[1]/div[2]/button'
SEGUNDOBOTON = '//*[@id="radix-:re:"]/div[2]/div[1]/div[2]/button[2]'
INPUTTEXT = '//*[@id="prompt-textarea"]'

GPTREQUEST = '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/div/div/div/div[position() mod 2 = 0]'
CONTAINERTEXT = '/div/div[2]/div[1]/div/div'


fTIME = False

CHECKFULL = '//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button'

stealth_js = '''() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
        window.navigator.chrome = {
            runtime: {},
        };
        delete window.navigator.__proto__.webdriver;
    }'''


