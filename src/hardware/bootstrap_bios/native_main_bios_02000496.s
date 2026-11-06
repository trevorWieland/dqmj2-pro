.section .text
.thumb
.global native_main_bios_02000496
.type native_main_bios_02000496, @function
native_main_bios_02000496:
    swi 0
    bx lr
.size native_main_bios_02000496, .-native_main_bios_02000496
