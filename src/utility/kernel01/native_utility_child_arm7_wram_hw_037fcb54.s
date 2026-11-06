.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fcb54
.type native_utility_child_arm7_wram_hw_037fcb54, @function
native_utility_child_arm7_wram_hw_037fcb54:
local_037fcb54:
    add r1, r0, #0
local_037fcb58:
    mrs r2, cpsr
local_037fcb5c:
    str r2, [r1], #4
local_037fcb60:
    mov r0, #0xd3
local_037fcb64:
    msr cpsr_c, r0
local_037fcb68:
    str sp, [r1, #0x40]
local_037fcb6c:
    msr cpsr_c, r2
local_037fcb70:
    mov r0, #1
local_037fcb74:
    stmia r1, {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, sp, lr}
local_037fcb78:
    add r0, pc, #8
local_037fcb7c:
    str r0, [r1, #0x3c]
local_037fcb80:
    mov r0, #0
local_037fcb84:
    bx lr
.size native_utility_child_arm7_wram_hw_037fcb54, .-native_utility_child_arm7_wram_hw_037fcb54
