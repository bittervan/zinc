CMAKE ?= cmake
ZINC_BUILD := $(ROOT_DIR)/build/zinc
ZINC_CMAKE_TIMESTAMP := $(ZINC_BUILD)/CMakeCache.txt

.PHONY: zinc

zinc: $(ZINC_CMAKE_TIMESTAMP)
	$(CMAKE) --build $(ZINC_BUILD)

$(ZINC_CMAKE_TIMESTAMP): CMakeLists.txt sim/CMakeLists.txt
	$(CMAKE) -S $(ROOT_DIR) \
			-B $(ZINC_BUILD) \
			-DCMAKE_EXPORT_COMPILE_COMMANDS=ON

.PHONY: clean-zinc

clean-zinc:
	rm -rf $(ZINC_BUILD)