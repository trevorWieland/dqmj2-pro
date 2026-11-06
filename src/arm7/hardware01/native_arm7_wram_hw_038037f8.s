.section .text
.thumb
.global native_arm7_wram_hw_038037f8
.type native_arm7_wram_hw_038037f8, @function
native_arm7_wram_hw_038037f8:
    swi 0xb
    bx lr
.size native_arm7_wram_hw_038037f8, .-native_arm7_wram_hw_038037f8
