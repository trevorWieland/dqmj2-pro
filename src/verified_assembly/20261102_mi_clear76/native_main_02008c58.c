typedef unsigned long u32;

asm void native_main_02008c58 (register u32 data, register void * destp, register u32 size)
{
    stmfd sp !, {r4 - r9}
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
@40:
    cmp r1, r12
    stmltia r1 !, {r0, r2 - r8}

    blt @40
@41:
    cmp r1, r9
    stmltia r1 !, {r0}

    blt @41
    ldmfd sp !, {r4 - r9}
    bx lr
}

typedef char verified_u32_width[(sizeof(u32)==4)?1:-1];
