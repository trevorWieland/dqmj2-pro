.section .text
.thumb
.global native_main_bios_020002ae
.type native_main_bios_020002ae, @function
native_main_bios_020002ae:
    swi 4
    bx lr
.size native_main_bios_020002ae, .-native_main_bios_020002ae
