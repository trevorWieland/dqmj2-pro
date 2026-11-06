.syntax unified
.arm
.text
.p2align 2
.global native_main_02008c58
.type native_main_02008c58,%function
native_main_02008c58:
stmdb sp !, {r4 - r9}
    add r9, r1, r2
    mov r12, r2, lsr #5
    add r12, r1, r12, lsl #5
    mov r2, r0
    mov r3, r2
    mov r4, r2
    mov r5, r2
    mov r6, r2
    mov r7, r2
    mov r8, r2
.Lblock_loop:
    cmp r1, r12
    stmialt r1 !, {r0, r2 - r8}

    blt .Lblock_loop
.Lword_loop:
    cmp r1, r9
    stmialt r1 !, {r0}

    blt .Lword_loop
    ldmia sp !, {r4 - r9}
    bx lr
.size native_main_02008c58,.-native_main_02008c58
