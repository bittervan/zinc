ROOT_DIR := $(CURDIR)

RISCV_TESTS_SRC := $(ROOT_DIR)/third_party/riscv-tests
RISCV_TESTS_BUILD := $(ROOT_DIR)/build/riscv-tests
RISCV_TESTS_ISA_BUILD := $(RISCV_TESTS_BUILD)/isa
RISCV_TESTS_INSTALL := $(RISCV_TESTS_BUILD)/install

RISCV_TARGET ?= riscv64-elf
RISCV_PREFIX := $(RISCV_TARGET)-
RISCV_TESTS_TARGETS := rv64ui rv64uf

.PHONY: riscv-tests
riscv-tests: $(RISCV_TESTS_BUILD)/Makefile $(RISCV_TESTS_ISA_BUILD)
	$(MAKE) -C $(RISCV_TESTS_ISA_BUILD) \
		-f $(RISCV_TESTS_SRC)/isa/Makefile \
		src_dir=$(RISCV_TESTS_SRC)/isa \
		XLEN=64 \
		RISCV_PREFIX=$(RISCV_PREFIX) \
		rv64ui_v_tests= \
		rv64uf_v_tests= \
		$(RISCV_TESTS_TARGETS)

$(RISCV_TESTS_BUILD)/Makefile: $(RISCV_TESTS_SRC)/configure
	mkdir -p $(RISCV_TESTS_BUILD)
	cd $(RISCV_TESTS_BUILD) && \
			$(RISCV_TESTS_SRC)/configure \
					--target=$(RISCV_TARGET) \
					--prefix=$(RISCV_TESTS_INSTALL)

$(RISCV_TESTS_SRC)/configure:
	git submodule update --init third_party/riscv-tests

$(RISCV_TESTS_SRC)/env/p/riscv_test.h:
	git -C $(RISCV_TESTS_SRC) config submodule.env.url git@github.com:riscv/riscv-test-env.git
	git -C $(RISCV_TESTS_SRC) submodule update --init env

$(RISCV_TESTS_BUILD)/Makefile: $(RISCV_TESTS_SRC)/env/p/riscv_test.h

$(RISCV_TESTS_ISA_BUILD):
	mkdir -p $@

.PHONY: clean-riscv-tests
clean-riscv-tests:
	rm -rf $(RISCV_TESTS_BUILD)
