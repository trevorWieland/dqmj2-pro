.section .text
.thumb
.global native_main_bios_020003e6
.type native_main_bios_020003e6, @function
native_main_bios_020003e6:
    mov r2, #0
    swi 5
    bx lr
.size native_main_bios_020003e6, .-native_main_bios_020003e6
