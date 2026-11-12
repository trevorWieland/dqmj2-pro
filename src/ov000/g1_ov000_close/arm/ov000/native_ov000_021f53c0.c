/* ov000 row 0x021f53c0: 344 bytes.
 *
 * What it does: 85 instructions; 11 call(s) to 0x020624c0, 0x020624c0, 0x02223ec0, +8 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x154 -> native_data_0222b964 (image word 0x0222b964)
 *   branch +0xbc -> +0x138
 *   branch +0xf0 -> +0x104
 *   branch +0x100 -> +0x120
 *   back edge +0x148 -> +0x98
 *   test +0xb8 cmp r6, #0
 *   test +0xc8 cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   test +0xe8 cmp r9, #0
 *   test +0x144 cmp r7, #3
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f53c0; the literal pool and
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

extern u8 native_data_0222b964[];
extern void native_fn_020624c0(void);
extern void native_fn_02223ec0(void);
extern void native_fn_02045dc4(void);
extern void native_fn_02223d40(void);
extern void native_fn_02223d70(void);
extern void native_fn_02223e58(void);
extern void native_fn_021f5518(void);


asm u32 native_ov000_021f53c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222b964
    mov r0, #19
    ldrb r2, [r1]
    ldrb r1, [r1, #0x1]
    mov r8, #0
    strb r2, [sp, #0x8]
    strb r1, [sp, #0x9]
    bl native_fn_020624c0
    mov r10, r0
    mov r0, #19
    bl native_fn_020624c0
    bl native_fn_02223ec0
    ldrb r4, [sp, #0x9]
    ldrb r5, [sp, #0x8]
    mov r0, #5
    str r0, [sp]
    mov r0, #15
    str r0, [sp, #0x4]
    mov r0, r8
    mov r1, #1
    mov r2, r5
    mov r3, r4
    bl native_fn_02045dc4
    mov r0, #5
    str r0, [sp]
    mov r0, #15
    str r0, [sp, #0x4]
    mov r2, r5
    mov r3, r4
    mov r0, r8
    mov r1, #2
    bl native_fn_02045dc4
    mov r7, r8
    mov r5, r8
    mov r11, r8
    mov r4, #5
ov000_021f53c0_L98:
    mov r0, r10
    mov r1, r7
    bl native_fn_02223d40
    mov r6, r0
    mov r0, r10
    mov r1, r7
    bl native_fn_02223d70
    mov r9, r0
    cmp r6, #0
    beq ov000_021f53c0_L138
    ldrsh r0, [r6, #24]
    mov r1, r7
    cmp r0, #0
    mov r0, r10
    moveq r9, r5
    bl native_fn_02223e58
    cmp r0, #0
    add r0, r8, #3
    movne r9, r11
    mov r0, r0, lsl #24
    cmp r9, #0
    mov r0, r0, asr #24
    beq ov000_021f53c0_L104
    ldrsb r1, [sp, #8]
    ldrsb r2, [sp, #9]
    bl native_fn_021f5518
    b ov000_021f53c0_L120
ov000_021f53c0_L104:
    ldrb r2, [sp, #0x8]
    ldrb r3, [sp, #0x9]
    str r4, [sp]
    mov r0, #0
    mov r1, #1
    str r4, [sp, #0x4]
    bl native_fn_02045dc4
ov000_021f53c0_L120:
    ldrsb r1, [sp, #9]
    add r0, r8, #1
    mov r0, r0, lsl #24
    add r1, r1, #5
    strb r1, [sp, #0x9]
    mov r8, r0, asr #24
ov000_021f53c0_L138:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    blt ov000_021f53c0_L98
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
