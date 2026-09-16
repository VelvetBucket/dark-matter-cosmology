# `run_madgraph.py` — Guía de Preparación del Standalone de MadGraph

**Autor:** Juan Diego Inga  
**Proyecto:** Dark Matter Cosmology  
**Nombre recomendado del script:** `scripts/run_madgraph.py`

---

## 1. Objetivo

`run_madgraph.py` prepara el output standalone C++ de MadGraph que necesita el resto del pipeline de materia oscura.

Recibe, directamente o a través del workspace generado por CMake:

1. un modelo UFO,
2. una lista de partículas Z2-impares (`odd particles`),
3. una instalación de MadGraph5_aMC,

y genera un standalone que contiene:

```text
SubProcesses/
src/
lib/        # cuando MadGraph lo genera
```

Ese directorio generado es el **MG5 output root** que posteriormente consumen la UI de selección de subprocesses y Kerrigan.

El script **no modifica**:

- el UFO original,
- la instalación de MadGraph,
- el árbol fuente original de MadGraph.

---

## 2. Lugar del script dentro del pipeline

El flujo recomendado es:

```text
1. Configurar el proyecto con CMake
                |
                v
2. CMake crea/configura el workspace del build
                |
                v
3. El usuario coloca UFO + odd list en build/input/
                |
                v
4. scripts/run_madgraph.py
                |
                v
5. MadGraph genera standalone_cpp
                |
                v
6. build/generated/<MODELO>_standalone/
   ├── SubProcesses/
   ├── src/
   └── lib/   [opcional]
                |
                v
7. select_effective_subprocesses_v3_ui.py
                |
                v
8. Kerrigan.sh
                |
                +--> sigmaV
                |
                +--> pipeline de densidad reliquia
```

### Importante

`run_madgraph.py` debe ejecutarse **después de configurar CMake**, porque el modo pipeline lee el directorio de build y puede obtener la ruta de MadGraph desde `CMakeCache.txt`.

No necesita que la UI o Kerrigan se hayan ejecutado previamente.

---

## 3. Archivo oficial que debe conservarse

El proyecto debería conservar únicamente:

```text
scripts/run_madgraph.py
```

El archivo de desarrollo:

```text
prepare_mg5_standalone_updated.py
```

contiene la misma implementación y no es necesario si `run_madgraph.py` ya está en el repositorio.

La versión antigua:

```text
prepare_mg5_standalone.py
```

debería eliminarse o archivarse para evitar tener dos versiones distintas de la misma etapa.

Si algún `CMakeLists.txt`, script Bash, README, workflow de CI o documentación todavía llama a:

```text
prepare_mg5_standalone.py
```

se debe cambiar esa referencia a:

```text
run_madgraph.py
```

---

## 4. Estructura recomendada del workspace

Después de configurar CMake, una estructura normal puede ser:

```text
build/
├── CMakeCache.txt
├── input/
│   ├── MyModel_UFO/
│   │   ├── __init__.py
│   │   ├── particles.py
│   │   ├── parameters.py
│   │   ├── vertices.py
│   │   ├── couplings.py
│   │   ├── lorentz.py
│   │   ├── object_library.py
│   │   └── ...
│   │
│   └── odd_particles.txt
│
├── generated/
└── ...
```

La invocación más simple sería:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

---

## 5. Qué descubre automáticamente el modo pipeline

Al ejecutarse con:

```bash
--build-dir build
```

el script puede resolver automáticamente lo siguiente.

### MadGraph

Lee `CMakeCache.txt` buscando variables comunes:

```text
MADGRAPH_DIR
MADGRAPH_ROOT
MG5_DIR
MG5_ROOT
MG5_BASE_DIR
FOLDER
```

También admite variables de entorno equivalentes.

La ruta elegida debe contener realmente:

```text
bin/mg5_aMC
```

o:

```text
bin/mg5
```

El script no confía únicamente en que una ruta aparezca en CMake.

---

### Modelo UFO

Si no se proporciona `--ufo`, se busca en:

```text
build/input/
```

exactamente un modelo UFO válido.

Se reconoce un UFO por la presencia de:

```text
particles.py
parameters.py
vertices.py
couplings.py
lorentz.py
object_library.py
__init__.py
```

Si no existe ningún UFO, el programa se detiene.

Si existen dos o más, también se detiene en lugar de escoger uno arbitrariamente.

En ese caso:

```bash
--ufo /ruta/al/ModeloEspecifico_UFO
```

---

### Lista de partículas odd

Si no se proporciona `--odd` ni `--odd-file`, se buscan:

```text
odd_particles.txt
odd_particles.dat
odd_particles
```

en el directorio de input.

El nombre recomendado es:

```text
odd_particles.txt
```

---

### Output

Si no se proporciona `--output`, se genera:

```text
build/generated/<nombre-del-UFO>_standalone/
```

Ejemplo:

```text
build/generated/scotogenic_UFO_standalone/
```

---

## 6. Política de versión de MadGraph

El rango soportado por defecto actualmente es:

```text
3.6.7 <= MadGraph <= 3.7.0
```

Por lo tanto:

```text
3.6.7  -> aceptada
3.6.8  -> aceptada
3.7.0  -> aceptada
3.7.1  -> rechazada por defecto
3.5.6  -> rechazada por defecto
```

Este rango es conservador y debería representar las versiones validadas por el proyecto.

### Modificar el rango

Se pueden utilizar:

```bash
--min-version 3.6.7
--max-version 3.7.0
```

### Exigir una versión exacta

```bash
--require-version 3.6.7
```

### Desactivar el chequeo

Solo para desarrollo/pruebas:

```bash
--require-version any
```

Desactivar el chequeo no significa que cualquier versión de MadGraph esté oficialmente soportada.

---

## 7. Input de partículas odd

El sector odd se puede proporcionar con nombres UFO o con códigos PDG.

### Recomendado: PDGs

Ejemplo de `build/input/odd_particles.txt`:

```text
# Sector Z2-odd
1012
1014
1016
1001
1002
1003
```

También puede escribirse:

```text
1012 1014 1016 1001 1002 1003
```

o:

```text
1012, 1014, 1016, 1001, 1002, 1003
```

Los comentarios que comienzan con `#` se ignoran.

### Desde terminal

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --odd 1012 1014 1016 1001 1002 1003
```

También se admiten nombres UFO:

```bash
--odd n1 n2 n3 etR etI etp
```

En general se prefieren los PDG porque los nombres pueden cambiar entre modelos UFO.

---

## 8. Manejo de partícula / antipartícula

El script lee `particles.py` sin ejecutar el UFO.

Para cada estado odd resuelve:

- PDG,
- nombre de partícula,
- nombre de antipartícula,
- si es auto-conjugada.

Por defecto, si una partícula odd no es auto-conjugada, se añade también su antipartícula.

Ejemplo:

```text
input: etp
odd resuelto: etp etm
```

Se puede desactivar conscientemente con:

```bash
--no-auto-antiparticles
```

---

## 9. Construcción del sector even

Una vez resuelto el sector odd, el resto de partículas físicas propagantes del UFO se utiliza para construir:

```text
dm_even
```

Se excluyen Goldstones, ghosts y partículas declaradas como no propagantes cuando el UFO proporciona esas propiedades.

Las definiciones conceptuales enviadas a MadGraph son:

```text
define dm_odd = ...
define dm_even = ...
```

---

## 10. Estrategia de generación por defecto

El default es:

```bash
--generation-mode multiparticle
```

y genera conceptualmente:

```text
import model /ruta/absoluta/model_UFO

define dm_odd = ...
define dm_even = ...

generate dm_odd dm_odd > dm_even dm_even

output standalone_cpp /ruta/absoluta/output
```

MadGraph decide qué amplitudes y procesos realmente existen en el modelo UFO.

Python no intenta sustituir la generación de diagramas de MadGraph.

---

## 11. Modo de generación explícito

Para debugging o inspección:

```bash
--generation-mode explicit
```

Se construyen todas las parejas iniciales no ordenadas del sector odd:

```text
generate n1 n1 > dm_even dm_even
add process n1 n2 > dm_even dm_even
add process n1 n3 > dm_even dm_even
...
```

Para uso normal se recomienda mantener el modo `multiparticle`.

---

## 12. Primera prueba recomendada: dry-run

Después de configurar CMake y colocar los inputs:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Se espera algo similar a:

```text
Invocation mode    : pipeline
CMake build        : /.../build
Pipeline input     : /.../build/input
MG5 root           : /.../MG5_aMC...
MG5 executable     : /.../bin/mg5_aMC
MG5 version        : 3.6.7 ... 3.7.0
UFO model          : /.../build/input/MyModel_UFO
Odd-particle file  : /.../build/input/odd_particles.txt
Standalone output  : /.../build/generated/MyModel_UFO_standalone
```

Además debe aparecer:

```text
Resolved odd-particle input:
```

y el command card completo de MadGraph.

### Garantía del dry-run

`--dry-run` no ejecuta MadGraph ni crea el standalone final.

Puede dejar el archivo temporal `.mg5` junto a la ruta planificada para que el usuario pueda inspeccionar los comandos.

---

## 13. Ejecución real

Cuando el dry-run sea correcto:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

Salida esperada:

```text
SUCCESS
Standalone output  : /.../build/generated/MyModel_UFO_standalone
Subprocesses       : N
src/               : yes
lib/               : yes
```

o:

```text
lib/               : no (allowed)
```

---

## 14. Output esperado

```text
build/generated/MyModel_UFO_standalone/
├── SubProcesses/
│   ├── P1_...
│   ├── P2_...
│   └── ...
├── src/
├── lib/                         # opcional
├── generation_commands.mg5
├── generation_manifest.json
├── odd_particles_resolved.txt
└── mg5_generation.log
```

### Obligatorios para el contrato actual UI/Kerrigan

```text
SubProcesses/
src/
```

### Opcional

```text
lib/
```

Si `lib/` no existe, el script muestra un warning en lugar de fallar.

Esto es intencional porque el Kerrigan actual puede mantener las librerías existentes del build si el standalone generado no aporta `lib/`.

---

## 15. Archivos pointer del pipeline

En modo pipeline también se crean:

```text
build/generated/current_mg5_output.txt
build/generated/current_mg5_output.json
```

`current_mg5_output.txt` contiene la ruta absoluta al último standalone generado correctamente.

Ejemplo:

```text
/home/user/project/build/generated/scotogenic_UFO_standalone
```

El JSON contiene:

```text
mg5_output
subprocesses
generation_manifest
```

Estos archivos son metadata de conveniencia.

La UI y Kerrigan actuales **no dependen** de ellos, por lo que su incorporación no rompe el contrato previo.

---

## 16. Metadata de reproducibilidad

### `generation_commands.mg5`

Command card exacto usado por MadGraph.

### `generation_manifest.json`

Contiene, entre otros:

- modo de invocación,
- build de CMake,
- input directory,
- ruta de MadGraph,
- ejecutable de MadGraph,
- versión de MadGraph,
- ruta del UFO,
- catálogo de partículas,
- odd input original,
- odd states resueltos,
- antipartículas añadidas,
- even states,
- parejas iniciales odd,
- lista de subprocesses generados,
- presencia o ausencia de `lib/`.

### `odd_particles_resolved.txt`

Nombres finales del sector odd utilizados por MadGraph.

### `mg5_generation.log`

Log completo de ejecución.

---

## 17. Pasar el resultado a la UI

Después del éxito, el programa imprime:

```text
Next-step paths:
  --mg5-output /.../MyModel_UFO_standalone
  --subprocesses /.../MyModel_UFO_standalone/SubProcesses
```

Ejemplo:

```bash
python3 UI/select_effective_subprocesses_v3_ui.py \
    /ruta/al/param_card.dat \
    --build-dir build \
    --mg5-output build/generated/MyModel_UFO_standalone \
    --subprocesses build/generated/MyModel_UFO_standalone/SubProcesses \
    --mode combined \
    --candidate 1012 \
    --task sigmav
```

La UI selecciona los procesos efectivos y posteriormente llama al Kerrigan generado por CMake.

---

## 18. Modo explícito compatible con el workflow anterior

El modo pipeline es el recomendado, pero se pueden seguir proporcionando todas las rutas:

```bash
python3 scripts/run_madgraph.py \
    --mg5-root /ruta/a/MG5_aMC \
    --ufo /ruta/a/MyModel_UFO \
    --odd-file /ruta/a/odd_particles.txt \
    --output /ruta/a/MyModel_standalone
```

o:

```bash
python3 scripts/run_madgraph.py \
    --mg5-root /ruta/a/MG5_aMC \
    --ufo /ruta/a/MyModel_UFO \
    --odd 1012 1014 1016 \
    --output /ruta/a/MyModel_standalone
```

Esto mantiene compatibilidad con el uso anterior.

---

## 19. Protección contra sobreescritura

Por defecto, si el output ya existe el script se detiene:

```text
ERROR: Output already exists...
```

Para regenerarlo conscientemente:

```bash
--force
```

Ejemplo:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --force
```

`--force` elimina recursivamente únicamente el output seleccionado antes de regenerarlo.

Debe utilizarse con cuidado.

---

# 20. Pruebas recomendadas

## Test 1 — Sintaxis de Python

```bash
python3 -m py_compile scripts/run_madgraph.py
```

Esperado:

```text
sin output
exit code 0
```

---

## Test 2 — Help

```bash
python3 scripts/run_madgraph.py --help
```

Debe mostrar:

```text
--build-dir
--input-dir
--mg5-root
--ufo
--odd
--odd-file
--output
--generation-mode
--min-version
--max-version
--require-version
--force
--dry-run
```

---

## Test 3 — Descubrimiento automático del pipeline

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Verificar que sean correctos:

```text
MG5 root
UFO model
Odd-particle file
Standalone output
```

---

## Test 4 — Override de UFO

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --ufo /ruta/a/MyModel_UFO \
    --dry-run
```

El UFO explícito debe tener prioridad.

---

## Test 5 — Odd PDGs por CLI

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --odd 1012 1014 1016 \
    --dry-run
```

No debe requerir `odd_particles.txt`.

---

## Test 6 — Dos UFOs en input

Colocar dos UFO válidos en `build/input/` y ejecutar:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Esperado:

```text
ERROR: More than one UFO model was found...
```

Después comprobar que funciona:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --ufo build/input/ChosenModel_UFO \
    --dry-run
```

---

## Test 7 — Versión no soportada

Una instalación fuera del rango debe fallar antes de generar procesos.

Política por defecto:

```text
3.6.7 <= version <= 3.7.0
```

---

## Test 8 — Versión exacta

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --require-version 3.6.7 \
    --dry-run
```

Solo 3.6.7 debe pasar.

---

## Test 9 — Bypass de versión

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --require-version any \
    --dry-run
```

Solo utilizar para desarrollo.

---

## Test 10 — Generación real

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

Verificar:

```bash
test -d build/generated/*_standalone/SubProcesses
test -d build/generated/*_standalone/src
```

Comprobar que haya procesos:

```bash
find build/generated/*_standalone/SubProcesses \
    -mindepth 1 -maxdepth 1 -type d \
    -name 'P*' | head
```

---

## Test 11 — Metadata generada

```bash
test -s build/generated/*_standalone/generation_manifest.json
test -s build/generated/*_standalone/generation_commands.mg5
test -s build/generated/*_standalone/mg5_generation.log
test -s build/generated/*_standalone/odd_particles_resolved.txt
```

---

## Test 12 — Pointer actual

```bash
cat build/generated/current_mg5_output.txt
```

Debe apuntar al standalone recién generado.

---

## Test 13 — Compatibilidad con la UI

```bash
python3 UI/select_effective_subprocesses_v3_ui.py \
    /ruta/al/param_card.dat \
    --build-dir build \
    --mg5-output "$(cat build/generated/current_mg5_output.txt)" \
    --subprocesses "$(cat build/generated/current_mg5_output.txt)/SubProcesses" \
    --mode pdg \
    --pdgs 1012 \
    --task sigmav \
    --dry-run
```

La UI debe poder leer correctamente los `SubProcesses/` generados.

---

# 21. Checklist mínimo de aceptación

Un nuevo modelo está listo para la siguiente etapa cuando:

- [ ] `run_madgraph.py` compila.
- [ ] MadGraph se resuelve correctamente.
- [ ] La versión de MadGraph cumple la política del proyecto.
- [ ] Se selecciona exactamente el UFO deseado.
- [ ] Las partículas odd se resuelven correctamente.
- [ ] Las antipartículas necesarias se añaden correctamente.
- [ ] El command card del dry-run es físicamente razonable.
- [ ] MadGraph finaliza correctamente.
- [ ] Existe `SubProcesses/`.
- [ ] Existe `src/`.
- [ ] Existe al menos un directorio `P*`.
- [ ] Existe `generation_manifest.json`.
- [ ] Existe `generation_commands.mg5`.
- [ ] Existe `mg5_generation.log`.
- [ ] `current_mg5_output.txt` apunta al standalone correcto.
- [ ] La UI puede analizar los `SubProcesses/`.
- [ ] La instalación original de MadGraph no fue modificada.
- [ ] El UFO original no fue modificado.

---

# 22. Troubleshooting

## `MadGraph path could not be resolved`

Causas posibles:

- CMake no guardó la ruta con un nombre reconocido,
- falta la variable de entorno,
- la ruta ya no contiene `bin/mg5_aMC`.

Solución:

```bash
--mg5-root /ruta/absoluta/a/MG5_aMC
```

---

## `Pipeline input directory does not exist`

Crear:

```bash
mkdir -p build/input
```

y colocar ahí UFO + odd list.

---

## `No UFO model was found`

Revisar que el UFO contenga los archivos estándar requeridos.

O indicar:

```bash
--ufo /ruta/absoluta/model_UFO
```

---

## `More than one UFO model was found`

El programa no escoge arbitrariamente.

Utilizar:

```bash
--ufo build/input/ChosenModel_UFO
```

---

## `No odd particles were provided`

Proporcionar:

```text
build/input/odd_particles.txt
```

o:

```bash
--odd-file /ruta/archivo
```

o:

```bash
--odd 1012 1014 ...
```

---

## `Odd particle ... was not found in the UFO`

El nombre o PDG no coincide con una partícula de `particles.py`.

Revisar las definiciones del UFO.

---

## `Unsupported MadGraph version`

Usar una versión soportada por el proyecto.

No desactivar la validación en producción sin haber probado previamente esa versión.

---

## `Output already exists`

Escoger otro output o regenerar conscientemente:

```bash
--force
```

---

## MadGraph devuelve exit code no cero

Revisar el log temporal:

```text
<parent>/.<standalone-name>.mg5.log
```

Cuando la generación termina correctamente, el log se copia a:

```text
<standalone>/mg5_generation.log
```

---

# 23. Resumen de seguridad

El comportamiento deseado es:

```text
Instalación de MadGraph  -> solo lectura/ejecución
UFO fuente               -> solo lectura
odd-particle file        -> solo lectura
build/input              -> solo lectura
build/generated          -> datos generados por runtime
```

Solo el output generado seleccionado puede eliminarse recursivamente cuando el usuario proporciona explícitamente:

```bash
--force
```

---

## Autor

**Juan Diego Inga**

Proyecto Dark Matter Cosmology
