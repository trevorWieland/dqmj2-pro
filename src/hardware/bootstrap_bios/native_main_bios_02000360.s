.section .text
.thumb
.global native_main_bios_02000360
.type native_main_bios_02000360, @function
native_main_bios_02000360:
    swi 0x10
    bx lr
.size native_main_bios_02000360, .-native_main_bios_02000360
