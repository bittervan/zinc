ROOT_DIR := $(CURDIR)

include mk/spike.mk
include mk/riscv-tests.mk

.PHONY: clean all

all: riscv-tests

clean: clean-riscv-tests
