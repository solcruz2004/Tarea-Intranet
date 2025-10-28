# Guía de instalación y uso para el cuaderno automático

Esta guía explica, paso a paso, cómo cualquier persona puede instalar el programa, abrirlo y convertir un audio de clase en apuntes listos para revisar en Obsidian. No necesitas saber usar la terminal ni instalar herramientas adicionales: todo viene incluido en el paquete.

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
