/* ov001 row 0x021e0cb8: 140 bytes.
 *
 * What it does: 34 instructions; 6 call(s) to 0x02203320, 0x02203320, 0x021e66f8, +3 more; no back edge; returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: branched body (34 instructions, 6 calls, 6 branches, 0 back edges, 1 literal slot).
 *
 *   pool +0x88 -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x34 -> +0x44
 *   branch +0x40 -> +0x74
 *   branch +0x48 -> +0x58
 *   branch +0x54 -> +0x74
 *   branch +0x5c -> +0x6c
 *   branch +0x68 -> +0x74
 *   test +0x10 cmp r0, #2
 *   test +0x24 cmp r0, #2
 *   test +0x30 cmp r4, #1
 *   test +0x44 cmp r4, #2
 *   test +0x58 cmp r4, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e0cb8; the literal pool and
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

extern void native_fn_02203320(void);
extern void native_fn_021e66f8(void);


asm u32 native_ov001_021e0cb8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    mov r0, r4
    bl native_fn_02203320
    cmp r0, #2
    orreq r0, r4, #1
    andeq r4, r0, #255
    mov r0, #1
    bl native_fn_02203320
    cmp r0, #2
    orreq r0, r4, #2
    andeq r4, r0, #255
    cmp r4, #1
    bne ov001_021e0cb8_L44
    mov r0, #10
    bl native_fn_021e66f8
    b ov001_021e0cb8_L74
ov001_021e0cb8_L44:
    cmp r4, #2
    bne ov001_021e0cb8_L58
    mov r0, #11
    bl native_fn_021e66f8
    b ov001_021e0cb8_L74
ov001_021e0cb8_L58:
    cmp r4, #3
    bne ov001_021e0cb8_L6c
    mov r0, #12
    bl native_fn_021e66f8
    b ov001_021e0cb8_L74
ov001_021e0cb8_L6c:
    mov r0, #10
    bl native_fn_021e66f8
ov001_021e0cb8_L74:
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
    mov r0, #0
    ldmia sp!, {r4, pc}
}
