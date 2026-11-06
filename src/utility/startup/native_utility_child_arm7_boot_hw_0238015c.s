.section .text
.arm
.global native_utility_child_arm7_boot_hw_0238015c
.type native_utility_child_arm7_boot_hw_0238015c, @function
native_utility_child_arm7_boot_hw_0238015c:
local_0238015c:
    mov r0, #1
local_02380160:
    mov r1, #0
local_02380164:
    ldr r2, local_02380194
local_02380168:
    sub r3, r2, #0x400000
local_0238016c:
    strh r1, [r2]
local_02380170:
    ldrh ip, [r3]
local_02380174:
    cmp r1, ip
local_02380178:
    movne r0, #2
local_0238017c:
    bne local_0238018c
local_02380180:
    add r1, r1, #1
local_02380184:
    cmp r1, #2
local_02380188:
    bne local_0238016c
local_0238018c:
    strh r0, [r2]
local_02380190:
    bx lr
local_02380194: .word 0x27ffffa
.size native_utility_child_arm7_boot_hw_0238015c, .-native_utility_child_arm7_boot_hw_0238015c
