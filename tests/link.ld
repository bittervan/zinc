ENTRY(_start)
SECTIONS
{
    /* 假设你的处理器从 0x00000000 启动 */
    . = 0x00000000;
    .text : { *(.text) }
    .data : { *(.data) }
    .bss : { *(.bss) }
}