/* ov001 row 0x0221ac78: 112 bytes.
 *
 * What it does: 28 instructions; 6 call(s) to 0x0221fae4, 0x021db8d0, 0x021dbd24, +3 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (28 instructions, 6 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0x68
 *   branch +0x24 -> +0x4c
 *   branch +0x48 -> +0x68
 *   back edge +0x64 -> +0x18
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x44 cmp r4, r0, asr #2
 *   test +0x4c cmp r5, #2
 *   test +0x5c cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221ac78; the literal pool and
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

extern void native_fn_0221fae4(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221ac78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r6, [r0, #0x4]
    bl native_fn_0221fae4
    cmp r0, #0
    beq ov001_0221ac78_L68
    mov r5, #0
ov001_0221ac78_L18:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221ac78_L4c
    mov r0, r6
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r6
    bl native_fn_021dbcbc
    mov r1, r0, asr #1
    add r0, r0, r1, lsr #30
    cmp r4, r0, asr #2
    blt ov001_0221ac78_L68
ov001_0221ac78_L4c:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221ac78_L18
ov001_0221ac78_L68:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
