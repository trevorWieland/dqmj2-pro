.section .text
.arm
.global saved_sdk_fill
.type saved_sdk_fill, @function
saved_sdk_fill:
cmp r2, #0
    bxeq lr
    tst r0, #1
    beq local_fill_even
    ldrh r12, [r0, #-1]
    and r12, r12, #255
    orr r3, r12, r1, lsl #8
    strh r3, [r0, #-1]
    add r0, r0, #1
    subs r2, r2, #1
    bxeq lr
local_fill_even:
    cmp r2, #2
    bcc local_fill_tail
    orr r1, r1, r1, lsl #8
    tst r0, #2
    beq local_fill_words
    strh r1, [r0], #2
    subs r2, r2, #2
    bxeq lr
local_fill_words:
    orr r1, r1, r1, lsl #16
    bics r3, r2, #3
    beq local_fill_halfword
    sub r2, r2, r3
    add r12, r3, r0
local_fill_word_loop:
    str r1, [r0], #4
    cmp r0, r12
    bcc local_fill_word_loop
local_fill_halfword:
    tst r2, #2
    strneh r1, [r0], #2
local_fill_tail:
    tst r2, #1
    bxeq lr
    ldrh r3, [r0]
    and r3, r3, #0xff00
    and r1, r1, #255
    orr r1, r1, r3
    strh r1, [r0]
    bx lr
.size saved_sdk_fill, .-saved_sdk_fill
