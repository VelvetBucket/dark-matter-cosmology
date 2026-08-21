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
# Define data directory paths for executables AND Kerrigan.sh
# ============================================
set(DATA_DIR "${CMAKE_CURRENT_BINARY_DIR}/data")
set(CARDS_DIR "${DATA_DIR}/cards")
set(DATATABLES_DIR "${DATA_DIR}/datatables")

# Pass to C++ executables
add_definitions(-DDATA_DIR="${DATA_DIR}")
add_definitions(-DCARDS_DIR="${CARDS_DIR}")
add_definitions(-DDATATABLES_DIR="${DATATABLES_DIR}")

message(STATUS "Data directory definitions:")
message(STATUS "  - DATA_DIR: ${DATA_DIR}")
message(STATUS "  - CARDS_DIR: ${CARDS_DIR}")
message(STATUS "  - DATATABLES_DIR: ${DATATABLES_DIR}")

# ============================================
# Directories in the BUILD tree
# ============================================
set(SCRIPTS_DIR ${CMAKE_CURRENT_BINARY_DIR}/scripts)
set(MODEL_DIR ${CMAKE_CURRENT_BINARY_DIR}/model)
set(LIB_DIR ${CMAKE_CURRENT_BINARY_DIR}/lib)
set(PROCESS_DIR ${CMAKE_CURRENT_BINARY_DIR}/process)

# Create directories
file(MAKE_DIRECTORY ${MODEL_DIR})
file(MAKE_DIRECTORY ${LIB_DIR})
file(MAKE_DIRECTORY ${PROCESS_DIR})
file(MAKE_DIRECTORY ${DATA_DIR})
file(MAKE_DIRECTORY ${CARDS_DIR})
file(MAKE_DIRECTORY ${DATATABLES_DIR})
file(MAKE_DIRECTORY ${SCRIPTS_DIR})

# ============================================
# Copy TEMPLATE files from source to build
# ============================================
message(STATUS "Copying template files to build directory...")

# Copy template model files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/templates/model)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/templates/model
         DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    message(STATUS "  - Copied template model files to ${MODEL_DIR}")
else()
    message(WARNING "No template model files found in templates/model/")
endif()

# Copy template process files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/templates/process)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/templates/process
         DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    message(STATUS "  - Copied template process files to ${PROCESS_DIR}")
else()
    message(WARNING "No template process files found in templates/process/")
endif()

# Copy template library files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/templates/lib)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/templates/lib
         DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    message(STATUS "  - Copied template library files to ${LIB_DIR}")
else()
    message(WARNING "No template library files found in templates/lib/")
endif()

# ============================================
# Copy data files to build directory
# ============================================
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/data/cards)
    file(GLOB CARD_FILES "${CMAKE_CURRENT_SOURCE_DIR}/data/cards/*.dat")
    foreach(FILE ${CARD_FILES})
        get_filename_component(FILENAME ${FILE} NAME)
        configure_file(${FILE} ${CARDS_DIR}/${FILENAME} COPYONLY)
    endforeach()
    message(STATUS "Copied parameter cards to ${CARDS_DIR}")
else()
    message(WARNING "No cards found in ${CMAKE_CURRENT_SOURCE_DIR}/data/cards")
endif()

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/data/datatables)
    file(GLOB DATATABLE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/data/datatables/*.txt")
    foreach(FILE ${DATATABLE_FILES})
        get_filename_component(FILENAME ${FILE} NAME)
        configure_file(${FILE} ${DATATABLES_DIR}/${FILENAME} COPYONLY)
    endforeach()
    message(STATUS "Copied datatables to ${DATATABLES_DIR}")
else()
    message(WARNING "No datatables found in ${CMAKE_CURRENT_SOURCE_DIR}/data/datatables")
endif()

# ============================================
# Copy scripts to build directory
# ============================================
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/scripts/modify_template
         DESTINATION ${SCRIPTS_DIR})
    message(STATUS "Copied modify_template to ${SCRIPTS_DIR}/modify_template")
else()
    message(WARNING "No modify_template found in ${CMAKE_CURRENT_SOURCE_DIR}/scripts")
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
# Convenience targets
# ============================================
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
# Install target (optional)
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
message(STATUS "  - Data files:      ${DATA_DIR} (from source data/)")
message(STATUS "  - Scripts:         ${SCRIPTS_DIR} (from source scripts/)")
message(STATUS "  - Model files:     ${MODEL_DIR} (templates from templates/model/)")
message(STATUS "  - Process files:   ${PROCESS_DIR} (templates from templates/process/)")
message(STATUS "  - Libraries:       ${LIB_DIR} (templates from templates/lib/)")
message(STATUS "========================================")
message(STATUS "Note: Templates will be overwritten by")
message(STATUS "      ./scripts/Kerrigan.sh DM_test")
message(STATUS "========================================")
