===============================================
Cuaderno automatico de clases (versión portable)
===============================================

COMO DESCARGAR EL ARCHIVO .ZIP
-------------------------------
1. Abre en tu navegador el enlace de descargas del proyecto (por ejemplo `https://github.com/<equipo>/<proyecto>/releases`).
2. Busca la sección **Latest release** y dentro de **Assets** haz clic en el archivo que termina en `.zip`.
3. Guarda el archivo cuando el navegador te lo ofrezca. Estará en tu carpeta **Descargas**.
4. Si Windows te avisa que podría ser peligroso, elige **Conservar** o **Mantener de todos modos**.

INSTRUCCIONES RAPIDAS PARA LA PERSONA QUE RECIBE EL .ZIP
-------------------------------------------------------
1. Descomprime la carpeta completa donde prefieras (Documentos, Escritorio, etc.).
2. Copia el archivo "plantilla.env" como ".env" en la misma carpeta y, si lo necesitas, edítalo con el Bloc de notas.
   - Normalmente no hace falta cambiar nada: la app ya iniciará LM Studio, Docker y Obsidian usando los recursos incluidos.
3. Haz doble clic en "CuadernoAutomatico.exe". La primera vez puede tardar unos segundos mientras prepara los servicios.
4. Cuando veas la pantalla principal:
   - Arriba encontrarás el estado de LM Studio, Docker y Obsidian. Deben aparecer en verde antes de procesar un audio.
   - Pulsa **Buscar** para seleccionar tu archivo de clase.
   - Revisa o cambia la carpeta donde guardar las notas si lo deseas.
   - Pulsa **Generar apuntes automáticos** y espera a que finalice.
5. Al terminar se abrirá Obsidian (si está configurado como portable) y la carpeta `notes` con tus apuntes y transcripciones.

Si aparece un aviso del firewall, permite el acceso para que LM Studio y la aplicación se comuniquen en tu equipo.
