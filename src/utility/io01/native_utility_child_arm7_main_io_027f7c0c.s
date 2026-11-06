.section .text
.arm
.global native_utility_child_arm7_main_io_027f7c0c
.type native_utility_child_arm7_main_io_027f7c0c, @function
native_utility_child_arm7_main_io_027f7c0c:
local_027f7c0c:
    mov ip, #0x4000000
local_027f7c10:
    add ip, ip, #0x138
local_027f7c14:
    mov r3, #2
local_027f7c18:
    subs r3, r3, #1
local_027f7c1c:
    bne local_027f7c18
local_027f7c20:
    ldrh r0, [ip]
local_027f7c24:
    bic r0, r0, #4
local_027f7c28:
    orr r0, r0, #0
local_027f7c2c:
    strh r0, [ip]
local_027f7c30:
    mov r3, #2
local_027f7c34:
    subs r3, r3, #1
local_027f7c38:
    bne local_027f7c34
local_027f7c3c:
    bx lr
.size native_utility_child_arm7_main_io_027f7c0c, .-native_utility_child_arm7_main_io_027f7c0c
