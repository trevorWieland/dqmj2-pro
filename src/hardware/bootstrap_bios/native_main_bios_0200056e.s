.section .text
.thumb
.global native_main_bios_0200056e
.type native_main_bios_0200056e, @function
native_main_bios_0200056e:
    swi 0x12
    bx lr
.size native_main_bios_0200056e, .-native_main_bios_0200056e
