/* ov001 row 0x021fe864: 112 bytes.
 *
 * What it does: 27 instructions; 4 call(s) to 0x02049ad0, 0x02202320, 0x0206006c, +1 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (27 instructions, 4 calls, 1 branch, 3 back edges, 1 literal slot).
 *
 *   pool +0x6c -> constant 0x02239de0 (image word 0x02239de0)
 *   branch +0x2c -> +0x54
 *   back edge +0x64 -> +0x10
 *   test +0x1c cmp r7, #0
 *   test +0x20 cmpne r1, #0
 *   test +0x28 cmpne r0, #127
 *   test +0x60 cmp r7, #36
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe864; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02202320(void);
extern void native_fn_0206006c(void);


asm u32 native_ov001_021fe864 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r5, =0x02239de0
    mov r7, #0
    mov r4, #12
ov001_021fe864_L10:
    mov r0, r7
    bl native_fn_02049ad0
    ldr r1, [r0]
    cmp r7, #0
    cmpne r1, #0
    ldrnesb r0, [r0, #5]
    cmpne r0, #127
    beq ov001_021fe864_L54
    ldr r6, [r1, #0x4]
    bl native_fn_02202320
    ldrsb r1, [r6, #95]
    mla r0, r4, r0, r5
    str r1, [sp]
    ldrsb r1, [r6, #92]
    ldrsb r2, [r6, #93]
    ldrsb r3, [r6, #94]
    bl native_fn_0206006c
ov001_021fe864_L54:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #36
    blt ov001_021fe864_L10
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
