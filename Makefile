ROOT_DIR := $(CURDIR)
.DEFAULT_GOAL := all

include mk/spike.mk
include mk/riscv-tests.mk

.PHONY: all clean

all: riscv-tests spike

clean: clean-riscv-tests clean-spike
