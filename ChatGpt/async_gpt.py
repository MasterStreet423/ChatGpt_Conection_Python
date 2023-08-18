from playwright.async_api import async_playwright
import tabulate
import os
from .Data import *


async def init():
    global playwright, selected_browser, browser, f_time
    # Inicializa el navegador Playwright
    playwright = await async_playwright().start()
    selected_browser = playwright.firefox
    # Lanza una nueva instancia del navegador en modo headless (sin interfaz gráfica)
    f_time = not os.path.isdir(os.path.join(os.getcwd(), "ChatGpt/cache_gpt"))
    browser = await selected_browser.launch_persistent_context(
        os.path.join(os.getcwd(), "ChatGpt/cache_gpt"), headless=not f_time
    )


class ChatGpt:
    def __init__(
        self,
        prompt="",
        lnk="https://chat.openai.com/",
        repeat_prompt=False,
    ) -> None:
        self.link = lnk
        self.peticions = 0
        self.prompt = prompt
        self.repeat_prompt = repeat_prompt
        self.running = False

    async def run(self):
        # abre una nueva página
        self.page = await browser.new_page()
        print("Accediendo a OpenAI..")
        # Bloquea las rutas de las hojas de estilo y la API de moderación
        if not f_time:
            await self.page.route("**/*.css", lambda route: route.abort())
            await self.page.route(
                "https://chat.openai.com/backend-api/moderations",
                lambda route: route.abort()
            )
        # Navega a la página de OpenAI

        if f_time:
            try:
                await self.page.goto(self.link, wait_until="commit")
                input("Please login on Chat-Gpt, this is only first time, press enter to continue..")


            except Exception as e:
                print(str(e))
                exit(
                    "Please Remove folder 'cache_gpt' from 'ChatGpt' folder to try login again"
                )
            print("Login successfully")
            exit("Relaunch Program")
        else:
            await self.page.goto(self.link, wait_until="domcontentloaded")
        # Define los selectores de los boto nes de politicas
        boton = PRIMERBOTON
        boton2 = SEGUNDOBOTON

        if not "login" in self.page.url:
            print("Aceptando politicas..")
        else:
            try:
                print("Please delete cache_gpt folder, session expired")
                await self.stop()
                

            except Exception as e:
                print(str(e))
                exit(
                    "Please Remove folder 'cache_gpt' from 'ChatGpt' folder to try login again"
                )
            exit("Relaunch Program")

        print("Aceptando politicas..")
        trying = 0
        politics = False
        while True:
            try:
                await self.page.wait_for_selector(f"xpath={boton}", timeout=500)
                politics = True
                break
            except Exception as e:
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
            await button.click()
            button = self.page.locator(f"xpath={boton2}")
            await button.click()
            button = self.page.locator(f"xpath={boton2}")
            await button.click()
        else:
            print("Politics Don't finded(Don't worry)")

        self.running = True
        if self.prompt != "":
            print("Prompt Inicial..")
            try:
                await self.page.wait_for_timeout(200)
                await self.peticion(self.prompt)
            except Exception as e:
                print(e)

    async def get_request(self):
        t = (
            self.page.locator(f"xpath={GPTREQUEST}")
            .last.locator(f"xpath={CONTAINERTEXT}")
            .locator("xpath=*")
        )
        text = ""
        # LAS ANALIZO Y DEPENDIENDO DE LA RESPUESTA RESPONDE DE UNA U OTRA FORMA
        for x in range(await t.count()):
            x = t.nth(x)
            Tn = await x.evaluate("(e) => e.tagName")

            match Tn:
                case "P":
                    text += await x.inner_text() + "\n\n"
                case "OL":
                    x = x.locator("li")
                    for i in range(await x.count()):
                        li = x.nth(i)
                        itext = await li.inner_text(timeout=5000)
                        text += f"\n{i+1}: {itext}\n"
                    text += "\n\n"
                case "UL":
                    x = x.locator("li")
                    for i in range(await x.count()):
                        li = x.nth(i)
                        itext = await li.inner_text(timeout=5000)
                        text += f"\n-. {itext}\n"
                    text += "\n\n"
                case "TABLE":
                    Headers = (
                        await x.locator("xpath=thead/tr").all_inner_texts()[0].split("\t")
                    )
                    filas = await x.locator("xpath=tbody/tr").all_inner_texts()
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
                        Title = await T.inner_text()
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
            await self.peticion("regenerate")

        return text

    async def peticion(self, Question):
        if not self.running:
            raise Exception("Chat Gpt not is running")

        entrada = await self.page.query_selector("#prompt-textarea")

        if Question == "regenerate" and self.peticions > 0:
            await self.check.first.click()
        else:
            await entrada.fill(
                f"({self.prompt}){Question}" if self.repeat_prompt else Question
            )
            await self.page.wait_for_timeout(100)
            await entrada.focus()
            await self.page.keyboard.press("Enter")
            self.peticions += 1

        self.check = self.page.locator(f"xpath={CHECKFULL}").locator("div")

        while (await self.check.inner_text()).lower() != "regenerate":
            await self.page.wait_for_timeout(100)
            if await self.check.count() > 1:
                await self.check.nth(1).click()

        return await self.get_request()

    async def stop(self):
        if self.running:
            eliminate = True
            try:
                print("\reliminando chat de openai..")
                btn = await self.page.query_selector_all("button.p-1.hover\\:text-white")
                if btn != []:
                    await btn[-1].click(timeout=1000)
                else:
                    eliminate = False
                btn = await self.page.query_selector_all("button.p-1.hover\\:text-white")
                if btn != []:
                   await btn[0].click(timeout=1000)
                else:
                    eliminate = False
                self.running = False
                await self.page.close()
                await browser.close()
            except:
                if not eliminate:
                    print("Error en borrado de chat")

    
    async def __aenter__(self):
        await init()
        await self.run()
        return self

    async def __aexit__(self,*args):
        await self.stop()