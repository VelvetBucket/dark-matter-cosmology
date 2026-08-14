cmake_minimum_required(VERSION 3.10)
project(dark_matter_cosmology VERSION 1.0.0 LANGUAGES CXX)

# --- REQUIRED FOLDER VARIABLE (Base MadGraph5 directory) ---
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
message(STATUS "When running overseer.sh, specify the output folder name")
message(STATUS "Example: ./scripts/overseer.sh DM_test")
# --- END REQUIRED FOLDER ---

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
add_definitions(-D_USE_MATH_DEFINES)

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast -g")
if(NOT MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
    
    # Suppress common warnings in generated code
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-parameter")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-but-set-variable")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function")
    
    # Suppress misleading indentation warnings
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-misleading-indentation")
    
    # Suppress multi-line comment warnings
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-comment")
    
endif()

# Set directories
set(LIBDIR ${CMAKE_CURRENT_SOURCE_DIR}/external/lib)
set(MODELLIB model_scotogenic_UFO)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/model
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/process
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core/tools
    ${CMAKE_CURRENT_SOURCE_DIR}/process           # CPPProcess files copied here
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Link directories
link_directories(${LIBDIR})

# ----------------------------
# Model Library (from MadGraph5)
# ----------------------------
set(MODEL_SOURCES
    src/core/model/HelAmps_scotogenic_UFO.cc
    src/core/model/Parameters_scotogenic_UFO.cc
    src/core/model/rambo.cc
    src/core/model/read_slha.cc
)

add_library(${MODELLIB} STATIC ${MODEL_SOURCES})
target_include_directories(${MODELLIB} PUBLIC src/core/model)
set_target_properties(${MODELLIB} PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${LIBDIR}
)

# ----------------------------
# Core Library (your tools + process)
# ----------------------------
set(CORE_SOURCES
    # Process files (copied from MadGraph5 by overseer.sh)
    process/CPPProcess.cc
    src/core/process/momenta.cc
    # Your tools
    src/core/tools/integration.cc
    src/core/tools/bessel.cc
    src/core/tools/data_handling.cc
    src/core/tools/interpolation.cc
)

add_library(core_lib STATIC ${CORE_SOURCES})
target_include_directories(core_lib PUBLIC 
    src/core
    src/core/process
    src/core/tools
    process                         # For CPPProcess.h
)
target_link_libraries(core_lib ${MODELLIB})

# ----------------------------
# sigmav executable - REBUILT when process/ changes
# ----------------------------
add_executable(sigmav src/main/sigmav.cpp)
target_link_libraries(sigmav core_lib gsl gslcblas m)
add_dependencies(sigmav core_lib)

# ----------------------------
# evolution and interp - INDEPENDENT
# ----------------------------
add_executable(evolution src/main/evolution.cpp)
target_link_libraries(evolution core_lib)

add_executable(interp src/main/interp.cpp)
target_link_libraries(interp core_lib)

# ----------------------------
# Output Directories
# ----------------------------
set_target_properties(sigmav evolution interp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# ----------------------------
# Configure overseer.sh with FOLDER
# ----------------------------
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/scripts/overseer.sh.in
    ${CMAKE_CURRENT_BINARY_DIR}/overseer.sh
    @ONLY
)

file(CHMOD ${CMAKE_CURRENT_BINARY_DIR}/overseer.sh
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
    GROUP_READ GROUP_EXECUTE
    WORLD_READ WORLD_EXECUTE
)

# ----------------------------
# Copy the script to root for convenience
# ----------------------------
add_custom_target(install_overseer
    COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_CURRENT_BINARY_DIR}/overseer.sh
        ${CMAKE_CURRENT_SOURCE_DIR}/scripts/overseer.sh
    COMMENT "Installing overseer.sh to scripts directory"
)

# ----------------------------
# Status Messages
# ----------------------------
message(STATUS "")
message(STATUS "========================================")
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "MadGraph5 base directory: ${FOLDER}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "========================================")
message(STATUS "Executables:")
message(STATUS "  - sigmav     : sigma*v calculation (rebuild when process/ changes)")
message(STATUS "  - evolution : Evolution calculation")
message(STATUS "  - interp    : Interpolation calculation")
message(STATUS "========================================")
message(STATUS "Usage:")
message(STATUS "  ./scripts/overseer.sh <output_folder>")
message(STATUS "  Example: ./scripts/overseer.sh DM_test")
message(STATUS "  This will use: ${FOLDER}/DM_test")
message(STATUS "========================================")
