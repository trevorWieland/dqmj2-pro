.section .text
.thumb
.global native_main_bios_0200064a
.type native_main_bios_0200064a, @function
native_main_bios_0200064a:
    swi 0xb
    bx lr
.size native_main_bios_0200064a, .-native_main_bios_0200064a
