.section .text
.thumb
.global native_main_bios_020001b8
.type native_main_bios_020001b8, @function
native_main_bios_020001b8:
    swi 0x14
    bx lr
.size native_main_bios_020001b8, .-native_main_bios_020001b8
