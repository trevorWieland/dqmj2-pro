/* ov001 row 0x02223f48: 160 bytes.
 *
 * What it does: 40 instructions; 5 call(s) to 0x0207afec, 0x021f07dc, 0x021dbd30, +2 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: block fill (40 instructions, 5 calls, 1 branch, 5 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x58
 *   test +0x2c cmp r0, #1
 *   1 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02223f48; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_021f0858(void);


asm u32 native_ov001_02223f48 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r5, r2
    mov r7, r0
    mov r0, r5
    mov r6, r1
    mov r4, r3
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_02223f48_L58
    mov r3, #0
    stmia sp, {r3, r4}
    mov r0, r7
    mov r1, r6
    mov r2, r5
    str r3, [sp, #0x8]
    bl native_fn_021f07dc
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
ov001_02223f48_L58:
    mov r0, r7
    bl native_fn_021dbd30
    ldr r2, [r7, #0x1e8]
    mov r1, r0
    mov r0, r5
    add r2, r2, #70
    bl native_fn_0207b244
    mov r1, #0
    str r1, [sp]
    mov r2, r0
    str r1, [sp, #0x4]
    mov r0, r7
    mov r1, r6
    mov r3, r5
    str r4, [sp, #0x8]
    bl native_fn_021f0858
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
