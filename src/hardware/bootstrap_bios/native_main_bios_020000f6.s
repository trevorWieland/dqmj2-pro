.section .text
.thumb
.global native_main_bios_020000f6
.type native_main_bios_020000f6, @function
native_main_bios_020000f6:
    swi 0xe
    bx lr
.size native_main_bios_020000f6, .-native_main_bios_020000f6
