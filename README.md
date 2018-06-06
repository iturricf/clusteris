# Algoritmos Genéticos para el Análisis de Clusters

Este trabajo consiste en implementar algoritmos genéticos que permitan encontrar clusters en bases de datos.

## Requirements:

* Python 2.7.12
* Python PIP
* Linux 64-bits o Microsoft Windows 10

Además de las siguientes especificadas en el archivo requirements.txt

## Instalación

### Linux

Dentro del directorio del código fuente

 * Instalar python: `sudo apt-get install python2.7`
 * Instalar python-pip: `sudo apt-get install python-pip`
 * Instalar dependencias de la aplicación: `sudo pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 -r requirements.txt`

### Windows

 * Instalar python v2.7.10 64bits (provisto con los instaladores)
 * Instalar wxPython
 * Verificar que el interpreter python.exe y pip.exe esten en el path de ejecutables
 * Instalar dependencias de la aplicación: `pip install -r requirements.txt`

## Ejecución

### Linux

Dentro del directorio clusteris

```python clusteris.py```

### Windows

Ejecutar el lanzador clusteris.exe

Alternativamente se pude ejecutar el lanzador `program.bat` en el directorio código fuente


## Uso

1 - Abrir el dataset a procesar desde el menú `Archivo` -> `Abrir dataset`
2 - Procesar el dataset cargado desde el menú `Procesamiento` -> `Procesar dataset`
3 - Seleccionar opciones de procesamiento y luego el botón `Procesar`
4 - Se puede exportar el resultado a un archivo csv desde el menú `Archivo` -> `Exportar como CSV`
5 - Se puede exportar el gráfico como una imagen desde el menú `Archivo` -> `Exportar como imagen`
