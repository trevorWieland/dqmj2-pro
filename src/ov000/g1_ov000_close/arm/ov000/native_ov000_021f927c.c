/* ov000 row 0x021f927c: 192 bytes.
 *
 * What it does: 47 instructions; 3 call(s) to 0x02215698, 0x021f9118, 0x021f9148; loops (back edge at +0xa4); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xbc -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x40 -> +0x50
 *   branch +0x60 -> +0x74
 *   branch +0x78 -> +0xac
 *   branch +0xa8 -> +0xb4
 *   test +0x30 cmp r3, #0
 *   test +0x44 cmp r3, #0
 *   test +0x58 cmp r2, r1
 *   test +0x64 cmp r2, #0
 *   test +0x74 cmp r4, #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f927c; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_021f9118(void);
extern void native_fn_021f9148(void);


asm u32 native_ov000_021f927c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r5, r2
    mov r6, r1
    mov r4, r3
    bl native_fn_02215698
    add r1, r7, r5
    mov r1, r1, lsl #24
    add r2, r6, r4
    mov r3, r1, asr #24
    mov r1, r2, lsl #24
    mov r4, #0
    cmp r3, #0
    movgt r3, r4
    mov r2, r1, asr #24
    movgt r4, #1
    bgt ov000_021f927c_L50
    cmp r3, #0
    movlt r3, #3
    movlt r4, #1
ov000_021f927c_L50:
    add r1, r0, #1024
    ldrsb r1, [r1, #149]
    cmp r2, r1
    movge r2, #0
    bge ov000_021f927c_L74
    cmp r2, #0
    sublt r1, r1, #1
    movlt r1, r1, lsl #24
    movlt r2, r1, asr #24
ov000_021f927c_L74:
    cmp r4, #1
    bne ov000_021f927c_Lac
    add r0, r0, r2, lsl #3
    ldrb r1, [r0, #0xa5]
    ldr r2, =0x66666667
    mov r0, r3
    sub r3, r1, #48
    smull r1, r12, r2, r3
    mov r1, r3, lsr #31
    add r12, r1, r12, asr #4
    mov r1, r12, lsl #24
    mov r1, r1, asr #24
    bl native_fn_021f9118
    b ov000_021f927c_Lb4
ov000_021f927c_Lac:
    mov r0, r2
    bl native_fn_021f9148
ov000_021f927c_Lb4:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
