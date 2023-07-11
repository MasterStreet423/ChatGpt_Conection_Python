# Documentación del código
 Este código es un script de Python que utiliza la biblioteca Playwright para interactuar con la página web de OpenAI. El script inicia un navegador, navega a la página de OpenAI, acepta las políticas y luego interactúa con la interfaz de usuario de la página para hacer peticiones a la API de OpenAI.
 ## Bibliotecas utilizadas
 - **playwright**: Permite automatizar la interacción con los navegadores web.
- **tabulate**: Ayuda a crear tablas bonitas y fáciles de leer.
- **os**: Proporciona funciones para interactuar con el sistema operativo.
- **atexit**: Permite definir funciones de limpieza que deben ser ejecutadas cuando el programa termina.
- **Data**: Un archivo local del que se importan algunas constantes y funciones.
 ## Funciones y Clases
 ### init()
 Esta función inicializa el navegador Playwright y lanza una nueva instancia del navegador en modo headless (sin interfaz gráfica). También limpia las cookies del navegador.
 ### ChatGpt
 Esta es la clase principal que se utiliza para interactuar con la API de OpenAI.
 #### `__init__(self, prompt="", lnk="https://chat.openai.com/", repeat_prompt=False) `
 Este es el constructor de la clase. Inicializa varias variables de instancia y registra la función ` stop ` para ser llamada cuando el programa termine.
 #### ` run(self) `
 Esta función inicia la interacción con la página de OpenAI. Añade las cookies al navegador, abre una nueva página, establece las cabeceras HTTP, navega a la página de OpenAI, acepta las políticas y luego hace una petición inicial a la API de OpenAI.
 #### ` get_request(self) `
 Esta función obtiene la respuesta de la API de OpenAI. Analiza el contenido de la página para extraer la respuesta en texto.
 #### ` peticion(self, Question) `
 Esta función hace una petición a la API de OpenAI. Escribe la pregunta en el área de texto de la página y luego presiona la tecla Enter.
 #### ` stop(self) `
 Esta función detiene la interacción con la página de OpenAI. Cierra la página y el navegador.
 ## Uso
 Para usar este script, simplemente importa la clase ` ChatGpt`, crea una instancia de la clase y luego llama a sus métodos. Por ejemplo:

```python
from script import ChatGpt
 chat = ChatGpt(prompt="Hola, soy un bot.")
chat.run()
respuesta = chat.peticion("¿Cómo estás?")
print(respuesta)
chat.stop()
```

Este script es una forma eficiente de interactuar con la API de OpenAI sin tener que lidiar con las solicitudes HTTP y el manejo de cookies.