/* ov001 row 0x0221d438: 216 bytes.
 *
 * What it does: 53 instructions; 7 call(s) to 0x021db8d0, 0x021dbe5c, 0x021dbe5c, +4 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (53 instructions, 7 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0xd4 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x40 -> +0xb8
 *   branch +0x6c -> +0xb8
 *   back edge +0xc4 -> +0x34
 *   test +0x1c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x68 cmp r9, r2
 *   test +0xa8 cmp r0, r1, asr #1
 *   test +0xbc cmp r5, #3
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d438; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221d438 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r4, [r0]
    ldr r6, [r0, #0x8]
    ldrb r0, [r4, #0x356]
    mov r5, #0
    ldr r8, =0x66666667
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r4, #0x356]
    mov r11, r5
    mov r10, #1
    mov r7, #6
ov001_0221d438_L34:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221d438_Lb8
    mov r0, r4
    bl native_fn_021dbe5c
    mov r9, r0
    mov r0, r6
    bl native_fn_021dbe5c
    mul r1, r0, r7
    smull r0, r2, r8, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #1
    cmp r9, r2
    blt ov001_0221d438_Lb8
    str r11, [sp]
    mov r0, r4
    mov r1, r6
    mov r2, r11
    mov r3, r11
    stmib sp, {r10, r11}
    bl native_fn_021f07dc
    mov r9, r0
    mov r0, r6
    bl native_fn_021dbd24
    ldrb r2, [r4, #0x356]
    add r1, r9, r9, lsl #1
    mul r1, r2, r1
    add r1, r1, r1, lsr #31
    cmp r0, r1, asr #1
    addle sp, sp, #12
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0221d438_Lb8:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_0221d438_L34
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
