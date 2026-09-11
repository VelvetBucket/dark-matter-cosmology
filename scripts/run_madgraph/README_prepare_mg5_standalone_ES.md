# Script de Preparación del Standalone de MadGraph

**Autor:** Juan Diego Inga

## Descripción general

`prepare_mg5_standalone.py` es una herramienta en Python diseñada para preparar un output standalone C++ de MadGraph5_aMC@NLO a partir de:

1. un modelo UFO proporcionado por el usuario,
2. una lista de partículas Z2-impares (`odd particles`),
3. una instalación de MadGraph5_aMC,
4. y una carpeta de salida donde se guardará el standalone generado.

El objetivo de este script es actuar como puente entre el modelo físico proporcionado por el usuario y el resto del flujo de `dark-matter-cosmology`.

El script **no modifica la instalación de MadGraph**. En cambio, importa directamente el modelo UFO desde la ruta indicada por el usuario y le solicita a MadGraph generar la estructura C++ standalone correspondiente.

---

## Qué debe hacer el script

El flujo esperado es:

```text
Modelo UFO
   +
Lista de partículas odd
   +
Ruta de MadGraph
   |
   v
prepare_mg5_standalone.py
   |
   v
MadGraph5_aMC
   |
   v
output standalone_cpp
   |
   +-- src/
   +-- lib/
   +-- SubProcesses/
   |
   v
UI / Kerrigan / sigmaV / densidad reliquia
```

Por lo tanto, este script se encarga de preparar el entorno standalone de MadGraph.

No reemplaza a Kerrigan, al cálculo de sigmaV ni al cálculo de densidad reliquia.

---

## Por qué se utiliza Python

Python es preferible a Bash para esta etapa porque el programa necesita hacer bastante más que simplemente ejecutar MadGraph.

El script:

- valida rutas,
- valida la instalación de MadGraph,
- valida la estructura del UFO,
- lee `particles.py`,
- acepta nombres UFO o códigos PDG,
- resuelve relaciones partícula/antipartícula,
- construye el sector odd,
- construye el sector even complementario,
- genera los comandos de MadGraph,
- ejecuta MadGraph,
- valida el standalone generado,
- guarda logs y metadata para reproducibilidad,
- y evita sobreescrituras accidentales salvo que el usuario lo solicite explícitamente.

Bash seguiría siendo adecuado para wrappers más simples, pero Python es más apropiado para este nivel de validación y orquestación.

---

## Requisitos

La versión actual del script está configurada para requerir:

- Python 3
- MadGraph5_aMC@NLO **3.6.7 por defecto**
- un directorio UFO válido
- una lista de partículas Z2-impares

### Nota importante sobre la versión de MadGraph

Actualmente el script exige **exactamente la versión 3.6.7 por defecto**.

Esto significa:

```text
3.6.7    -> aceptada
3.6.8    -> rechazada por defecto
3.7.0    -> rechazada por defecto
3.5.6    -> rechazada por defecto
```

Este comportamiento es intencional porque el entorno actual del proyecto fue desarrollado alrededor de MadGraph 3.6.7.

Si el usuario desea desactivar la comprobación exacta de versión, el script permite:

```bash
--require-version any
```

Ejemplo:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /ruta/a/MG5_aMC \
    --ufo /ruta/al/modelo_UFO \
    --odd-file odd_particles.txt \
    --output /ruta/al/output \
    --require-version any
```

Esto desactiva la restricción de versión, pero **no garantiza** que cualquier versión más nueva de MadGraph sea compatible.

Si en el futuro se comprueba que las versiones posteriores a 3.6.7 funcionan correctamente, la política podría cambiarse de:

```text
version == 3.6.7
```

a:

```text
version >= 3.6.7
```

Por el momento, exigir exactamente 3.6.7 es la opción más segura.

---

## Estructura esperada del UFO

La ruta suministrada con `--ufo` debe apuntar a un directorio UFO válido con archivos como:

```text
model_UFO/
├── __init__.py
├── particles.py
├── parameters.py
├── vertices.py
├── couplings.py
├── lorentz.py
├── object_library.py
└── ...
```

El script valida la presencia de los archivos principales antes de ejecutar MadGraph.

---

## Input de partículas odd

El usuario puede proporcionar el sector odd de dos maneras.

### Opción 1: directamente desde la terminal

Usando nombres UFO:

```bash
--odd n1 n2 n3 etR etI etp
```

o usando códigos PDG:

```bash
--odd 1012 1014 1016 1001 1002 1003
```

En general se recomienda utilizar PDGs cuando sea posible, porque los nombres de las partículas pueden variar entre modelos UFO.

### Opción 2: mediante un archivo de texto

Ejemplo:

```text
# odd_particles.txt

1012
1014
1016
1001
1002
1003
```

También se aceptan valores separados por espacios o comas.

Ejemplo:

```text
1012 1014 1016 1001 1002 1003
```

o:

```text
1012, 1014, 1016, 1001, 1002, 1003
```

---

## Manejo de partículas y antipartículas

El script lee las definiciones de partículas directamente desde `particles.py`.

Si una partícula odd no es auto-conjugada, su antipartícula se añade automáticamente por defecto.

Por ejemplo, si:

```text
etp
```

tiene como antipartícula:

```text
etm
```

proporcionar solamente:

```text
etp
```

puede resultar en que ambas sean incluidas en la definición final del sector odd.

Este comportamiento se puede desactivar con:

```bash
--no-auto-antiparticles
```

---

## Estrategia de generación de MadGraph por defecto

Por defecto, el script crea dos definiciones multipartícula de MadGraph:

```text
dm_odd
dm_even
```

donde:

```text
dm_odd  = partículas odd seleccionadas por el usuario
dm_even = partículas físicas del UFO que no están en dm_odd
```

Los comandos generados conceptualmente son:

```text
import model /ruta/absoluta/al/modelo_UFO

define dm_odd = ...
define dm_even = ...

generate dm_odd dm_odd > dm_even dm_even

output standalone_cpp /ruta/absoluta/al/output
```

La idea importante es que el script de Python no intenta decidir qué diagramas de Feynman son físicamente posibles.

MadGraph recibe el modelo y determina qué amplitudes y procesos existen realmente.

---

## Modo de generación explícito

También existe:

```bash
--generation-mode explicit
```

Este modo genera comandos del tipo:

```text
generate n1 n1 > dm_even dm_even
add process n1 n2 > dm_even dm_even
add process n1 n3 > dm_even dm_even
...
```

Este modo es útil cuando se quiere inspeccionar explícitamente cada combinación del estado inicial.

El modo `multiparticle`, utilizado por defecto, es más compacto y más independiente del modelo.

---

## Primera prueba recomendada: dry run

Antes de ejecutar MadGraph, se recomienda validar los inputs mediante:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /ruta/a/MG5_aMC_v3_6_7 \
    --ufo /ruta/a/scotogenic_UFO \
    --odd-file odd_particles.txt \
    --output /ruta/a/scotogenic_standalone \
    --dry-run
```

Un `dry-run`:

- valida la ruta de MadGraph,
- valida su versión,
- valida el UFO,
- lee las partículas del UFO,
- resuelve la lista odd,
- construye el command card de MadGraph,
- muestra los comandos que se ejecutarían,
- y **no ejecuta MadGraph**.

Antes de continuar, el usuario debería revisar que `dm_odd` y `dm_even` tengan sentido.

---

## Ejemplo de ejecución real

Una vez validado el `dry-run`:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /ruta/a/MG5_aMC_v3_6_7 \
    --ufo /ruta/a/scotogenic_UFO \
    --odd-file odd_particles.txt \
    --output /ruta/a/scotogenic_standalone
```

o directamente con PDGs:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /ruta/a/MG5_aMC_v3_6_7 \
    --ufo /ruta/a/scotogenic_UFO \
    --odd 1012 1014 1016 1001 1002 1003 \
    --output /ruta/a/scotogenic_standalone
```

---

## Output esperado

Después de una ejecución exitosa, debería existir una estructura similar a:

```text
scotogenic_standalone/
├── SubProcesses/
│   ├── P1_...
│   ├── P2_...
│   └── ...
├── src/
├── lib/
├── generation_commands.mg5
├── generation_manifest.json
├── odd_particles_resolved.txt
└── mg5_generation.log
```

El script verifica que:

```text
SubProcesses/
src/
lib/
```

existan y que al menos un directorio `P*` haya sido generado.

---

## Metadata generada

### `generation_commands.mg5`

Contiene exactamente el command card utilizado para MadGraph.

Es útil para:

- reproducibilidad,
- depuración,
- inspección manual,
- comparación entre corridas.

### `generation_manifest.json`

Guarda información como:

- ruta de MadGraph,
- versión de MadGraph,
- ruta del UFO,
- partículas odd solicitadas,
- nombres de partículas resueltos,
- antipartículas añadidas,
- modo de generación,
- carpeta de salida,
- número de subprocesses.

### `odd_particles_resolved.txt`

Contiene los nombres finales del sector odd utilizados por MadGraph.

### `mg5_generation.log`

Contiene el log completo de ejecución de MadGraph.

---

## Protección contra sobreescritura

Por defecto, el programa se niega a reemplazar una carpeta de output existente.

Para reemplazarla explícitamente:

```bash
--force
```

Ejemplo:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /ruta/a/MG5_aMC_v3_6_7 \
    --ufo /ruta/al/modelo_UFO \
    --odd-file odd_particles.txt \
    --output /ruta/al/standalone \
    --force
```

Utilice `--force` con cuidado.

---

## Ubicación recomendada dentro del proyecto

Una estructura limpia podría ser:

```text
dark-matter-cosmology/
├── input/
│   ├── model_UFO/
│   └── odd_particles.txt
├── output/
├── scripts/
│   └── prepare_mg5_standalone.py
├── UI/
├── CMakeLists.txt
└── README.md
```

Luego, el standalone generado puede entregarse al flujo UI/Kerrigan.

---

## Flujo completo esperado del proyecto

El flujo de largo plazo es:

```text
UFO + lista de partículas odd
        |
        v
prepare_mg5_standalone.py
        |
        v
MadGraph standalone_cpp
        |
        +-- src/
        +-- lib/
        +-- SubProcesses/
        |
        v
select_effective_subprocesses_v3_ui.py
        |
        v
Kerrigan
        |
        +-- sigmaV
        |
        +-- densidad reliquia
```

Esta separación es intencional:

- `prepare_mg5_standalone.py` prepara MadGraph,
- la UI determina el conjunto relevante de subprocesses,
- Kerrigan orquesta el cálculo físico,
- los códigos posteriores calculan sigmaV y observables de densidad reliquia.

---

## Checklist recomendado para el usuario

Antes de considerar una ejecución exitosa, verificar:

- [ ] La ruta de MadGraph es correcta.
- [ ] La versión de MadGraph es aceptada.
- [ ] El directorio UFO es válido.
- [ ] Las partículas odd fueron identificadas correctamente.
- [ ] Las antipartículas fueron manejadas como se esperaba.
- [ ] Los comandos mostrados en `--dry-run` tienen sentido.
- [ ] Existe `SubProcesses/` después de la ejecución real.
- [ ] Existe `src/`.
- [ ] Existe `lib/`.
- [ ] Existe al menos un directorio `P*`.
- [ ] Existe `generation_manifest.json`.
- [ ] `mg5_generation.log` no contiene errores fatales de MadGraph.
- [ ] El standalone generado puede utilizarse en el flujo UI/Kerrigan.

---

## Autor

**Juan Diego Inga**

Proyecto Dark Matter Cosmology
