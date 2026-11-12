/* ov000 row 0x0220c4f4: 108 bytes.
 *
 * What it does: 27 instructions; 4 call(s) to 0x0220c550, 0x021d8c18, 0x0220a0d0, +1 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x5c
 *   branch +0x28 -> +0x64
 *   branch +0x44 -> +0x64
 *   branch +0x58 -> +0x64
 *   test +0x14 cmp r1, #1200
 *   test +0x24 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220c4f4; the literal pool and
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

extern void native_fn_021d8c18(void);
extern void native_fn_0220a0d0(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220c4f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    mov r4, #0
    cmp r1, #1200
    blt ov000_0220c4f4_L5c
    add r0, r5, #112
    bl native_fn_021d8c18
    cmp r0, #0
    bne ov000_0220c4f4_L64
    mov r0, r5
    bl native_fn_0220a0d0
    mov r2, #409600
    subs r0, r2, r0
    mov r2, r4
    sbcs r0, r2, r1
    bge ov000_0220c4f4_L64
    mov r0, r5
    mov r1, r2
    bl native_fn_02209c68
    mov r4, #1
    b ov000_0220c4f4_L64
ov000_0220c4f4_L5c:
    add r1, r1, #1
    strh r1, [r0, #122]
ov000_0220c4f4_L64:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
