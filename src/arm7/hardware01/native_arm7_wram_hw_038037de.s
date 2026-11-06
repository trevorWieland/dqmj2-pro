.section .text
.thumb
.global native_arm7_wram_hw_038037de
.type native_arm7_wram_hw_038037de, @function
native_arm7_wram_hw_038037de:
    add r1, r0, #0
    mov r0, #1
    swi 8
    bx lr
.size native_arm7_wram_hw_038037de, .-native_arm7_wram_hw_038037de
