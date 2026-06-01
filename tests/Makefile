ROOT := ..
BUILD_DIR := $(ROOT)/build/tests

CLANG ?= clang
OBJCOPY ?= llvm-objcopy

TARGET := riscv64-unknown-elf
ARCH := rv64i
ABI := lp64

ASFLAGS := --target=$(TARGET) -march=$(ARCH) -mabi=$(ABI)
CFLAGS := --target=$(TARGET) -march=$(ARCH) -mabi=$(ABI) -ffreestanding \
	-fno-builtin -nostdlib -O2 -Wall -Wextra
LDFLAGS := --target=$(TARGET) -march=$(ARCH) -mabi=$(ABI) -fuse-ld=lld -nostdlib \
	-Wl,-T,link.ld -Wl,--no-relax

TESTS := add
CRT0_OBJ := $(BUILD_DIR)/crt0.o
OBJS := $(addprefix $(BUILD_DIR)/,$(addsuffix .o,$(TESTS)))
ELFS := $(addprefix $(BUILD_DIR)/,$(addsuffix .elf,$(TESTS)))
BINS := $(addprefix $(BUILD_DIR)/,$(addsuffix .bin,$(TESTS)))

.PHONY: all clean
.SECONDARY: $(CRT0_OBJ) $(OBJS) $(ELFS)

all: $(ELFS) $(BINS)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/crt0.o: crt0.S | $(BUILD_DIR)
	$(CLANG) $(ASFLAGS) -c $< -o $@

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CLANG) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/%.elf: $(CRT0_OBJ) $(BUILD_DIR)/%.o link.ld
	$(CLANG) $(LDFLAGS) $(CRT0_OBJ) $(BUILD_DIR)/$*.o -o $@

$(BUILD_DIR)/%.bin: $(BUILD_DIR)/%.elf
	$(OBJCOPY) -O binary $< $@

clean:
	rm -rf $(BUILD_DIR)
