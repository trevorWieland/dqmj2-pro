.section .text
.thumb
.global native_main_bios_0200043e
.type native_main_bios_0200043e, @function
native_main_bios_0200043e:
    swi 0x11
    bx lr
.size native_main_bios_0200043e, .-native_main_bios_0200043e
