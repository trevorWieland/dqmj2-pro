/* ov000 row 0x021e582c: 116 bytes.
 *
 * What it does: 29 instructions; 1 call(s) to 0x021e57f8; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x20 -> +0x6c
 *   8 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e582c; the literal pool and
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

extern void native_fn_021e57f8(void);


asm u32 native_ov000_021e582c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    mov r4, #0
    bl native_fn_021e57f8
    movs r12, r0
    beq ov000_021e582c_L6c
    mov r4, #1
    strb r4, [r12]
    strh r8, [r12, #2]
    add r3, r12, #16
    ldmia r7, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r12, #28
    ldmia r6, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r12, #40
    ldmia r5, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x18]
    add r3, r12, #52
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldrb r0, [sp, #0x1c]
    strb r0, [r12, #0x1]
ov000_021e582c_L6c:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
