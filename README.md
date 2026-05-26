# Tarea 1 — Juego de la Vida de Conway

Implementacion en Python del Juego de la Vida de Conway para el curso de
Programacion Paralela y Distribuida (LEAD University).

## Requisitos

- Python 3.9 o superior
- Librerias listadas en `requirements.txt`

## Instalacion

```bash
python -m pip install -r requirements.txt
```

## Como ejecutar

### Demo animada de un patron clasico

```bash
python main.py demo --pattern glider --size 64 --steps 200
```

Patrones disponibles: `block`, `beehive`, `blinker`, `toad`, `beacon`,
`pulsar`, `glider`, `lwss`, `random`.

### Estado inicial aleatorio

```bash
python main.py demo --pattern random --size 128 --density 0.25 --steps 300
```

### Guardar la animacion como GIF

```bash
python main.py demo --pattern pulsar --size 32 --steps 60 --save salida.gif --no-show
```

### Benchmark de rendimiento

```bash
python main.py benchmark --sizes 32 64 128 256 512 1024 --iters 50
```

Comparar paralelo vs secuencial:

```bash
python main.py benchmark --sizes 64 128 256 512 1024 --iters 50 --compare
```

Los resultados (graficas) se guardan en la carpeta `resultados/`.

## Estructura del proyecto

```
juego_de_la_vida/
├── game_of_life.py     # Clase GameOfLife
├── patterns.py         # Patrones clasicos
├── visualization.py    # Animacion con matplotlib
├── benchmark.py        # Medicion de rendimiento
├── main.py             # CLI principal
├── requirements.txt    # Dependencias
└── resultados/         # Salidas generadas
```
