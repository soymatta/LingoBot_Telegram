# LingoBot

**LingoBot** es un bot de Telegram escrito en Python, diseñado para facilitar el aprendizaje de idiomas mediante traducciones personalizadas y un glosario descargable. Permite aprender un idioma desde uno o dos idiomas de referencia, ofrece palabras diarias (cuando tú lo desees) con ejemplos, y gestiona las palabras guardadas en formato CSV, brindando una experiencia práctica e interactiva.

## Características

- **Traducción de texto** en uno o dos idiomas de referencia.
- **Generación de palabra aleatoria** con su traducción y ejemplo de uso, solo cuando lo solicites.
- **Glosario personal** de palabras guardadas, descargable en formato CSV.
- **Configuración flexible** de idiomas de origen y destino.

## Comandos disponibles

### Comandos principales:

- `/start` - Inicia el bot y muestra el mensaje de bienvenida.
- `/menu` - Muestra el menú principal con todas las opciones disponibles.
- `/traductions` - Activa el modo de traducción de texto.
- `/random` - Genera una palabra aleatoria para practicar.
- `/glossary` - Muestra el glosario personal de palabras guardadas.
- `/viewconfig` - Muestra la configuración actual del bot.

### Comandos de configuración:

- `/changeorigin` - Cambia el idioma de origen para las traducciones.
- `/changetype` - Alterna entre traducción individual o simultánea.
- `/changedestiny` - Cambia el idioma de destino para las traducciones.

## Instalación

Para instalar y ejecutar LingoBot en tu entorno local, sigue estos pasos:

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/LingoBot.git
   cd LingoBot
   ```

2. **Crea un entorno virtual**:
   En el directorio del proyecto, crea un entorno virtual para aislar las dependencias.

   ```bash
   python3 -m venv venv
   ```

3. **Activa el entorno virtual**:

   - En **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - En **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Instala las dependencias**:
   Con el entorno virtual activado, instala las dependencias requeridas.

   ```bash
   pip install -r requirements.txt
   ```

5. **Configura tus credenciales de Telegram**:
   Crea un archivo `Telegram_Token.py` en el directorio raíz del proyecto para almacenar tu token de acceso de Telegram. Puedes hacerlo con el siguiente comando:

   ```bash
   echo 'PERSONAL_TOKEN = "AQUI VA TU TOKEN"' > Telegram_Token.py
   ```

   Reemplaza `"AQUI VA TU TOKEN"` por tu token real.

6. **Inicia el bot**:
   Ejecuta el archivo principal para iniciar el bot.
   ```bash
   python run_bot.py
   ```

## Uso

Una vez que el bot esté en funcionamiento, puedes interactuar con él a través de Telegram usando los comandos disponibles. Inicia el bot con `/start` para recibir una introducción y accede al menú principal con `/menu`.
