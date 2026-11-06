.section .text
.thumb
.global native_main_bios_020004fc
.type native_main_bios_020004fc, @function
native_main_bios_020004fc:
    swi 3
    bx lr
.size native_main_bios_020004fc, .-native_main_bios_020004fc
