.section .text
.thumb
.global native_main_bios_020007a6
.type native_main_bios_020007a6, @function
native_main_bios_020007a6:
    swi 0xc
    bx lr
.size native_main_bios_020007a6, .-native_main_bios_020007a6
