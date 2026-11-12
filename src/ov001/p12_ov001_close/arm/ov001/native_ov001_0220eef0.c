/* ov001 row 0x0220eef0: 224 bytes.
 *
 * What it does: 54 instructions; 4 call(s) to 0x0207afec, 0x0207afec, 0x0207afec, +1 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (54 instructions, 4 calls, 6 branches, 4 back edges, 2 literal slots).
 *
 *   pool +0xd8 -> native_data_0222e0e8 (image word 0x0222e0e8)
 *   pool +0xdc -> constant 0x55555556 (image word 0x55555556)
 *   branch +0x34 -> +0x54
 *   branch +0x50 -> +0xd0
 *   back edge +0x78 -> +0x5c
 *   branch +0x80 -> +0x98
 *   branch +0x88 -> +0xac
 *   branch +0x90 -> +0xbc
 *   branch +0x94 -> +0xd0
 *   test +0x30 cmp r0, #1
 *   test +0x4c cmp r0, #7
 *   test +0x60 cmp r4, r0
 *   test +0x70 cmp r1, #9
 *   test +0x7c cmp r5, #2
 *   test +0x84 cmp r5, #121
 *   test +0x8c cmp r5, #122
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220eef0; the literal pool and
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
extern u8 native_data_0222e0e8[];


asm u32 native_ov001_0220eef0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r6, r1
    mov r5, r2
    bl native_fn_0207afec
    mov r4, r0
    mov r0, r7
    bl native_fn_0207afec
    ldrh r1, [r4, #8]
    ldrb r4, [r0, #0x1f]
    mov r0, r1, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    beq ov001_0220eef0_L54
    mov r0, r7
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #7
    bne ov001_0220eef0_Ld0
ov001_0220eef0_L54:
    ldr r2, =native_data_0222e0e8
    mov r1, #0
ov001_0220eef0_L5c:
    ldrb r0, [r2]
    cmp r4, r0
    moveq r0, r6
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    add r1, r1, #1
    cmp r1, #9
    add r2, r2, #1
    blt ov001_0220eef0_L5c
    cmp r5, #2
    beq ov001_0220eef0_L98
    cmp r5, #121
    beq ov001_0220eef0_Lac
    cmp r5, #122
    beq ov001_0220eef0_Lbc
    b ov001_0220eef0_Ld0
ov001_0220eef0_L98:
    ldr r2, =0x55555556
    add r3, r6, #2
    smull r1, r0, r2, r3
    add r0, r0, r3, lsr #31
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0220eef0_Lac:
    add r0, r6, #1
    add r0, r0, r0, lsr #31
    mov r0, r0, asr #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0220eef0_Lbc:
    add r1, r6, #3
    mov r0, r1, asr #1
    add r0, r1, r0, lsr #30
    mov r0, r0, asr #2
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0220eef0_Ld0:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
