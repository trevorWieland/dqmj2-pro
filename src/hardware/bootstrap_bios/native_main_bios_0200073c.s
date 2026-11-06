.section .text
.thumb
.global native_main_bios_0200073c
.type native_main_bios_0200073c, @function
native_main_bios_0200073c:
    swi 9
    add r0, r1, #0
    bx lr
.size native_main_bios_0200073c, .-native_main_bios_0200073c
