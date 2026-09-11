# ==============================================================================
# Dark Matter Cosmology — CMake configuration
#
# Build layout (inside ./build/):
#   process_files/   CMake-tracked process files (seeded from example_process/)
#     ├── CPPProcess.cc/h
#     ├── lib/       process libraries (linked into core_lib)
#     └── src/       process sources/headers (compiled into core_lib)
#   event/           Runtime symlink → user's chosen event folder
#   input/example/   Copied from source example_input/
#   datatables/      Copied from source datatables/
#   UI/              Copied from source UI/
#   scripts/         Copied from source scripts/
#   bin/             sigmav, evolution, interp
#
# Workflow:
#   1. cmake .. -DMADGRAPH_DIR=/path/to/MG5
#   2. make                      # builds with example_process
#   3. ./run_ui  (or Kerrigan.sh) # overwrites process_files/ then `make sigmav`
# ==============================================================================

cmake_minimum_required(VERSION 3.10)
project(dark_matter_cosmology VERSION 1.0.0 LANGUAGES CXX)

# Ensure every target's runtime output goes into build/bin/
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")


# ==============================================================================
# Required: path to the MadGraph5 base directory
# ==============================================================================
set(MADGRAPH_DIR "" CACHE PATH "Absolute path to the base MadGraph5 directory")
if(NOT MADGRAPH_DIR)
    message(FATAL_ERROR
        "MADGRAPH_DIR is required.\n"
        "Usage: cmake .. -DMADGRAPH_DIR=/absolute/path/to/MadGraph5_base"
    )
endif()

get_filename_component(MADGRAPH_DIR "${MADGRAPH_DIR}" ABSOLUTE)
if(NOT EXISTS "${MADGRAPH_DIR}")
    message(FATAL_ERROR "MADGRAPH_DIR does not exist: ${MADGRAPH_DIR}")
endif()

message(STATUS "MadGraph5 base directory: ${MADGRAPH_DIR}")


# ==============================================================================
# Enforce MadGraph5 version range: 3.6.7 ≤ version ≤ 3.7.0
# ==============================================================================
set(MG5_MIN_VERSION "3.6.7")
set(MG5_MAX_VERSION "3.7.0")
message(STATUS "Required MadGraph5 version range: ${MG5_MIN_VERSION} … ${MG5_MAX_VERSION}")

if(NOT EXISTS "${MADGRAPH_DIR}/VERSION")
    message(FATAL_ERROR "VERSION file not found in ${MADGRAPH_DIR}")
endif()

file(STRINGS "${MADGRAPH_DIR}/VERSION" MG5_VERSION_LINES)

set(MG5_VERSION "")
foreach(LINE ${MG5_VERSION_LINES})
    if(LINE MATCHES "^[ \t]*version[ \t]*=")
        string(REGEX REPLACE "^[ \t]*version[ \t]*=[ \t]*" "" MG5_VERSION "${LINE}")
    endif()
endforeach()

if(NOT MG5_VERSION)
    message(FATAL_ERROR "Could not parse version from ${MADGRAPH_DIR}/VERSION")
endif()

if(MG5_VERSION VERSION_LESS MG5_MIN_VERSION OR
   MG5_VERSION VERSION_GREATER MG5_MAX_VERSION)
    message(FATAL_ERROR
        "MadGraph5 version ${MG5_VERSION} is outside the accepted range "
        "[${MG5_MIN_VERSION}, ${MG5_MAX_VERSION}]."
    )
endif()

message(STATUS "MadGraph5 version ${MG5_VERSION} — OK")


# ==============================================================================
# C++ settings
# ==============================================================================
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

add_definitions(-D_USE_MATH_DEFINES)

if(NOT MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast -g -Wall -Wextra")
    # MadGraph5-generated code is noisy; silence the common warnings.
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-parameter")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-but-set-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-misleading-indentation")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-comment")
endif()


# ==============================================================================
# Build-tree directories
# ==============================================================================
set(SCRIPTS_DIR     "${CMAKE_CURRENT_BINARY_DIR}/scripts")
set(INPUT_DIR       "${CMAKE_CURRENT_BINARY_DIR}/input")
set(EXAMPLE_DIR     "${INPUT_DIR}/example")
set(PROCESS_DIR     "${CMAKE_CURRENT_BINARY_DIR}/process_files")   # CMake-tracked
set(PROCESS_LIB_DIR "${PROCESS_DIR}/lib")
set(PROCESS_SRC_DIR "${PROCESS_DIR}/src")
set(EVENT_DIR       "${CMAKE_CURRENT_BINARY_DIR}/event")           # runtime symlink
set(DATATABLES_DIR  "${CMAKE_CURRENT_BINARY_DIR}/datatables")
set(BUILD_UI_DIR    "${CMAKE_CURRENT_BINARY_DIR}/UI")

file(MAKE_DIRECTORY "${SCRIPTS_DIR}")
file(MAKE_DIRECTORY "${INPUT_DIR}")
file(MAKE_DIRECTORY "${EXAMPLE_DIR}")
file(MAKE_DIRECTORY "${PROCESS_DIR}")
file(MAKE_DIRECTORY "${DATATABLES_DIR}")
file(MAKE_DIRECTORY "${BUILD_UI_DIR}")

add_definitions(-DDATATABLES_DIR="${DATATABLES_DIR}")


# ==============================================================================
# Copy source-tree assets into the build tree
# ==============================================================================
message(STATUS "Copying assets into the build tree...")

# --- UI (Python) ------------------------------------------------------------
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/UI")
    file(GLOB UI_FILES
        "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.json"
        "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.txt"
    )
    foreach(FILE ${UI_FILES})
        get_filename_component(FILENAME "${FILE}" NAME)
        configure_file("${FILE}" "${BUILD_UI_DIR}/${FILENAME}" COPYONLY)
    endforeach()
    message(STATUS "  UI                  -> ${BUILD_UI_DIR}")
else()
    message(WARNING "UI/ directory not found in source tree")
endif()

# --- example_input ----------------------------------------------------------
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/example_input")
    file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/example_input"
         DESTINATION "${INPUT_DIR}")
    file(RENAME "${INPUT_DIR}/example_input" "${EXAMPLE_DIR}")
    message(STATUS "  example_input       -> ${EXAMPLE_DIR}")
else()
    message(WARNING "example_input/ not found in source tree")
endif()

# --- datatables -------------------------------------------------------------
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/datatables")
    file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/datatables"
         DESTINATION "${CMAKE_CURRENT_BINARY_DIR}")
    message(STATUS "  datatables          -> ${DATATABLES_DIR}")
else()
    message(WARNING "datatables/ not found in source tree")
endif()

# --- scripts ----------------------------------------------------------------
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template")
    file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template"
         DESTINATION "${SCRIPTS_DIR}")
    message(STATUS "  modify_template     -> ${SCRIPTS_DIR}/modify_template")
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/utilities")
    file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/scripts/utilities"
         DESTINATION "${SCRIPTS_DIR}")
    message(STATUS "  utilities           -> ${SCRIPTS_DIR}/utilities")
endif()


# ==============================================================================
# Seed process_files/ with the contents of example_process/
# (CPPProcess.cc, CPPProcess.h, lib/, src/)
#
# These files are what CMake tracks for sigmav. Replacing them at runtime and
# running `make sigmav` recompiles core_lib and relinks sigmav — no CMake rerun.
# ==============================================================================
set(EXAMPLE_PROCESS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/example_process")

if(EXISTS "${EXAMPLE_PROCESS_DIR}")
    message(STATUS "Copying example_process/ into ${PROCESS_DIR}/ ...")

    # --- CPPProcess.cc / .h ---
    if(EXISTS "${EXAMPLE_PROCESS_DIR}/CPPProcess.cc")
        configure_file(
            "${EXAMPLE_PROCESS_DIR}/CPPProcess.cc"
            "${PROCESS_DIR}/CPPProcess.cc" COPYONLY)
    endif()
    if(EXISTS "${EXAMPLE_PROCESS_DIR}/CPPProcess.h")
        configure_file(
            "${EXAMPLE_PROCESS_DIR}/CPPProcess.h"
            "${PROCESS_DIR}/CPPProcess.h" COPYONLY)
    endif()

    # --- lib/ (static archives, .so, etc.) ---
    if(EXISTS "${EXAMPLE_PROCESS_DIR}/lib")
        file(COPY "${EXAMPLE_PROCESS_DIR}/lib/"
             DESTINATION "${PROCESS_LIB_DIR}")
        message(STATUS "  lib/  -> ${PROCESS_LIB_DIR}")
    endif()

    # --- src/ (source + headers used by the process) ---
    if(EXISTS "${EXAMPLE_PROCESS_DIR}/src")
        file(COPY "${EXAMPLE_PROCESS_DIR}/src/"
             DESTINATION "${PROCESS_SRC_DIR}")
        message(STATUS "  src/  -> ${PROCESS_SRC_DIR}")
    endif()

    message(STATUS "  CPPProcess.* -> ${PROCESS_DIR}")
else()
    message(WARNING "example_process/ not found in source tree — "
                    "process_files/ will be empty")
endif()


# ==============================================================================
# core_lib — your tools + the current process
#
# Sources:
#   process_files/CPPProcess.cc      ← tracked; replaced at runtime by Kerrigan
#   process_files/src/*.cc           ← optional extra sources from the process
#   src/core/...                     ← your own utilities
# ==============================================================================

# Auto-glob extra sources under process_files/src/
file(GLOB_RECURSE PROCESS_EXTRA_SOURCES
    "${PROCESS_SRC_DIR}/*.cc"
    "${PROCESS_SRC_DIR}/*.cpp"
)

set(CORE_SOURCES
    "${PROCESS_DIR}/CPPProcess.cc"
    ${PROCESS_EXTRA_SOURCES}
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/process/momenta.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/integration.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/bessel.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/data_handling.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/interpolation.cc"
)

set(CORE_HEADERS
    "${PROCESS_DIR}/CPPProcess.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/tools.h"
)

add_library(core_lib STATIC ${CORE_SOURCES} ${CORE_HEADERS})

target_include_directories(core_lib PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/core/process"
    "${PROCESS_DIR}"           # for "CPPProcess.h"
    "${PROCESS_SRC_DIR}"       # for any headers under process_files/src/
)

# Link the process's own library/ies if present
if(EXISTS "${PROCESS_LIB_DIR}")
    file(GLOB PROCESS_LIBS
        "${PROCESS_LIB_DIR}/*.a"
        "${PROCESS_LIB_DIR}/*.so"
        "${PROCESS_LIB_DIR}/*.dylib"
    )
    if(PROCESS_LIBS)
        target_link_libraries(core_lib PUBLIC ${PROCESS_LIBS})
        foreach(_lib ${PROCESS_LIBS})
            message(STATUS "  Linking process lib: ${_lib}")
        endforeach()
    else()
        message(STATUS "  process_files/lib/ exists but contains no archives")
    endif()
    target_link_directories(core_lib PUBLIC "${PROCESS_LIB_DIR}")
endif()


# ==============================================================================
# Executables
# ==============================================================================
add_executable(sigmav    "${CMAKE_CURRENT_SOURCE_DIR}/src/main/sigmav.cpp")
add_executable(evolution "${CMAKE_CURRENT_SOURCE_DIR}/src/main/evolution.cpp")
add_executable(interp    "${CMAKE_CURRENT_SOURCE_DIR}/src/main/interp.cpp")

target_link_libraries(sigmav    core_lib gsl gslcblas m)
target_link_libraries(evolution core_lib)
target_link_libraries(interp    core_lib)

set_target_properties(sigmav evolution interp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)


# ==============================================================================
# Run interp once after build, only if its output doesn't exist yet
# ==============================================================================
add_custom_command(TARGET interp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Checking ${DATATABLES_DIR}/interp_ath.dat ..."
    COMMAND /bin/bash -c "if [ ! -f '${DATATABLES_DIR}/interp_ath.dat' ]; then \
        echo 'Running interp (first time)...'; \
        '${CMAKE_BINARY_DIR}/bin/interp' > '${DATATABLES_DIR}/interp_ath.dat'; \
        echo 'Saved to ${DATATABLES_DIR}/interp_ath.dat'; \
    else \
        echo 'interp_ath.dat already exists — skipping'; \
    fi"
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
    COMMENT "interp post-build"
    VERBATIM
)


# ==============================================================================
# Force a rebuild of sigmav after replacing process_files/
# ==============================================================================
add_custom_target(relink_sigmav
    COMMAND ${CMAKE_COMMAND} -E touch "${PROCESS_DIR}/CPPProcess.cc"
    COMMAND ${CMAKE_COMMAND} -E touch "${PROCESS_DIR}/CPPProcess.h"
    COMMAND ${CMAKE_COMMAND} --build "${CMAKE_BINARY_DIR}" --target sigmav
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
    COMMENT "Relinking sigmav against current process_files/"
    USES_TERMINAL
)


# ==============================================================================
# Configure Kerrigan.sh
# ==============================================================================
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/scripts/Kerrigan.sh.in"
    "${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh"
    @ONLY
)

file(CHMOD "${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh"
    PERMISSIONS
        OWNER_READ OWNER_WRITE OWNER_EXECUTE
        GROUP_READ GROUP_EXECUTE
        WORLD_READ WORLD_EXECUTE
)


# ==============================================================================
# run_ui wrapper (runs UI.py from the build tree with the right env)
# ==============================================================================
set(UI_WRAPPER "${CMAKE_CURRENT_BINARY_DIR}/run_ui")

file(WRITE  "${UI_WRAPPER}" "#!/usr/bin/env bash\n")
file(APPEND "${UI_WRAPPER}" "# Auto-generated by CMake\n\n")
file(APPEND "${UI_WRAPPER}" "export DATATABLES_DIR=\"${DATATABLES_DIR}\"\n")
file(APPEND "${UI_WRAPPER}" "export PROCESS_DIR=\"${PROCESS_DIR}\"\n")
file(APPEND "${UI_WRAPPER}" "export EVENT_DIR=\"${EVENT_DIR}\"\n")
file(APPEND "${UI_WRAPPER}" "export BUILD_DIR=\"${CMAKE_CURRENT_BINARY_DIR}\"\n")
file(APPEND "${UI_WRAPPER}" "export MADGRAPH_DIR=\"${MADGRAPH_DIR}\"\n\n")
file(APPEND "${UI_WRAPPER}" "cd \"${CMAKE_CURRENT_BINARY_DIR}\"\n")
file(APPEND "${UI_WRAPPER}" "exec python3 \"${BUILD_UI_DIR}/UI.py\" \"\$@\"\n")

file(CHMOD "${UI_WRAPPER}"
    PERMISSIONS
        OWNER_READ OWNER_WRITE OWNER_EXECUTE
        GROUP_READ GROUP_EXECUTE
        WORLD_READ WORLD_EXECUTE
)


# ==============================================================================
# Convenience targets
# ==============================================================================
add_custom_target(ui
    COMMAND "${CMAKE_CURRENT_BINARY_DIR}/run_ui"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMENT "Running UI"
    USES_TERMINAL
)

add_custom_target(run
    COMMAND "${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh" DM_test
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMENT "Running Kerrigan.sh on DM_test"
    USES_TERMINAL
)

add_custom_target(list_mg5
    COMMAND /bin/bash -c "ls -d ${MADGRAPH_DIR}/*/ 2>/dev/null | xargs -n 1 basename"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMENT "Available MadGraph5 outputs"
    USES_TERMINAL
)


# ==============================================================================
# Install
# ==============================================================================
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/bin/"
        DESTINATION bin USE_SOURCE_PERMISSIONS)
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/scripts/"
        DESTINATION share/dark_matter/scripts USE_SOURCE_PERMISSIONS)
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/datatables/"
        DESTINATION share/dark_matter/datatables USE_SOURCE_PERMISSIONS)
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/UI/"
        DESTINATION share/dark_matter/UI USE_SOURCE_PERMISSIONS)
install(PROGRAMS "${CMAKE_CURRENT_BINARY_DIR}/run_ui"
        DESTINATION bin RENAME dark_matter_ui)


# ==============================================================================
# Summary
# ==============================================================================
message(STATUS "")
message(STATUS "========================================")
message(STATUS "  ${PROJECT_NAME} ${PROJECT_VERSION}")
message(STATUS "========================================")
message(STATUS "  MG5 base dir   : ${MADGRAPH_DIR}")
message(STATUS "  MG5 version    : ${MG5_VERSION}")
message(STATUS "  Accepted range : [${MG5_MIN_VERSION}, ${MG5_MAX_VERSION}]")
message(STATUS "  Build dir      : ${CMAKE_CURRENT_BINARY_DIR}")
message(STATUS "")
message(STATUS "  process_files/ : ${PROCESS_DIR}")
message(STATUS "    ├── CPPProcess.cc/h")
message(STATUS "    ├── lib/       (linked into core_lib)")
message(STATUS "    └── src/       (compiled into core_lib)")
message(STATUS "  datatables/    : ${DATATABLES_DIR}")
message(STATUS "  UI/            : ${BUILD_UI_DIR}")
message(STATUS "  scripts/       : ${SCRIPTS_DIR}")
message(STATUS "  example/       : ${EXAMPLE_DIR}")
message(STATUS "")
message(STATUS "  Executables    : bin/sigmav, bin/evolution, bin/interp")
message(STATUS "")
message(STATUS "  make ui            # run the UI")
message(STATUS "  make run           # run Kerrigan.sh DM_test")
message(STATUS "  make relink_sigmav # after replacing process_files/")
message(STATUS "========================================")
