.section .text
.thumb
.global native_arm7_wram_hw_038037e6
.type native_arm7_wram_hw_038037e6, @function
native_arm7_wram_hw_038037e6:
    add r1, r0, #0
    mov r0, #0
    swi 8
    bx lr
.size native_arm7_wram_hw_038037e6, .-native_arm7_wram_hw_038037e6
