# Documentación del código
 Este código es un script de Python que utiliza la biblioteca Playwright para interactuar con la página web de OpenAI. El script inicia un navegador, navega a la página de OpenAI, acepta las políticas y luego interactúa con la interfaz de usuario de la página para hacer peticiones a la IA de OpenAI.
 
  Para usar el proyecto este debe estar en la misma carpeta que el archivo main, del cual se ejecutara el programa.

 No olvidar usar el 
 
 ```
 playwright install firefox
 ```
 
 para que funcione correctamente, en el caso de querer usar otro navegador reemplazar el `selected_browser` en la función init de "chatgpt.py"
 ## Bibliotecas utilizadas
 - **playwright**: Permite automatizar la interacción con los navegadores web.
- **tabulate**: Ayuda a crear tablas bonitas y fáciles de leer.
- **os**: Proporciona funciones para interactuar con el sistema operativo.
- **Data**: Un archivo local del que se importan algunas constantes.
 ## Funciones y Clases
 ### init()
 Esta función inicializa el navegador Playwright y lanza una nueva instancia del navegador en modo headless (sin interfaz gráfica).
 ### ChatGpt
 Esta es la clase principal que se utiliza para interactuar con la IA de OpenAI.
 #### `__init__(self, prompt="", lnk="https://chat.openai.com/", repeat_prompt=False) `
 Este es el constructor de la clase. Inicializa varias variables de instancia y registra la función ` stop ` para ser llamada cuando el programa termine.
 
 ##### prompt
 se refiere al mensaje inicial dado a la ia, muy util en el caso que se requiera dar algún tipo de personalidad

 ##### lnk(Link) 
 hace referencia a un chat pre-guardado, chatgpt permite reutilizar tus chats copiando el link al cual tenga al momento de cambiar de chat

 ##### repeat_prompt
  se refiere a que si quiere que el prompt inicial sea recordado a ChatGpt en  cada petición usando la sintaxis "(Prompt)(Petición)"
 ##### ` run(self) `
 Esta función inicia la interacción con la página de OpenAI. abre una nueva página, navega a la página de OpenAI, acepta las políticas y luego hace una petición inicial a la API de OpenAI.
 #### ` get_request(self) `
 Esta función obtiene la respuesta de la API de OpenAI. Analiza el contenido de la página para extraer la respuesta en texto.
 #### ` peticion(self, Question) `
 Esta función hace una petición a la pagina de ChatGpt. Escribe la pregunta en el área de texto de la página y luego presiona la tecla Enter.
 #### ` stop(self) `
 Esta función detiene la interacción con la página de OpenAI. Cierra la página y el navegador.
 ## Uso
 Para usar este script, simplemente importa la clase ` ChatGpt`, crea una instancia de la clase y luego llama a sus métodos. Por ejemplo:

```python
from ChatGpt import ChatGpt,init

init()
chat = ChatGpt(prompt="Hola, soy un bot.")
chat.run()
respuesta = chat.peticion("¿Cómo estás?")
print(respuesta)
chat.stop()
```

Este script es una forma eficiente de interactuar con la pagina de ChatGpt, ya que el navegador bloquea la carga de css, lo que acelera la carga en conexiones lentas, en solo un par de segundos ya se tiene una conexión establecida con ChatGpt(todo dependiendo de la conexión a internet que se posea) completamente gratis.