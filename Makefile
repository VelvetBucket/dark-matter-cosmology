# Root Makefile - delegates to CMake build system
# FOLDER should point to the base MadGraph5 directory

BUILD_DIR ?= build
FOLDER ?= $(error Please set FOLDER: make FOLDER=/path/to/MadGraph5_base)
CMAKE_OPTS ?= -DCMAKE_BUILD_TYPE=Release

# Default target - builds everything
all: sigmav evolution interp
	@echo "All executables built successfully!"

# Build the model library (matching original make -C src)
model:
	@mkdir -p $(BUILD_DIR)
	@if [ ! -f $(BUILD_DIR)/CMakeCache.txt ]; then \
		echo "First time build, configuring..."; \
		cd $(BUILD_DIR) && cmake .. -DFOLDER=$(FOLDER) $(CMAKE_OPTS); \
	fi
	@$(MAKE) -C $(BUILD_DIR) model_scotogenic_UFO

# Build sigmav (normal)
sigmav:
	@mkdir -p $(BUILD_DIR)
	@if [ ! -f $(BUILD_DIR)/CMakeCache.txt ]; then \
		echo "First time build, configuring..."; \
		cd $(BUILD_DIR) && cmake .. -DFOLDER=$(FOLDER) $(CMAKE_OPTS); \
	fi
	@$(MAKE) -C $(BUILD_DIR) sigmav

# Force rebuild sigmav (when process/ files change)
force-sigmav:
	@echo "Force rebuilding sigmav (process files changed)..."
	@rm -rf $(BUILD_DIR)/CMakeCache.txt $(BUILD_DIR)/CMakeFiles
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && cmake .. -DFOLDER=$(FOLDER) $(CMAKE_OPTS)
	@$(MAKE) -C $(BUILD_DIR) sigmav

# Build evolution
evolution:
	@mkdir -p $(BUILD_DIR)
	@if [ ! -f $(BUILD_DIR)/CMakeCache.txt ]; then \
		echo "First time build, configuring..."; \
		cd $(BUILD_DIR) && cmake .. -DFOLDER=$(FOLDER) $(CMAKE_OPTS); \
	fi
	@$(MAKE) -C $(BUILD_DIR) evolution

# Build interp
interp:
	@mkdir -p $(BUILD_DIR)
	@if [ ! -f $(BUILD_DIR)/CMakeCache.txt ]; then \
		echo "First time build, configuring..."; \
		cd $(BUILD_DIR) && cmake .. -DFOLDER=$(FOLDER) $(CMAKE_OPTS); \
	fi
	@$(MAKE) -C $(BUILD_DIR) interp

# Clean
clean:
	@rm -rf $(BUILD_DIR)
	@echo "Cleaned"

# Deep clean (remove everything including generated files)
distclean: clean
	@rm -rf output/*
	@rm -f process/*.cc process/*.h
	@echo "Deep cleaned"

# Help
help:
	@echo "========================================"
	@echo "Available targets:"
	@echo "========================================"
	@echo "  all          - Build everything"
	@echo "  model        - Build model library only"
	@echo "  sigmav       - Build sigmav (reuses existing build)"
	@echo "  force-sigmav - Force rebuild sigmav (use when process/ files change)"
	@echo "  evolution    - Build evolution"
	@echo "  interp       - Build interp"
	@echo "  clean        - Clean build directory"
	@echo "  distclean    - Deep clean (removes output and process files)"
	@echo "  help         - Show this help"
	@echo ""
	@echo "Required: FOLDER=/absolute/path/to/MadGraph5_base_directory"
	@echo "Example: make FOLDER=/home/user/MG5 sigmav"
	@echo ""
	@echo "For overseer.sh workflow:"
	@echo "  ./scripts/overseer.sh <output_folder_name>"
	@echo "  Example: ./scripts/overseer.sh DM_test"
	@echo "  This will use: /home/user/MG5/DM_test"
	@echo "========================================"

.PHONY: all model sigmav force-sigmav evolution interp clean distclean help
