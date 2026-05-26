.PHONY: test sim-build sim clean all

all: test sim-build

test:
	$(MAKE) -C tests

sim-build:
	cmake -S zinc-simulator -B build/zinc-simulator -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
	cmake --build build/zinc-simulator
	ln -sf ../build/zinc-simulator/compile_commands.json zinc-simulator/compile_commands.json

sim: test sim-build
	build/zinc-simulator/zinc-simulator build/tests/add.bin

clean:
	$(MAKE) -C tests clean
