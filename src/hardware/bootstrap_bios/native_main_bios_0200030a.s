.section .text
.thumb
.global native_main_bios_0200030a
.type native_main_bios_0200030a, @function
native_main_bios_0200030a:
    swi 9
    bx lr
.size native_main_bios_0200030a, .-native_main_bios_0200030a
