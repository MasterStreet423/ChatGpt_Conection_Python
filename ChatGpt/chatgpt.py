from playwright.sync_api import sync_playwright
import tabulate
import os
import atexit
from .Data import *

def init():
    global playwright,selected_browser,browser,f_time
    # Inicializa el navegador Playwright
    playwright = sync_playwright().start()
    selected_browser = playwright.firefox
    # Lanza una nueva instancia del navegador en modo headless (sin interfaz gráfica)
    f_time = not os.path.isdir(os.path.join(os.getcwd(), "ChatGpt/cache_gpt"))
    browser = selected_browser.launch_persistent_context(
        os.path.join(os.getcwd(), "ChatGpt/cache_gpt"),headless=not f_time
    )


class ChatGpt:
    def __init__(
        self,
        prompt="",
        lnk="https://chat.openai.com/",
        repeat_prompt=False,
    ) -> None:
        self.link = lnk
        atexit.register(self.stop)
        self.peticions = 0
        self.prompt = prompt
        self.repeat_prompt = repeat_prompt
        self.running = False

    def run(self):
        # Añade las cookies al navegador y abre una nueva página
        self.page = browser.new_page()
        # Establece las cabeceras HTTP
        print("Accediendo a OpenAI..")
        # Bloquea las rutas de las hojas de estilo y la API de moderación
        if not f_time:
            self.page.route("**/*.css", lambda route: route.abort())
            self.page.route(
                "https://chat.openai.com/backend-api/moderations",
                lambda route: route.abort(),
            )
        # Navega a la página de OpenAI
        self.page.goto(self.link, wait_until="domcontentloaded")

        if f_time:
            self.page.wait_for_timeout(2000)
            print("Please login on Chat-Gpt, this is only first time")
            while self.page.url != "https://chat.openai.com/":
                self.page.wait_for_timeout(200)
            print("Login successfully")
            exit("Relaunch Program")

        # Define los selectores de los boto nes de politicas
        boton = '//*[@id="radix-:re:"]/div[2]/div[1]/div[2]/button'
        boton2 = '//*[@id="radix-:re:"]/div[2]/div[1]/div[2]/button[2]'
        print("Aceptando politicas..")
        trying = 0
        politics = False
        while True:
            try:
                self.page.wait_for_selector(f"xpath={boton}", timeout=500)
                politics = True
                break
            except:
                if trying > 4:
                    break
                trying += 1
                if trying % 2 == 0:
                    boton = boton.replace("re", "rd")
                    boton2 = boton2.replace("re", "rd")
                else:
                    boton = boton.replace("rd", "re")
                    boton2 = boton2.replace("rd", "re")
        if politics:
            button = self.page.locator(f"xpath={boton}")
            button.click()
            button = self.page.locator(f"xpath={boton2}")
            button.click()
            button = self.page.locator(f"xpath={boton2}")
            button.click()
        else:
            print("Politics Don't finded(Don't worry)")

        self.running = True
        if self.prompt != "":
            print("Dando personalidad..")
            try:
                self.page.wait_for_timeout(200)
                self.peticion(self.prompt)
                # print(self.get_request()["text"])
            except Exception as e:
                print(e)

    def get_request(self):
        t = (
            self.page.locator(f"xpath={GPTREQUEST}")
            .last.locator(f"xpath={CONTAINERTEXT}")
            .locator("xpath=*")
        )
        text = ""
        # LAS ANALIZO Y DEPENDIENDO DE LA RESPUESTA RESPONDE DE UNA U OTRA FORMA
        for x in range(t.count()):
            x = t.nth(x)
            Tn = x.evaluate("(e) => e.tagName")

            match Tn:
                case "P":
                    text += x.inner_text() + "\n\n"
                case "OL":
                    x = x.locator("li")
                    for i in range(x.count()):
                        li = x.nth(i)
                        itext = li.inner_text(timeout=5000)
                        text += f"\n{i+1}: {itext}\n"
                    text += "\n\n"
                case "UL":
                    x = x.locator("li")
                    for i in range(x.count()):
                        li = x.nth(i)
                        itext = li.inner_text(timeout=5000)
                        text += f"\n-. {itext}\n"
                    text += "\n\n"
                case "TABLE":
                    Headers = (
                        x.locator("xpath=thead/tr").all_inner_texts()[0].split("\t")
                    )
                    filas = x.locator("xpath=tbody/tr").all_inner_texts()
                    filas = list(map(lambda x: x.split("\t"), filas))

                    tabla = (
                        tabulate.tabulate(filas, Headers, "fancy_grid", maxcolwidths=40)
                        + "\n\n"
                    )
                    text += tabla
                case "PRE":
                    # Título de la ventana
                    try:
                        T = x.locator(".bg-black.rounded-md.mb-4").locator("span").first
                        Title = T.inner_text()
                        text += f"\n{Title}\n"
                    except:
                        text += "\nCodigo\n"
                    # Código
                    Code = (
                        x.locator(".bg-black.rounded-md.mb-4")
                        .locator("xpath=/*")
                        .all()[1]
                        .inner_text()
                    )
                    text += f"\n{Code}\n"
                case _:
                    print(f"soy un {Tn}")
        text = text.strip("\n\n")

        if text == "":
            self.peticion("regenerate")

        return text
    
    def peticion(self, Question):


        if not self.running:
            raise Exception("Chat Gpt not is running")
        
        entrada = self.page.query_selector("#prompt-textarea")

        if Question == "regenerate" and self.peticions > 0:
            self.check.first.click()
        else:
            entrada.fill(
                f"({self.prompt}){Question}" if self.repeat_prompt else Question
            )
            self.page.wait_for_timeout(100)
            entrada.focus()
            self.page.keyboard.press("Enter")
            self.peticions += 1

        
        self.check = self.page.locator(f"xpath={CHECKFULL}").locator("div")

        while self.check.inner_text().lower() != "regenerate response":
            self.page.wait_for_timeout(100)
            if self.check.count() > 1:
                self.check.nth(1).click()


        return self.get_request()

    def stop(self):
        if self.running:
            print("\reliminando chat de openai..")
            btn = self.page.query_selector_all("button.p-1.hover\\:text-white")
            if btn != []:
                btn[-1].click()
            else:
                print("Dont find button")
            btn = self.page.query_selector_all("button.p-1.hover\\:text-white")
            if btn != []:
                btn[0].click()
            else:
                print("Dont find button")
            print("chat eliminado")
            self.running = False
            self.page.close()
            browser.close()