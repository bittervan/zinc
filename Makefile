ROOT_DIR := $(CURDIR)
.DEFAULT_GOAL := all

include mk/spike.mk
include mk/riscv-tests.mk
include mk/zinc.mk

.PHONY: all clean

all: riscv-tests spike zinc

clean: clean-riscv-tests clean-spike clean-zinc
