/* ov000 row 0x021f8838: 292 bytes.
 *
 * What it does: 72 instructions; 9 call(s) to 0x02215698, 0x0221744c, 0x02008c58, +6 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x120 -> constant 0x02236f28 (image word 0x02236f28)
 *   back edge +0x114 -> +0x64
 *   test +0x38 cmp r11, #0
 *   test +0x110 cmp r6, r11
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8838; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0221744c(void);
extern void native_fn_02008c58(void);
extern void native_fn_02062a50(void);
extern void native_fn_02044cdc(void);
extern void native_fn_0206ccb4(void);
extern void native_fn_0206cf44(void);
extern void native_fn_0206d250(void);


asm u32 native_ov000_021f8838 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    bl ov000_display_context_02215698
    mov r5, r0
    bl native_fn_0221744c
    add r1, r5, #1024
    ldrsb r11, [r1, #149]
    mov r7, #0
    str r0, [sp, #0x4]
    mov r0, r7
    add r1, r5, #160
    mov r2, #24
    mov r9, #48
    bl native_fn_02008c58
    cmp r11, #0
    mov r6, r7
    addle sp, sp, #16
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r5, #160
    add r1, r5, #150
    str r0, [sp, #0x8]
    add r0, r5, #1024
    ldr r10, =0x02236f28
    add r4, r1, #1024
    str r0, [sp, #0xc]
ov000_021f8838_L64:
    ldr r0, [sp, #0xc]
    ldr r1, [sp, #0x8]
    ldrsb r5, [r0, #150]
    mov r0, r6
    add r8, r1, r5, lsl #3
    bl native_fn_02062a50
    ldr r2, [r0, #0x14]
    ldr r1, [sp, #0x8]
    str r2, [r1, r5, lsl #3]
    mov r1, #16
    strb r1, [r8, #0x4]
    strb r9, [r8, #0x5]
    strb r7, [r8, #0x7]
    ldrsh r0, [r0, #24]
    bl native_fn_02044cdc
    ldrsb r1, [r10], #1
    add r0, r0, #1
    add r0, r7, r0
    strb r1, [r8, #0x6]
    mov r1, #3
    mov r0, r0, lsl #24
    str r1, [sp]
    mov r7, r0, asr #24
    ldrsb r1, [r8, #6]
    ldr r0, [sp, #0x4]
    mov r2, #2
    mov r3, #8
    bl native_fn_0206ccb4
    ldrsb r0, [r8, #6]
    mov r1, #16
    and r2, r9, #255
    bl native_fn_0206cf44
    ldrsb r0, [r4]
    add r0, r0, #1
    strb r0, [r4]
    ldrsb r0, [r8, #6]
    bl native_fn_0206d250
    add r1, r0, #1
    mov r0, #40
    mla r0, r1, r0, r9
    mov r0, r0, lsl #16
    add r6, r6, #1
    mov r9, r0, asr #16
    cmp r6, r11
    blt ov000_021f8838_L64
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
