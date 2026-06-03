SPIKE_BUILD_DIR := build/third_party/spike
SPIKE := $(SPIKE_BUILD_DIR)/spike
SPIKE_ISA ?= RV64I
SPIKE_PC ?= 0x80000000
SPIKE_INSTRUCTIONS ?= 128
CASE ?= add

.PHONY: test sim-build sim spike-build spike-run spike-trace difftest clean all

all: test sim-build

test:
	$(MAKE) -C tests

sim-build:
	cmake -S zinc-simulator -B build/zinc-simulator -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
	cmake --build build/zinc-simulator
	ln -sf ../build/zinc-simulator/compile_commands.json zinc-simulator/compile_commands.json

sim: test sim-build
	build/zinc-simulator/zinc-simulator build/tests/$(CASE).bin

$(SPIKE_BUILD_DIR)/Makefile:
	mkdir -p $(SPIKE_BUILD_DIR)
	cd $(SPIKE_BUILD_DIR) && ../../../third_party/spike/configure --prefix=$$(pwd)/install --with-target=riscv64-unknown-elf

$(SPIKE): $(SPIKE_BUILD_DIR)/Makefile
	$(MAKE) -C $(SPIKE_BUILD_DIR) -j$$(nproc)

spike-build: $(SPIKE)

spike-run: test spike-build
	$(SPIKE) --isa=$(SPIKE_ISA) --pc=$(SPIKE_PC) --instructions=$(SPIKE_INSTRUCTIONS) build/tests/$(CASE).elf

spike-trace: test spike-build
	$(SPIKE) --isa=$(SPIKE_ISA) --pc=$(SPIKE_PC) --instructions=$(SPIKE_INSTRUCTIONS) -l --log-commits build/tests/$(CASE).elf

difftest: test sim-build spike-build
	zinc-simulator/tools/difftest.py --steps $(SPIKE_INSTRUCTIONS) $(if $(filter command line,$(origin CASE)),--case $(CASE),)

clean:
	$(MAKE) -C tests clean
