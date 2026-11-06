.section .text
.thumb
.global native_main_bios_020005ea
.type native_main_bios_020005ea, @function
native_main_bios_020005ea:
    swi 0xf
    bx lr
.size native_main_bios_020005ea, .-native_main_bios_020005ea
