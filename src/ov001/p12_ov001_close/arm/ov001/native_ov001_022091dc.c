/* ov001 row 0x022091dc: 228 bytes.
 *
 * What it does: 57 instructions; 8 call(s) to 0x021d8dec, 0x0203d294, 0x022092a8, +5 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 8 calls (57 instructions, 8 calls, 6 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x64
 *   branch +0x44 -> +0xcc
 *   branch +0x50 -> +0xcc
 *   branch +0x60 -> +0xcc
 *   branch +0x6c -> +0x98
 *   branch +0x78 -> +0xcc
 *   branch +0x84 -> +0xcc
 *   branch +0x94 -> +0xcc
 *   branch +0xa4 -> +0xcc
 *   branch +0xb0 -> +0xcc
 *   branch +0xbc -> +0xcc
 *   branch +0xd0 -> +0xdc
 *   test +0x18 cmp r0, #1
 *   test +0x30 cmp r1, #0
 *   test +0x34 cmpne r1, #5
 *   test +0x3c cmp r0, #1
 *   test +0x48 cmp r0, #3
 *   test +0x54 cmp r0, #5
 *   test +0x64 cmp r1, #1
 *   test +0x68 cmpne r1, #6
 *   test +0x70 cmp r0, #3
 *   test +0x7c cmp r0, #5
 *   test +0x88 cmp r0, #7
 *   test +0x98 cmp r1, #3
 *   test +0x9c cmpne r1, #8
 *   test +0xa8 cmp r0, #5
 *   test +0xb4 cmp r0, #6
 *   test +0xc0 cmp r0, #7
 *   test +0xcc cmp r6, #0
 *   test +0xd4 cmp r1, #5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022091dc; the literal pool and
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

extern void native_fn_021d8dec(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_022091dc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r1
    bl native_fn_021d8dec
    mov r4, r0
    ldrsb r5, [r4, #6]
    add r0, r5, #2
    cmp r0, #1
    movls r0, r5
    ldmlsia sp!, {r4, r5, r6, pc}
    mov r0, #8
    bl native_fn_0203d294
    ldrb r1, [r4, #0x2]
    cmp r1, #0
    cmpne r1, #5
    bne ov001_022091dc_L64
    cmp r0, #1
    addlt r5, r5, #1
    blt ov001_022091dc_Lcc
    cmp r0, #3
    addlt r5, r5, #2
    blt ov001_022091dc_Lcc
    cmp r0, #5
    addlt r5, r5, #3
    addge r5, r5, #4
    b ov001_022091dc_Lcc
ov001_022091dc_L64:
    cmp r1, #1
    cmpne r1, #6
    bne ov001_022091dc_L98
    cmp r0, #3
    addlt r5, r5, #1
    blt ov001_022091dc_Lcc
    cmp r0, #5
    addlt r5, r5, #2
    blt ov001_022091dc_Lcc
    cmp r0, #7
    addlt r5, r5, #3
    addge r5, r5, #4
    b ov001_022091dc_Lcc
ov001_022091dc_L98:
    cmp r1, #3
    cmpne r1, #8
    addeq r5, r5, #1
    beq ov001_022091dc_Lcc
    cmp r0, #5
    addlt r5, r5, #1
    blt ov001_022091dc_Lcc
    cmp r0, #6
    addlt r5, r5, #2
    blt ov001_022091dc_Lcc
    cmp r0, #7
    addlt r5, r5, #3
    addge r5, r5, #4
ov001_022091dc_Lcc:
    cmp r6, #0
    beq ov001_022091dc_Ldc
    cmp r1, #5
    addge r5, r5, #1
ov001_022091dc_Ldc:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
