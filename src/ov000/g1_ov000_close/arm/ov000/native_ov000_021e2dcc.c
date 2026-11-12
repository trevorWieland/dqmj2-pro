/* ov000 row 0x021e2dcc: 228 bytes.
 *
 * What it does: 55 instructions; 3 call(s) to 0x020281b8, 0x020281b8, 0x021e3140; loops (back edge at +0x90); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xdc -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0xe0 -> constant 0x02232344 (image word 0x02232344)
 *   branch +0x1c -> +0xcc
 *   branch +0xa4 -> +0xd0
 *   branch +0xc8 -> +0xd0
 *   test +0x18 cmp r0, #1
 *   test +0xa0 cmp r7, r0
 *   2 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2dcc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020281b8(void);
extern void native_fn_021e3140(void);


asm u32 native_ov000_021e2dcc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #24
    ldr r5, =0x022322d4
    mov r4, #0
    ldrb r0, [r5, #0x27f]
    ldr r6, =0x02232344
    cmp r0, #1
    bne ov000_021e2dcc_Lcc
    ldr r1, [r6]
    ldr r0, [r5, #0x1e8]
    ldr r2, [r5, #0x200]
    sub lr, r1, r0
    sub r9, r2, r1
    ldr r1, [r6, #0x4]
    ldr r0, [r5, #0x1ec]
    ldr r3, [r5, #0x204]
    sub r12, r1, r0
    sub r8, r3, r1
    sub r1, r3, r12
    sub r2, r2, lr
    ldr r7, [r6, #0x8]
    ldr r3, [r5, #0x1f0]
    ldr r0, [r5, #0x208]
    sub r3, r7, r3
    sub r7, r0, r7
    sub r10, r0, r3
    add r0, sp, #12
    str r9, [sp, #0xc]
    str r8, [sp, #0x10]
    str r7, [sp, #0x14]
    str lr, [r6]
    str r12, [r6, #0x4]
    str r3, [r6, #0x8]
    str r2, [sp]
    str r1, [sp, #0x4]
    str r10, [sp, #0x8]
    bl native_fn_020281b8
    mov r7, r0
    add r0, sp, #0
    bl native_fn_020281b8
    cmp r7, r0
    bgt ov000_021e2dcc_Ld0
    add r0, r5, #512
    ldmia r0, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    bl native_fn_021e3140
    mov r1, r4
    mov r0, r5
    strb r1, [r5, #0x210]
    strb r1, [r0, #0x27f]
    b ov000_021e2dcc_Ld0
ov000_021e2dcc_Lcc:
    mov r4, #1
ov000_021e2dcc_Ld0:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
