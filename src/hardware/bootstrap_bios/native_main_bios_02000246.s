.section .text
.thumb
.global native_main_bios_02000246
.type native_main_bios_02000246, @function
native_main_bios_02000246:
    swi 6
    bx lr
.size native_main_bios_02000246, .-native_main_bios_02000246
