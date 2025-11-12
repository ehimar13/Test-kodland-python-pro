# Test-kodland-python-pro
En este repositorio se encuentra el proyecto / bot que le permite al usuario escoger cartas pokemon, ver su inventario, ver la estadistica de sus cartas y el ranking de las cartas.
---
## Requisitos
- Tener cuenta de discord . https://discord.com/
- Crear una apllicacion en el portal de desarrolladores de discord  https://discord.com/developers/applications
- Invitar el bot a tu servidor con los permisos correspondientes.

## Instalacion.
1. Descarga repositorio en formato .zip 
2. Asegúrate de tener Python 3.10+ instalado en tu ID o computadora
3. Abre una terminal dentro de la carpeta del proyecto dando click derecho en la carpeta
4. Instala los requerimientos necesarios con: pip install -r requirements.txt
5. Configura el archivo config.py con tu token de Discord: python TOKEN = "escribe_tu_token" (se obtiene de la pagian de discord developer https://discord.com/developers/applications)
6. Ejecuta el bot con:  python main.py

## Comandos del bot.
se configuro para que los comandos funcionen de esta forma !comando  

| `!pokem`   | Sacar carta aleatoria y guardarla  |  

| `!inve`    | Ver tu inventario interactivo      |  

| `!stats`   | Ver estadísticas de tus cartas     |  

| `!ranking` | Ver ranking global de cartas raras |  

los elementos se guardan en un archivo llamado inventario con el fin de que el usuario del bot pueda almecenar sus cartas

## Archivos.
- main.py --> Codigo principal del bot
- config.py --> contiene el token que debe ingresar el usuario
- requirements.txt --> lista de requerimientos necesarios para que funcione el bot.
- inventario.json --> generado por el programa para almacenar la informacion del usuario.

