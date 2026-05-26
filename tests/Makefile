ROOT := ..
BUILD_DIR := $(ROOT)/build/tests

CLANG ?= clang
OBJCOPY ?= llvm-objcopy

TARGET := riscv32-unknown-elf
ARCH := rv32i
ABI := ilp32

ASFLAGS := --target=$(TARGET) -march=$(ARCH) -mabi=$(ABI)
LDFLAGS := --target=$(TARGET) -march=$(ARCH) -mabi=$(ABI) -fuse-ld=lld -nostdlib \
	-Wl,-T,link.ld -Wl,--no-relax

TESTS := add
BINS := $(addprefix $(BUILD_DIR)/,$(addsuffix .bin,$(TESTS)))

.PHONY: all clean

all: $(BINS)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/%.o: %.S | $(BUILD_DIR)
	$(CLANG) $(ASFLAGS) -c $< -o $@

$(BUILD_DIR)/%.elf: $(BUILD_DIR)/%.o link.ld
	$(CLANG) $(LDFLAGS) $< -o $@

$(BUILD_DIR)/%.bin: $(BUILD_DIR)/%.elf
	$(OBJCOPY) -O binary $< $@

clean:
	rm -rf $(BUILD_DIR)
