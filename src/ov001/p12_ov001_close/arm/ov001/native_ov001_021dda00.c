/* ov001 row 0x021dda00: 128 bytes.
 *
 * What it does: 32 instructions; 6 call(s) to 0x02044424, 0x021db578, 0x02044424, +3 more; loops (back edge at +0x14); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 6 calls (32 instructions, 6 calls, 2 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x44 -> +0x58
 *   branch +0x64 -> +0x78
 *   test +0x04 cmp r0, #0
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r0, #4
 *   test +0x60 cmp r0, #0
 *   test +0x6c cmp r0, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dda00; the literal pool and
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

extern void native_fn_02044424(void);
extern void native_fn_021db578(void);
extern void native_fn_02044414(void);


asm u32 native_ov001_021dda00 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    cmp r0, #0
    moveq r4, #2
    movne r4, #3
    mov r0, #67108864
    bl native_fn_02044424
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_021db578
    cmp r0, #0
    movle r0, #0
    ldmleia sp!, {r4, pc}
    mov r0, #8388608
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_021dda00_L58
    bl native_fn_02044414
    cmp r0, #4
    movge r0, #0
    ldmgeia sp!, {r4, pc}
ov001_021dda00_L58:
    mov r0, #16777216
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_021dda00_L78
    bl native_fn_02044414
    cmp r0, #9
    movge r0, #0
    ldmgeia sp!, {r4, pc}
ov001_021dda00_L78:
    mov r0, #1
    ldmia sp!, {r4, pc}
}
