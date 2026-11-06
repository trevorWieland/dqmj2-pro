.section .text
.thumb
.global native_utility_child_arm9_itcm_dma_01ff81b4
.type native_utility_child_arm9_itcm_dma_01ff81b4, @function
native_utility_child_arm9_itcm_dma_01ff81b4:
    push {r4, r5, r6}
    sub sp, #4
    mov r4, #12
    add r6, r0, #0
    mul r6, r4
    ldr r5, dma_registers
    add r4, r6, r5
    str r1, [r4]
    str r2, [r4, #4]
    str r3, [r4, #8]
    ldr r1, [r5]
    ldr r1, [r5]
    cmp r0, #0
    bne dma_completed
    mov r0, #0
    str r0, [r4]
    str r0, [r4, #4]
    ldr r0, dma_idle_control
    str r0, [r4, #8]
dma_completed:
    ldr r1, dma_registers
    ldr r0, [r1]
    ldr r0, [r1]
    add sp, #4
    pop {r4, r5, r6}
    bx lr
    mov r8, r8
dma_registers: .word 0x040000b0
dma_idle_control: .word 0x81400001
.size native_utility_child_arm9_itcm_dma_01ff81b4, .-native_utility_child_arm9_itcm_dma_01ff81b4
