# Guía de instalación y uso para el cuaderno automático

Esta guía explica, paso a paso, cómo cualquier persona puede instalar el programa, abrirlo y convertir un audio de clase en apuntes listos para revisar en Obsidian. No necesitas saber usar la terminal ni instalar herramientas adicionales: todo viene incluido en el paquete.

---

## 0. ¿Cómo descargo el paquete `.zip`?

Si alguien ya te envió el archivo por correo o en una memoria USB, puedes saltar al paso siguiente. Si todavía no tienes el `.zip`, sigue estos pasos para descargarlo desde GitHub:

1. Abre tu navegador y entra al enlace que te compartieron (normalmente será algo como `https://github.com/<equipo>/<proyecto>/releases`).
2. Busca la sección **Latest release** (Última versión).
3. Dentro de **Assets** (Archivos incluidos) haz clic en el archivo que termina en `.zip`, por ejemplo `CuadernoAutomatico-portable.zip`.
4. El navegador comenzará la descarga. Cuando termine, verás el archivo en la carpeta **Descargas**.
5. Si Windows pregunta si quieres conservar el archivo, elige **Conservar** o **Mantener de todos modos**. Es seguro.

> Consejo: si compartes el enlace con otra persona, envíale directamente la URL de la sección de releases para que también pueda descargar la versión más reciente.

---

## 1. ¿Qué recibirás?

Alguien te compartirá un archivo `.zip` llamado por ejemplo `CuadernoAutomatico.zip`. Dentro del `.zip` ya vienen:

- `CuadernoAutomatico.exe`: el programa principal con la interfaz gráfica.
- Una carpeta `bundled/` con LM Studio y Obsidian configurados para funcionar con el programa.
- El archivo `plantilla.env` con las opciones básicas ya listas.
- Un archivo `LEEME.txt` con un recordatorio breve.

> Si te entregaron una memoria USB, probablemente el contenido ya esté descomprimido. En ese caso puedes saltar directamente al paso 3.

---

## 2. Requisitos de tu computadora

- **Sistema operativo:** Windows 10 o Windows 11 de 64 bits.
- **Espacio libre:** al menos 10 GB para guardar los audios, modelos y notas.
- **Permisos:** necesitarás aceptar que Windows ejecute aplicaciones descargadas. La primera vez puede pedir confirmación del Firewall.

No necesitas instalar Python, Docker ni LM Studio: el paquete ya incluye todo para que funcione.

---

## 3. Instalar el programa (solo una vez)

1. **Descarga o copia** el archivo `CuadernoAutomatico.zip` a tu computadora.
2. **Haz clic derecho** sobre el archivo y elige **Extraer todo...**.
3. Selecciona una carpeta fácil de recordar, por ejemplo `Documentos\CuadernoAutomatico`, y pulsa **Extraer**.
4. Dentro de la carpeta extraída verás varios archivos y carpetas. A partir de ahora siempre entrarás allí para abrir el programa.

> Consejo: crea un acceso directo a `CuadernoAutomatico.exe` en tu escritorio para tenerlo a mano.

---

## 4. Primer inicio del programa

1. Abre la carpeta donde extrajiste el contenido y haz doble clic en `CuadernoAutomatico.exe`.
2. Windows puede mostrarte una ventana de seguridad. Pulsa **Más información** y luego **Ejecutar de todas formas**.
3. Aparecerá la ventana **"Asistente automático de apuntes"**. Tardará unos segundos en revisar o encender los servicios internos:
   - El panel derecho mostrará el estado de **LM Studio**, **Docker** y **Obsidian**. Cuando se vean en verde significa que todo está listo.
   - El registro inferior irá mostrando mensajes como "Iniciando LM Studio" o "LM Studio en ejecución".
4. Cuando todos los servicios estén en verde, el botón **Generar apuntes automáticos** quedará habilitado.

La primera vez puede tardar algunos minutos mientras se descargan modelos y se prepara el entorno. En los siguientes usos será mucho más rápido.

---

## 5. Procesar tu primer audio

1. Pulsa el botón **Buscar** y selecciona el archivo de audio (mp3, wav, m4a, etc.).
2. Ajusta si quieres el **Título** de la nota y la **Fecha** de la clase.
3. Revisa la carpeta donde se guardarán las notas en el campo **Carpeta de notas**. Por defecto es `notas`, dentro de la carpeta del programa.
4. Presiona **Generar apuntes automáticos**.
5. Observa el registro inferior: verás mensajes sobre la transcripción, la generación del resumen y el guardado de archivos.
6. Al terminar, Obsidian se abrirá automáticamente mostrando la nota creada (si decides cerrar Obsidian, la nota seguirá guardada en la carpeta).

---

## 6. ¿Dónde quedan tus apuntes?

Dentro de la carpeta del programa encontrarás la subcarpeta `notas/`. Ahí se ordenan los archivos por año y mes:

```
notas/
 └── 2024/
     └── 05/
         ├── 2024-05-20-algebra-lineal.md      ← Resumen de la clase
         └── transcripciones/
             └── 2024-05-20-algebra-lineal.md  ← Transcripción detallada
```

Puedes abrir `notas/` con Obsidian en cualquier momento, incluso sin ejecutar el programa, para revisar o editar tus apuntes.

---

## 7. Agregar nuevos audios en el futuro

Cada vez que quieras procesar un audio nuevo solo necesitas:

1. Colocar el archivo de audio en cualquier carpeta de tu preferencia.
2. Abrir `CuadernoAutomatico.exe`.
3. Repetir los pasos de la sección **Procesar tu primer audio**.

No hace falta reinstalar nada ni volver a configurar el programa.

---

## 8. Personalizar la configuración (opcional)

Si quieres cambiar la carpeta donde se guardan las notas o ajustar el idioma del modelo de transcripción, puedes editar el archivo `plantilla.env`.

1. Haz clic derecho sobre `plantilla.env` y ábrelo con **Bloc de notas**.
2. Cada línea tiene el formato `CLAVE=valor`. Modifica solo la parte después del signo igual.
   - `NOTES_ROOT`: ruta donde se guardarán las notas. Puedes poner por ejemplo `D:\Apuntes`. Asegúrate de que la ruta exista.
   - `WHISPER_LANGUAGE`: idioma principal del audio (`es` para español, `en` para inglés, etc.).
   - `LM_STUDIO_MODEL`: nombre del modelo que se usará para generar los resúmenes. En el paquete viene uno preconfigurado.
3. Guarda los cambios y cierra el Bloc de notas.
4. La próxima vez que abras `CuadernoAutomatico.exe`, el programa aplicará la nueva configuración automáticamente.

> Cambia estos valores solo si sabes lo que haces. El archivo ya está preparado para funcionar sin modificaciones.

---

## 9. Solución rápida a problemas comunes

| Problema | Qué hacer |
| --- | --- |
| El programa no abre y Windows muestra un mensaje de seguridad | Pulsa **Más información** → **Ejecutar de todas formas**. Si vuelve a aparecer, marca la casilla "No volver a preguntar". |
| El panel indica que LM Studio no inicia | Cierra el programa, espera 10 segundos y vuelve a abrirlo. Si persiste, entra a la carpeta `bundled/lm-studio` y ejecuta `LM Studio.exe` manualmente una vez. |
| Las notas no aparecen en Obsidian | Abre Obsidian, selecciona **Abrir carpeta como vault** y elige la carpeta `notas` dentro del programa. |
| El procesamiento tarda demasiado | Archivos de más de 1 hora pueden tardar varios minutos. Déjalo trabajando; la barra de progreso avanza a medida que se completa cada paso. |
| Quiero cambiar la ubicación de las notas | Edita `plantilla.env` y ajusta `NOTES_ROOT` a la ruta deseada. Luego vuelve a abrir el programa. |

---

## 10. Necesito ayuda adicional

Si te compartieron el programa, contacta a la persona que lo preparó y coméntale el problema exacto. También puedes revisar el archivo `LEEME.txt` incluido en el paquete para un recordatorio rápido de los pasos principales.

¡Listo! Con estos pasos cualquier persona puede descargar, instalar y comenzar a generar apuntes automáticos a partir de sus audios de clase.
# Automatización de apuntes con audio, LM Studio y Obsidian

Este proyecto permite convertir automáticamente cualquier archivo de audio en apuntes listos para Obsidian. La automatización corre en un contenedor Docker, transcribe el audio con Whisper (vía `faster-whisper`) y solicita a un modelo alojado en [LM Studio](https://lmstudio.ai/) que genere:

- Avances cubiertos en la clase.
- Tareas asignadas y pendientes.
- Preguntas relevantes para un examen.

El resultado se guarda como notas Markdown ordenadas por fecha dentro de un "cuaderno" (vault) que puedes abrir con Obsidian.

La interfaz gráfica incluida verifica y arranca automáticamente todos los servicios necesarios (LM Studio, contenedores Docker y Obsidian portable) para que una persona sin conocimientos técnicos solo tenga que abrir el ejecutable, escoger un audio y pulsar **Generar apuntes automáticos**.

## Requisitos previos

### Para construir o ejecutar en modo desarrollo

1. **Docker y Docker Compose** instalados en tu sistema.
2. **LM Studio** en tu equipo local, con el servidor OpenAI-compatible habilitado.
3. **Obsidian** si deseas abrir el vault generado directamente en tu máquina.
4. (Opcional) GPU compatible para acelerar la transcripción; por defecto se usa CPU.

### Para la persona que recibe el ejecutable portable

- Ninguno: el `.zip` generado incluye los binarios portables de LM Studio y Obsidian junto con la automatización. Solo necesita descomprimirlo y abrir `CuadernoAutomatico.exe`.

## Requisitos previos

1. **Docker y Docker Compose** instalados en tu sistema.
2. **LM Studio** en tu equipo local, con el servidor OpenAI-compatible habilitado.
3. **Obsidian** para abrir la carpeta `data/notes` como vault.
4. (Opcional) GPU compatible para acelerar la transcripción; por defecto se usa CPU.

## Preparación del entorno

1. Clona este repositorio y entra al directorio.
2. Crea tu archivo `.env` a partir del ejemplo. Puedes hacerlo de dos formas:
   - **Sin usar la terminal**: copia el archivo `.env.example`, pégalo en la misma carpeta y renómbralo como `.env`.
   - **Con la terminal**:
     ```bash
     cp .env.example .env
     ```
3. Abre el nuevo `.env` y ajusta las variables según tus necesidades:
   - `LM_STUDIO_BASE_URL`: apunta al servidor iniciado desde LM Studio. Si corres Docker en Linux, el valor `http://host.docker.internal:1234/v1` funciona al agregar el `extra_hosts` incluido en `docker-compose.yml`.
   - `LM_STUDIO_MODEL`: nombre exacto del modelo cargado en LM Studio.
   - Parámetros de Whisper (`WHISPER_MODEL_SIZE`, `WHISPER_COMPUTE_TYPE`, `WHISPER_LANGUAGE`).
   - `NOTES_ROOT`: carpeta donde se guardarán las notas. Si usarás Docker deja `/app/notes`; para la interfaz gráfica local puedes usar `data/notes` o elegir cualquier ruta en tu equipo.
   - `AUTO_BOOTSTRAP_SERVICES` y `LM_STUDIO_START_COMMAND`: permiten que la app intente arrancar LM Studio y Docker por ti (útil para la versión empaquetada).
   - `OBSIDIAN_EXECUTABLE` y `AUTO_OPEN_OBSIDIAN`: controlan la apertura automática del vault cuando termina el procesamiento.
2. Crea tu archivo `.env` a partir del ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Ajusta las variables según tus necesidades:
   - `LM_STUDIO_BASE_URL`: apunta al servidor iniciado desde LM Studio. Si corres Docker en Linux, el valor `http://host.docker.internal:1234/v1` funciona al agregar el `extra_hosts` incluido en `docker-compose.yml`.
   - `LM_STUDIO_MODEL`: nombre exacto del modelo cargado en LM Studio.
   - Parámetros de Whisper (`WHISPER_MODEL_SIZE`, `WHISPER_COMPUTE_TYPE`, `WHISPER_LANGUAGE`).
   - `NOTES_ROOT`: ruta dentro del contenedor donde se escribirán las notas (ya mapeada a `./data/notes`).

4. Inicia LM Studio, carga el modelo deseado y habilita el **Local Inference Server** (menú *Developer -> Local Server*) en el puerto configurado en el `.env`.

## Estructura de carpetas

- `data/audio`: coloca aquí los audios de tus clases.
- `data/notes`: Obsidian puede abrir esta carpeta como vault. Dentro se generarán subcarpetas por año, mes y las transcripciones.
- `data/cache`: se usa para cachear modelos de Whisper y acelerar futuras transcripciones.

Estas carpetas se crean automáticamente, pero puedes ajustarlas en `docker-compose.yml`.

## Primeros pasos sin usar la terminal (interfaz gráfica)

Pensado para cualquier persona que prefiera dar clics en lugar de escribir comandos:

1. Instala [Python 3.10 o superior](https://www.python.org/downloads/) y asegúrate de marcar la opción **Add Python to PATH** durante la instalación (en Windows). En macOS o Linux ya suele venir instalado.
2. Completa la sección anterior de **Preparación del entorno** para dejar listo tu archivo `.env`. Si defines `AUTO_BOOTSTRAP_SERVICES=true` y `LM_STUDIO_START_COMMAND`, la aplicación intentará iniciar LM Studio y Docker por ti; de lo contrario, enciende esos servicios manualmente antes de continuar.
3. Abre la carpeta del proyecto y ejecuta la interfaz:
   - En **Windows**, haz doble clic en `start_gui.bat`. El script instalará automáticamente las dependencias necesarias y abrirá la ventana de la aplicación.
   - En **macOS o Linux**, abre una terminal únicamente para este paso, ejecuta `python3 -m pip install -r requirements.txt` la primera vez y luego `python3 main.py --gui` (puedes crear un alias o acceso directo para no repetir el comando).
4. En la ventana "Asistente automático de apuntes":
   - Observa el panel derecho; mostrará el estado de LM Studio, Docker y Obsidian en tiempo real.
2. Completa la sección anterior de **Preparación del entorno** para dejar listo tu archivo `.env` y haber iniciado el servidor local de LM Studio con el modelo deseado.
3. Abre la carpeta del proyecto y ejecuta la interfaz:
   - En **Windows**, haz doble clic en `start_gui.bat`. El script instalará automáticamente las dependencias necesarias y abrirá la ventana de la aplicación.
   - En **macOS o Linux**, abre una terminal únicamente para este paso, ejecuta `python3 -m pip install -r requirements.txt` la primera vez y luego `python3 main.py --gui` (puedes crear un alias o acceso directo para no repetir el comando).
4. En la ventana "Cuaderno automático de clases":
   - Pulsa **Buscar** para elegir el archivo de audio en cualquier carpeta.
   - Cambia el **Título** o la **Fecha** si lo necesitas.
   - Revisa la **Carpeta de notas** donde se guardarán los apuntes (por defecto `data/notes`). Puedes elegir otra ubicación con **Elegir carpeta**.
   - Marca "Omitir resumen" solo si no quieres llamar a LM Studio y prefieres conservar únicamente la transcripción.
5. Pulsa **Generar apuntes automáticos** y espera. El registro inferior te mostrará cada paso (carga del modelo, transcripción, resumen, guardado).
6. Al finalizar se abrirá Obsidian (si se configuró `AUTO_OPEN_OBSIDIAN=true`) y la carpeta que contiene la nota y la transcripción completa.
5. Pulsa **Generar apuntes** y espera. El registro inferior te mostrará cada paso (carga del modelo, transcripción, resumen, guardado).
6. Al finalizar se abrirá automáticamente la carpeta que contiene la nota y la transcripción completa para que la agregues a tu vault de Obsidian.

> Consejo: crea un acceso directo a `start_gui.bat` (Windows) o un alias que ejecute `python3 main.py --gui` (macOS/Linux) para iniciar la app con doble clic siempre que tengas un nuevo audio.

## Crear un ejecutable `.exe` listo para compartir

Para entregar una experiencia "descargar y usar" debes incluir las versiones portables de LM Studio, Obsidian y cualquier otro recurso necesario dentro del paquete. El script `packaging/windows/package_windows.bat` prepara todo automáticamente siempre que coloques dichos recursos en `packaging/windows/bundled/`.

1. **Prepara los binarios portables**:
   - Descarga la versión portable de [LM Studio](https://lmstudio.ai/) y cópiala dentro de `packaging/windows/bundled/lm-studio/`.
   - Descarga [Obsidian portable](https://obsidian.md/download) y cópiala dentro de `packaging/windows/bundled/obsidian/`.
   - Coloca cualquier otro recurso adicional (modelos predescargados, scripts personalizados, etc.) dentro de `packaging/windows/bundled/`.
2. Revisa `.env.windows.example` y ajusta los valores por defecto que heredará la persona usuaria. El script copiará automáticamente ese archivo como `plantilla.env` en el directorio final.
3. Abre una terminal de Windows (símbolo del sistema) y navega a la carpeta del proyecto.
4. Ejecuta el script de empaquetado:
Si quieres entregar la aplicación a alguien que solo necesite descargarla y abrirla, puedes generar una versión portable para Windows usando PyInstaller. Dentro del repositorio se incluye el script `packaging/windows/package_windows.bat` que automatiza todo el proceso:

1. Abre una terminal de Windows (símbolo del sistema) y navega a la carpeta del proyecto.
2. Ejecuta el script:

   ```bat
   packaging\windows\package_windows.bat
   ```

   El script creará un entorno virtual temporal, instalará PyInstaller, compilará el ejecutable y copiará `docker-compose.yml`, `plantilla.env`, `LEEME.txt` y la carpeta `bundled/` con los recursos portables a `dist/CuadernoAutomatico/`.

5. Comprueba el resultado abriendo `dist/CuadernoAutomatico/CuadernoAutomatico.exe`. Verás que el panel de servicios cambia a verde tras iniciar LM Studio y Docker embebidos.
6. Comprime la carpeta `dist/CuadernoAutomatico` para compartirla. Quien la reciba solo tendrá que descomprimirla, revisar (si desea) el `.env` y ejecutar `CuadernoAutomatico.exe`.

> Consejo: prueba el paquete en una máquina o usuario diferente antes de distribuirlo para verificar permisos de firewall y rutas relativas.
   El script creará un entorno virtual temporal, instalará PyInstaller, construirá el ejecutable y colocará el resultado en `dist/CuadernoAutomatico/` junto con un archivo `plantilla.env` y una guía `LEEME.txt` para la persona que lo reciba.

3. Comprime la carpeta `dist/CuadernoAutomatico` y compártela. Indica a quien la reciba que:
   - Copie `plantilla.env` como `.env` (en la misma carpeta) y edite los valores si necesita cambiar el puerto/modelo de LM Studio.
   - Abra `CuadernoAutomatico.exe` para acceder a la interfaz gráfica sin instalar Python.

> Sugerencia: antes de compartir, prueba el `.exe` en otra carpeta para comprobar que crea la subcarpeta `notes` y que puede comunicarse con tu instancia de LM Studio.

## Uso desde la terminal con Docker

1. Asegúrate de que las carpetas compartidas existen (se crean automáticamente al correr Docker, pero puedes anticiparte):

   ```bash
   mkdir -p data/audio data/notes data/cache
   ```

2. Copia tu archivo de audio (mp3, wav, m4a, etc.) a `data/audio/`.
3. Ejecuta el contenedor con Docker Compose, indicando la ruta del audio dentro del contenedor (`/app/audio/...`):
## Uso básico

1. Copia tu archivo de audio (mp3, wav, m4a, etc.) a `data/audio/`.
2. Ejecuta el contenedor con Docker Compose, indicando la ruta del audio dentro del contenedor (`/app/audio/...`):

   ```bash
   docker compose run --rm class-notes /app/audio/mi_clase.mp3 --title "Álgebra Lineal" --date 2024-05-20
   ```

   Argumentos principales:
   - `--title`: nombre de la clase. Se usa para generar el slug del archivo.
   - `--date`: fecha de la clase en formato `YYYY-MM-DD`. Si se omite se usa la fecha actual.
   - `--notes-root`: sobrescribe el destino de las notas si deseas guardarlas en otra carpeta.
   - `--skip-summary`: salta la llamada a LM Studio y solo crea la transcripción.

4. Una vez finalizado, abre Obsidian y selecciona la carpeta `data/notes` como vault. Encontrarás:
3. Una vez finalizado, abre Obsidian y selecciona la carpeta `data/notes` como vault. Encontrarás:
   - Notas por fecha en `data/notes/<año>/<mes>/<fecha>-<slug>.md` con el resumen.
   - Transcripciones detalladas en `data/notes/<año>/<mes>/transcripciones/` con tablas por segmento.

## Flujo de trabajo sugerido

1. **Graba tu clase** y guarda el audio en cualquier formato común.
2. **Mueve el archivo** a la carpeta compartida (`data/audio`).
3. **Corre el contenedor** para transcribir y resumir.
4. **Revisa y complementa** los apuntes en Obsidian. Cada nota enlaza al archivo de transcripción completa.
5. **Consulta las tareas y preguntas** preparadas automáticamente para tu seguimiento.

## Personalización

- Ajusta el prompt en `app/summarizer.py` si necesitas otro formato de salida.
- Modifica las plantillas Markdown en `app/note_writer.py` para adaptarlas a tu estilo de Obsidian.
- Cambia el tamaño del modelo de Whisper desde el `.env` (`tiny`, `base`, `small`, `medium`, `large-v2`). Modelos más grandes ofrecen mejor calidad a costa de más tiempo.

## Ejecución sin Docker

Si prefieres correrlo directamente en tu máquina:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py ruta/al/audio.mp3 --title "Mi clase" --date 2024-05-20
```

Asegúrate de tener `ffmpeg` instalado y de exportar las variables necesarias.

### Ejecución paso a paso (referencia rápida)

1. Inicia LM Studio y habilita el servidor local compatible con OpenAI.
2. Ajusta el archivo `.env` con la URL del servidor, el nombre del modelo y los parámetros de Whisper.
3. Copia el audio a `data/audio/`.
4. Corre `docker compose run --rm class-notes /app/audio/<archivo>` con los argumentos necesarios.
5. Abre `data/notes` con Obsidian para revisar el resumen y la transcripción.

## Solución de problemas

- **El contenedor no alcanza a LM Studio**: verifica que el servidor local esté activo y accesible. En Linux puede ser necesario editar `docker-compose.yml` para apuntar al IP de tu host.
- **Transcripción lenta**: cambia a un modelo más pequeño (`WHISPER_MODEL_SIZE=tiny`) o habilita GPU en el contenedor ajustando el `docker-compose.yml` según tu plataforma.
- **Obsidian no ve las notas**: confirma que estés abriendo la carpeta correcta (`data/notes`) y que los archivos `.md` se hayan generado.

Con esta automatización tendrás un cuaderno digital actualizado automáticamente a partir de tus audios de clase, listo para revisar en cualquier momento.

