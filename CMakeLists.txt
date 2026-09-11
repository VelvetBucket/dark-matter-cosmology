# ============================================
# CMake minimum version and project name
# ============================================
cmake_minimum_required(VERSION 3.10)
project(dark_matter_cosmology VERSION 1.0.0 LANGUAGES CXX)

# ============================================
# REQUIRED FOLDER VARIABLE (Base MadGraph5 directory)
# ============================================
set(FOLDER "" CACHE PATH "Absolute path to the base MadGraph5 directory (e.g., /path/to/MG5)")
if(NOT FOLDER)
    message(FATAL_ERROR 
        "FOLDER is required!\n"
        "Usage: cmake .. -DFOLDER=/absolute/path/to/MadGraph5_base_directory\n"
        "Example: cmake .. -DFOLDER=/home/user/MG5"
    )
endif()

get_filename_component(FOLDER "${FOLDER}" ABSOLUTE)
if(NOT EXISTS "${FOLDER}")
    message(FATAL_ERROR "FOLDER does not exist: ${FOLDER}")
endif()

message(STATUS "Using MadGraph5 base directory: ${FOLDER}")

# ============================================
# MadGraph5 Version Check (EXACT MATCH REQUIRED)
# ============================================
set(REQUIRED_MG5_VERSION "3.6.7")
message(STATUS "Required MadGraph5 version: ${REQUIRED_MG5_VERSION} (exact match required)")

# Read version from VERSION file
if(EXISTS "${FOLDER}/VERSION")
    file(STRINGS "${FOLDER}/VERSION" MG5_VERSION_LINES)
    
    set(MG5_VERSION "")
    set(MG5_VERSION_DATE "")
    
    foreach(LINE ${MG5_VERSION_LINES})
        if(LINE MATCHES "^[ \t]*version[ \t]*=")
            string(REGEX REPLACE "^[ \t]*version[ \t]*=[ \t]*" "" MG5_VERSION "${LINE}")
            message(STATUS "Found MadGraph5 version: ${MG5_VERSION}")
        endif()
        if(LINE MATCHES "^[ \t]*date[ \t]*=")
            string(REGEX REPLACE "^[ \t]*date[ \t]*=[ \t]*" "" MG5_VERSION_DATE "${LINE}")
            message(STATUS "MadGraph5 build date: ${MG5_VERSION_DATE}")
        endif()
    endforeach()
    
    if(NOT MG5_VERSION)
        message(FATAL_ERROR 
            "Could not find version in VERSION file!\n"
            "Please check that the VERSION file has a line: version = X.X.X"
        )
    endif()
    
    if(NOT MG5_VERSION VERSION_EQUAL REQUIRED_MG5_VERSION)
        message(FATAL_ERROR 
            "\n========================================\n"
            "ERROR: MadGraph5 version mismatch!\n"
            "========================================\n"
            "Found version:    ${MG5_VERSION}\n"
            "Required version: ${REQUIRED_MG5_VERSION} (exact match required)\n"
            "Found at:         ${FOLDER}\n"
            "\n"
            "This project requires exactly MadGraph5 ${REQUIRED_MG5_VERSION}.\n"
            "========================================\n"
        )
    else()
        message(STATUS "✅ MadGraph5 version ${MG5_VERSION} matches required version (${REQUIRED_MG5_VERSION})")
    endif()
else()
    message(FATAL_ERROR "VERSION file not found in ${FOLDER}")
endif()

# ============================================
# C++ Standard Settings
# ============================================
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
add_definitions(-D_USE_MATH_DEFINES)

# ============================================
# Compiler Flags
# ============================================
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast -g")
if(NOT MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-parameter")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-but-set-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-misleading-indentation")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-comment")
endif()

# ============================================
# Directories in the BUILD tree
# ============================================
set(SCRIPTS_DIR ${CMAKE_CURRENT_BINARY_DIR}/scripts)
set(INPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/input)
set(BUILD_UI_DIR ${CMAKE_CURRENT_BINARY_DIR}/UI)
set(EXAMPLE_DIR "${INPUT_DIR}/example")
set(DATATABLES_DIR "${CMAKE_CURRENT_BINARY_DIR}/datatables")

# Create directories
file(MAKE_DIRECTORY ${SCRIPTS_DIR})
file(MAKE_DIRECTORY ${INPUT_DIR})
file(MAKE_DIRECTORY ${BUILD_UI_DIR})
file(MAKE_DIRECTORY ${EXAMPLE_DIR})
file(MAKE_DIRECTORY ${DATATABLES_DIR})

# ============================================
# Define data directory paths for executables
# ============================================
add_definitions(-DDATATABLES_DIR="${DATATABLES_DIR}")

message(STATUS "Data directory definitions:")
message(STATUS "  - DATATABLES_DIR: ${DATATABLES_DIR}")
message(STATUS "  - EXAMPLE_DIR: ${EXAMPLE_DIR}")

# ============================================
# Copy UI files to build directory
# ============================================
message(STATUS "Copying UI files to build directory...")

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/UI)
    # Copy all Python files
    file(GLOB UI_PY_FILES "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.py")
    foreach(FILE ${UI_PY_FILES})
        get_filename_component(FILENAME ${FILE} NAME)
        configure_file(${FILE} ${BUILD_UI_DIR}/${FILENAME} COPYONLY)
    endforeach()
    message(STATUS "  - Copied UI Python files to ${BUILD_UI_DIR}")
    
    # Copy any other UI files (JSON, etc.)
    file(GLOB UI_OTHER_FILES "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.json" "${CMAKE_CURRENT_SOURCE_DIR}/UI/*.txt")
    foreach(FILE ${UI_OTHER_FILES})
        get_filename_component(FILENAME ${FILE} NAME)
        configure_file(${FILE} ${BUILD_UI_DIR}/${FILENAME} COPYONLY)
    endforeach()
    message(STATUS "  - Copied UI data files to ${BUILD_UI_DIR}")
else()
    message(WARNING "UI directory not found at ${CMAKE_CURRENT_SOURCE_DIR}/UI")
endif()

# ============================================
# Copy example files from source to build
# ============================================
message(STATUS "Copying example files to build directory...")

# Copy example files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/example_input)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/example_input
         DESTINATION ${INPUT_DIR})
    file(RENAME ${INPUT_DIR}/example_input
            ${EXAMPLE_DIR})
    message(STATUS "  - Copied example files to ${EXAMPLE_DIR}")
else()
    message(WARNING "No example files found in example_input/")
endif()

# ============================================
# Copy datatables to build directory
# ============================================
message(STATUS "Copying datatables to build directory...")

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/datatables)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/datatables
         DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    message(STATUS "  - Copied datatables to ${DATATABLES_DIR}")
else()
    message(WARNING "No datatables found in ${CMAKE_CURRENT_SOURCE_DIR}/datatables")
endif()

# ============================================
# Copy scripts to build directory
# ============================================
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template
         DESTINATION ${SCRIPTS_DIR})
    message(STATUS "Copied modify_template to ${SCRIPTS_DIR}/modify_template")
endif()

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/utilities)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/scripts/utilities
         DESTINATION ${SCRIPTS_DIR})
    message(STATUS "Copied utilities to ${SCRIPTS_DIR}/utilities")
endif()

# ============================================
# Model Library (from templates in build directory)
# ============================================
set(MODELLIB model_scotogenic_UFO)
set(MODEL_SOURCES
    ${MODEL_DIR}/HelAmps_scotogenic_UFO.cc
    ${MODEL_DIR}/Parameters_scotogenic_UFO.cc
    ${MODEL_DIR}/rambo.cc
    ${MODEL_DIR}/read_slha.cc
)

add_library(${MODELLIB} STATIC ${MODEL_SOURCES})
target_include_directories(${MODELLIB} PUBLIC ${MODEL_DIR})
target_compile_options(${MODELLIB} PRIVATE -w)

# ============================================
# Core Library (your tools + process from build directory)
# ============================================
set(CORE_SOURCES
    ${PROCESS_DIR}/CPPProcess.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/process/momenta.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/integration.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/bessel.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/data_handling.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools/interpolation.cc
)

add_library(core_lib STATIC ${CORE_SOURCES})
target_include_directories(core_lib PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/process
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools
    ${PROCESS_DIR}
)
target_link_libraries(core_lib ${MODELLIB})

# ============================================
# Set output directories for both libraries
# ============================================
set_target_properties(${MODELLIB} core_lib PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${LIB_DIR}
)

# ============================================
# Include directories (source + build)
# ============================================
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/process
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools
    ${PROCESS_DIR}
    ${MODEL_DIR}
    ${DATA_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
)

link_directories(${LIB_DIR})

# ============================================
# Executables
# ============================================
add_executable(sigmav ${CMAKE_CURRENT_SOURCE_DIR}/src/main/sigmav.cpp)
target_link_libraries(sigmav core_lib gsl gslcblas m)
add_dependencies(sigmav core_lib)

add_executable(evolution ${CMAKE_CURRENT_SOURCE_DIR}/src/main/evolution.cpp)
target_link_libraries(evolution core_lib)

add_executable(interp ${CMAKE_CURRENT_SOURCE_DIR}/src/main/interp.cpp)
target_link_libraries(interp core_lib)

# ============================================
# Run interp automatically after build (only if output doesn't exist)
# ============================================
add_custom_command(
    TARGET interp
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "========================================"
    COMMAND ${CMAKE_COMMAND} -E echo "Checking if ${DATATABLES_DIR}/interp_ath.dat exists..."
    COMMAND ${CMAKE_COMMAND} -E echo "========================================"
    COMMAND /bin/bash -c "if [ ! -f ${DATATABLES_DIR}/interp_ath.dat ]; then \
        echo '⚠️  interp output not found. Running interp...'; \
        ${CMAKE_BINARY_DIR}/bin/interp > ${DATATABLES_DIR}/interp_ath.dat; \
        echo '✅ interp output saved to ${DATATABLES_DIR}/interp_ath.dat'; \
    else \
        echo '✅ interp output already exists: ${DATATABLES_DIR}/interp_ath.dat'; \
        echo '   To regenerate, delete the file and run: make interp'; \
    fi"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running interp only if output doesn't exist"
    VERBATIM
)

# ============================================
# Output Directories for executables
# ============================================
set_target_properties(sigmav evolution interp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# ============================================
# Configure Kerrigan.sh for build directory
# ============================================
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/scripts/Kerrigan.sh.in
    ${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh
    @ONLY
)

file(CHMOD ${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
    GROUP_READ GROUP_EXECUTE
    WORLD_READ WORLD_EXECUTE
)

# ============================================
# Create wrapper script to run UI.py from build directory
# ============================================
set(UI_WRAPPER ${CMAKE_CURRENT_BINARY_DIR}/run_ui)

# Create the wrapper script content
file(WRITE ${UI_WRAPPER} "#!/usr/bin/env bash\n")
file(APPEND ${UI_WRAPPER} "# Wrapper script to run UI.py from the build directory\n")
file(APPEND ${UI_WRAPPER} "# Generated by CMake\n\n")
file(APPEND ${UI_WRAPPER} "# Set environment variables for the UI\n")
file(APPEND ${UI_WRAPPER} "export DATATABLES_DIR=\"${DATATABLES_DIR}\"\n")
file(APPEND ${UI_WRAPPER} "export BUILD_DIR=\"${CMAKE_CURRENT_BINARY_DIR}\"\n")
file(APPEND ${UI_WRAPPER} "export MG5_BASE_DIR=\"${FOLDER}\"\n\n")
file(APPEND ${UI_WRAPPER} "# Run the UI\n")
file(APPEND ${UI_WRAPPER} "cd \"${CMAKE_CURRENT_BINARY_DIR}\"\n")
file(APPEND ${UI_WRAPPER} "python3 \"${BUILD_UI_DIR}/UI.py\" \"\$@\"\n")

# Make the wrapper executable
file(CHMOD ${UI_WRAPPER}
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
    GROUP_READ GROUP_EXECUTE
    WORLD_READ WORLD_EXECUTE
)

message(STATUS "Created UI wrapper script: ${UI_WRAPPER}")

# ============================================
# Convenience targets
# ============================================
add_custom_target(ui
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/run_ui
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running UI.py"
    USES_TERMINAL
)

add_custom_target(run
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/scripts/Kerrigan.sh DM_test
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running Kerrigan.sh with default DM_test"
    USES_TERMINAL
)

add_custom_target(list_mg5
    COMMAND ls -d ${FOLDER}/*/ 2>/dev/null | xargs -n 1 basename
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Available MadGraph5 output folders:"
    USES_TERMINAL
)

# ============================================
# Install target
# ============================================
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin/
    DESTINATION bin
    USE_SOURCE_PERMISSIONS
)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/scripts/
    DESTINATION share/dark_matter/scripts
    USE_SOURCE_PERMISSIONS
)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/data/
    DESTINATION share/dark_matter/data
    USE_SOURCE_PERMISSIONS
)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/UI/
    DESTINATION share/dark_matter/UI
    USE_SOURCE_PERMISSIONS
)

install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/run_ui
    DESTINATION bin
    RENAME dark_matter_ui
)

# ============================================
# Status Messages
# ============================================
message(STATUS "")
message(STATUS "========================================")
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "MadGraph5 base directory: ${FOLDER}")
message(STATUS "MadGraph5 version: ${MG5_VERSION}")
message(STATUS "Build directory: ${CMAKE_CURRENT_BINARY_DIR}")
message(STATUS "========================================")
message(STATUS "Files in build directory:")
message(STATUS "  - Data files:      ${DATA_DIR}")
message(STATUS "  - Scripts:         ${SCRIPTS_DIR}")
message(STATUS "  - UI:              ${BUILD_UI_DIR}")
message(STATUS "========================================")
message(STATUS "Executables:")
message(STATUS "  - sigmav     : ${CMAKE_BINARY_DIR}/bin/sigmav")
message(STATUS "  - evolution  : ${CMAKE_BINARY_DIR}/bin/evolution")
message(STATUS "  - interp     : ${CMAKE_BINARY_DIR}/bin/interp")
message(STATUS "========================================")
message(STATUS "Usage:")
message(STATUS "  # Run the UI (main interface)")
message(STATUS "  cd ${CMAKE_CURRENT_BINARY_DIR}")
message(STATUS "  ./run_ui")
message(STATUS "  # Or use the make target:")
message(STATUS "  make ui")
message(STATUS "")
message(STATUS "  # Run Kerrigan.sh workflow")
message(STATUS "  ./scripts/Kerrigan.sh DM_test")
message(STATUS "  make run")
message(STATUS "========================================")
