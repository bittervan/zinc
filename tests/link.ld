ENTRY(_start)

MEMORY
{
    ram (rwx) : ORIGIN = 0x80000000, LENGTH = 64K
}

SECTIONS
{
    . = ORIGIN(ram);

    .text : {
        *(.text.start)
        *(.text*)
    } > ram

    .rodata : {
        *(.rodata*)
    } > ram

    .data : {
        *(.sdata*)
        *(.data*)
    } > ram

    .bss : {
        *(.sbss*)
        *(.bss*)
        *(COMMON)
    } > ram

    . = ALIGN(16);
    _stack_top = ORIGIN(ram) + LENGTH(ram);
}
