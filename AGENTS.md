项目背景
- 顶层 Makefile 使用 .DEFAULT_GOAL := all，make / make -jN 默认构建全部
- 子模块：zinc-compiler / zinc-rtl / zinc-simulator（git submodule）
- 第三方：third_party/spike（RISC-V ISA Simulator）、third_party/riscv-tests
- 构建产物统一放在 build/ 下（out-of-tree 构建）
- 系统依赖：riscv64-elf 工具链、libboost、device-tree-compiler（spike）