.section .text
.thumb
.global native_main_bios_020006c2
.type native_main_bios_020006c2, @function
native_main_bios_020006c2:
    swi 0x15
    bx lr
.size native_main_bios_020006c2, .-native_main_bios_020006c2
