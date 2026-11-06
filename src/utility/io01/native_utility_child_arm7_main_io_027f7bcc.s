.section .text
.arm
.global native_utility_child_arm7_main_io_027f7bcc
.type native_utility_child_arm7_main_io_027f7bcc, @function
native_utility_child_arm7_main_io_027f7bcc:
local_027f7bcc:
    mov ip, #0x4000000
local_027f7bd0:
    add ip, ip, #0x138
local_027f7bd4:
    ldrh r0, [ip]
local_027f7bd8:
    bic r0, r0, #0x77
local_027f7bdc:
    orr r0, r0, #0x72
local_027f7be0:
    strh r0, [ip]
local_027f7be4:
    mov r3, #2
local_027f7be8:
    subs r3, r3, #1
local_027f7bec:
    bne local_027f7be8
local_027f7bf0:
    bic r0, r0, #4
local_027f7bf4:
    orr r0, r0, #4
local_027f7bf8:
    strh r0, [ip]
local_027f7bfc:
    mov r3, #2
local_027f7c00:
    subs r3, r3, #1
local_027f7c04:
    bne local_027f7c00
local_027f7c08:
    bx lr
.size native_utility_child_arm7_main_io_027f7bcc, .-native_utility_child_arm7_main_io_027f7bcc
