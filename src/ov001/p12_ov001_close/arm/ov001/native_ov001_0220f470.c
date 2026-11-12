/* ov001 row 0x0220f470: 192 bytes.
 *
 * What it does: 48 instructions; 6 call(s) to 0x021e81d0, 0x0207afec, 0x0207afec, +3 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (48 instructions, 6 calls, 6 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x4c
 *   branch +0x58 -> +0xb8
 *   branch +0x80 -> +0xb8
 *   branch +0x90 -> +0xb8
 *   branch +0xa0 -> +0xb8
 *   branch +0xa8 -> +0xb8
 *   test +0x30 cmp r0, #2
 *   test +0x44 cmp r0, #1
 *   test +0x54 cmp r0, #0
 *   test +0x64 cmp r1, #0
 *   test +0x6c cmpeq r1, #0
 *   test +0x74 cmpeq r1, #0
 *   test +0x7c cmpeq r0, #0
 *   test +0x8c cmp r0, #0
 *   test +0x9c cmp r0, #0
 *   test +0xa4 cmp r4, #0
 *   test +0xac cmp r5, #84
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220f470; the literal pool and
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

extern void native_fn_021e81d0(void);
extern void native_fn_0207afec(void);
extern void native_fn_021dc108(void);
extern void native_fn_021dcda8(void);
extern void native_fn_021dc190(void);


asm u32 native_ov001_0220f470 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldrb r0, [r6, #0x31e]
    ldrb r1, [r6, #0x31f]
    mov r4, #0
    bl native_fn_021e81d0
    ldrh r5, [r0]
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #2
    bne ov001_0220f470_L4c
    mov r0, r5
    bl native_fn_0207afec
    ldrsh r0, [r0, #16]
    cmp r0, #1
    movgt r4, #1
ov001_0220f470_L4c:
    mov r0, r6
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0220f470_Lb8
    add r0, r6, #512
    ldrsb r1, [r0, #77]
    cmp r1, #0
    ldreqsb r1, [r0, #69]
    cmpeq r1, #0
    ldreqsb r1, [r0, #81]
    cmpeq r1, #0
    ldreqsb r0, [r0, #55]
    cmpeq r0, #0
    bne ov001_0220f470_Lb8
    mov r0, r6
    bl native_fn_021dcda8
    cmp r0, #0
    bne ov001_0220f470_Lb8
    mov r0, r6
    bl native_fn_021dc190
    cmp r0, #0
    beq ov001_0220f470_Lb8
    cmp r4, #0
    bne ov001_0220f470_Lb8
    cmp r5, #84
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
ov001_0220f470_Lb8:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
