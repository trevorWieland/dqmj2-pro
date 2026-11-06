.section .text
.thumb
.global native_main_bios_02000156
.type native_main_bios_02000156, @function
native_main_bios_02000156:
    swi 0xd
    bx lr
.size native_main_bios_02000156, .-native_main_bios_02000156
