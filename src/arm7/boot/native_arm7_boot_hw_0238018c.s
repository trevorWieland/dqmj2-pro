.section .text
.arm
.global native_arm7_boot_hw_0238018c
.type native_arm7_boot_hw_0238018c, @function
native_arm7_boot_hw_0238018c:
local_0238018c:
    mov r1, #0
local_02380190:
    ldr r2, local_023801fc
local_02380194:
    sub r3, r2, #0x400000
local_02380198:
    strh r1, [r2]
local_0238019c:
    ldrh ip, [r3]
local_023801a0:
    cmp r1, ip
local_023801a4:
    bne local_023801bc
local_023801a8:
    add r1, r1, #1
local_023801ac:
    cmp r1, #2
local_023801b0:
    bne local_02380198
local_023801b4:
    mov r0, #1
local_023801b8:
    b local_023801f0
local_023801bc:
    mov r1, #0
local_023801c0:
    sub r3, r3, #0x400000
local_023801c4:
    strh r1, [r2]
local_023801c8:
    ldr ip, [r3]
local_023801cc:
    cmp r1, ip
local_023801d0:
    bne local_023801d8
local_023801d4:
    b local_023801dc
local_023801d8:
    mov r0, #6
local_023801dc:
    bne local_023801f0
local_023801e0:
    add r1, r1, #1
local_023801e4:
    cmp r1, #2
local_023801e8:
    bne local_023801c4
local_023801ec:
    mov r0, #2
local_023801f0:
    ldr r2, local_02380200
local_023801f4:
    strh r0, [r2]
local_023801f8:
    bx lr
local_023801fc: .word 0x2fffffa
local_02380200: .word 0x27ffffa
.size native_arm7_boot_hw_0238018c, .-native_arm7_boot_hw_0238018c
