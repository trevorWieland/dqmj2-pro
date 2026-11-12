/* ov001 row 0x02222208: 180 bytes.
 *
 * What it does: 45 instructions; 7 call(s) to 0x021db8d0, 0x022186d0, 0x021dc1c0, +4 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: block load (45 instructions, 7 calls, 5 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x9c
 *   branch +0x30 -> +0x9c
 *   branch +0x40 -> +0x9c
 *   branch +0x50 -> +0x9c
 *   branch +0x68 -> +0x84
 *   back edge +0x90 -> +0x5c
 *   back edge +0xa8 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x88 cmp r6, #3
 *   test +0xa0 cmp r6, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02222208; the literal pool and
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
extern void native_fn_022186d0(void);
extern void native_fn_021dc1c0(void);
extern void native_fn_02218498(void);


asm u32 native_ov001_02222208 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldmib r0, {r4, r7}
    mov r6, #0
    mov r5, #219
ov001_02222208_L10:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02222208_L9c
    mov r0, r7
    mov r1, r5
    bl native_fn_022186d0
    cmp r0, #0
    beq ov001_02222208_L9c
    add r0, r7, #512
    ldrsb r0, [r0, #84]
    cmp r0, #0
    bne ov001_02222208_L9c
    mov r0, r7
    bl native_fn_021dc1c0
    cmp r0, #0
    beq ov001_02222208_L9c
    mov r6, #0
    mov r5, #2
ov001_02222208_L5c:
    mov r0, r4
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02222208_L84
    mov r0, r4
    mov r1, r5
    bl native_fn_02218498
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02222208_L84:
    add r6, r6, #1
    cmp r6, #3
    add r4, r4, #1088
    blt ov001_02222208_L5c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02222208_L9c:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02222208_L10
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
