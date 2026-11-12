/* ov001 row 0x0221d674: 92 bytes.
 *
 * What it does: 23 instructions; 5 call(s) to 0x021db8d0, 0x021dbd24, 0x021dbcbc, +2 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (23 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x38
 *   branch +0x34 -> +0x54
 *   back edge +0x50 -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x30 cmp r4, r0
 *   test +0x38 cmp r5, #2
 *   test +0x48 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d674; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_0221d674 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r6, [r0, #0x4]
    mov r5, #0
ov001_0221d674_Lc:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d674_L38
    mov r0, r6
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r6
    bl native_fn_021dbcbc
    cmp r4, r0
    blt ov001_0221d674_L54
ov001_0221d674_L38:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221d674_Lc
ov001_0221d674_L54:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
