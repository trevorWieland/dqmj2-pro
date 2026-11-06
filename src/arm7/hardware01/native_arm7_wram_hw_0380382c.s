.section .text
.thumb
.global native_arm7_wram_hw_0380382c
.type native_arm7_wram_hw_0380382c, @function
native_arm7_wram_hw_0380382c:
    swi 0x1c
    bx lr
.size native_arm7_wram_hw_0380382c, .-native_arm7_wram_hw_0380382c
