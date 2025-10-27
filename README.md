# Automatización de apuntes con audio, LM Studio y Obsidian

Este proyecto permite convertir automáticamente cualquier archivo de audio en apuntes listos para Obsidian. La automatización corre en un contenedor Docker, transcribe el audio con Whisper (vía `faster-whisper`) y solicita a un modelo alojado en [LM Studio](https://lmstudio.ai/) que genere:

- Avances cubiertos en la clase.
- Tareas asignadas y pendientes.
- Preguntas relevantes para un examen.

El resultado se guarda como notas Markdown ordenadas por fecha dentro de un "cuaderno" (vault) que puedes abrir con Obsidian.

## Requisitos previos

1. **Docker y Docker Compose** instalados en tu sistema.
2. **LM Studio** en tu equipo local, con el servidor OpenAI-compatible habilitado.
3. **Obsidian** para abrir la carpeta `data/notes` como vault.
4. (Opcional) GPU compatible para acelerar la transcripción; por defecto se usa CPU.

## Preparación del entorno

1. Clona este repositorio y entra al directorio.
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

## Solución de problemas

- **El contenedor no alcanza a LM Studio**: verifica que el servidor local esté activo y accesible. En Linux puede ser necesario editar `docker-compose.yml` para apuntar al IP de tu host.
- **Transcripción lenta**: cambia a un modelo más pequeño (`WHISPER_MODEL_SIZE=tiny`) o habilita GPU en el contenedor ajustando el `docker-compose.yml` según tu plataforma.
- **Obsidian no ve las notas**: confirma que estés abriendo la carpeta correcta (`data/notes`) y que los archivos `.md` se hayan generado.

Con esta automatización tendrás un cuaderno digital actualizado automáticamente a partir de tus audios de clase, listo para revisar en cualquier momento.
