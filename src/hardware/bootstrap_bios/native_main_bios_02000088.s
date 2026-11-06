.section .text
.thumb
.global native_main_bios_02000088
.type native_main_bios_02000088, @function
native_main_bios_02000088:
    swi 0x13
    bx lr
.size native_main_bios_02000088, .-native_main_bios_02000088
