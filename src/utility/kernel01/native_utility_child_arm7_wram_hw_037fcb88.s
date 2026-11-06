.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fcb88
.type native_utility_child_arm7_wram_hw_037fcb88, @function
native_utility_child_arm7_wram_hw_037fcb88:
local_037fcb88:
    mrs r1, cpsr
local_037fcb8c:
    bic r1, r1, #0x1f
local_037fcb90:
    orr r1, r1, #0xd3
local_037fcb94:
    msr cpsr_c, r1
local_037fcb98:
    ldr r1, [r0], #4
local_037fcb9c:
    msr spsr_fsxc, r1
local_037fcba0:
    ldr sp, [r0, #0x40]
local_037fcba4:
    ldr lr, [r0, #0x3c]
local_037fcba8:
    ldmia r0, {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, sp, lr} ^
local_037fcbac:
    mov r0, r0
local_037fcbb0:
    subs pc, lr, #4
.size native_utility_child_arm7_wram_hw_037fcb88, .-native_utility_child_arm7_wram_hw_037fcb88
