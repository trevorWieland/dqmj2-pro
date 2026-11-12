/* ov000 row 0x021f6e84: 460 bytes.
 *
 * What it does: 115 instructions; 17 call(s) to 0x02061944, 0x020624c0, 0x021f7050, +14 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x5c -> +0x68
 *   branch +0xa8 -> +0xb8
 *   branch +0xd4 -> +0x124
 *   back edge +0x120 -> +0xe4
 *   branch +0x164 -> +0x178
 *   back edge +0x1c0 -> +0x8c
 *   test +0x2c cmp r0, #28
 *   test +0x58 cmp r1, #28
 *   test +0x7c cmp r0, #0
 *   test +0xa4 cmp r1, #28
 *   test +0xd0 cmp r0, #0
 *   test +0x11c cmp r0, r4, asr #24
 *   test +0x160 cmp r0, #100
 *   test +0x17c cmp r0, #1
 *   test +0x1ac cmp r0, r3, asr #24
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f6e84; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_020624c0(void);
extern void native_fn_021f7050(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021f70a4(void);


asm u32 native_ov000_021f6e84 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    str r0, [sp, #0xc]
    mov r0, #19
    bl native_fn_020624c0
    ldr r0, [sp, #0xc]
    mov r1, #1
    add r0, r0, #512
    ldrsb r0, [r0, #105]
    mov r2, #6
    cmp r0, #28
    movlt r0, #10
    movge r0, #11
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f7050
    bl native_fn_02062aa0
    ldr r1, [sp, #0xc]
    str r0, [sp, #0x8]
    add r1, r1, #512
    ldrsb r1, [r1, #105]
    cmp r1, #28
    blt ov000_021f6e84_L68
    bl native_fn_02062ad0
    str r0, [sp, #0x8]
ov000_021f6e84_L68:
    mov r0, #0
    str r0, [sp, #0x4]
    mov r5, r0
    ldr r0, [sp, #0x8]
    mov r7, #8
    cmp r0, #0
    mov r8, r7
    addle sp, sp, #16
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021f6e84_L8c:
    mov r0, r5
    bl native_fn_02062a50
    ldr r1, [sp, #0xc]
    mov r9, r0
    add r1, r1, #512
    ldrsb r1, [r1, #105]
    cmp r1, #28
    blt ov000_021f6e84_Lb8
    mov r0, r5
    bl native_fn_02062a88
    mov r9, r0
ov000_021f6e84_Lb8:
    ldrsh r0, [r9, #24]
    bl native_fn_02044cdc
    str r0, [sp]
    ldrsh r0, [r9, #24]
    mov r6, #0
    bl native_fn_02044cdc
    cmp r0, #0
    blt ov000_021f6e84_L124
    ldr r0, [sp, #0x4]
    mov r11, #1
    add r10, r0, #2
ov000_021f6e84_Le4:
    mov r0, r10, lsl #24
    mov r1, r11
    mov r2, r7
    mov r0, r0, asr #24
    bl native_fn_021f7050
    add r0, r7, #5
    add r1, r6, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    mov r4, r1, lsl #24
    add r10, r10, #1
    mov r6, r4, asr #24
    ldrsh r0, [r9, #24]
    bl native_fn_02044cdc
    cmp r0, r4, asr #24
    bge ov000_021f6e84_Le4
ov000_021f6e84_L124:
    ldr r0, [sp]
    bl native_fn_021f70a4
    add r0, r8, r0
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    ldrb r1, [r9, #0x32]
    add r2, r8, #2
    mov r2, r2, lsl #24
    add r0, r1, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #7
    mov r2, r2, asr #24
    bl native_fn_021f7050
    ldrb r0, [r9, #0x30]
    cmp r0, #100
    bne ov000_021f6e84_L178
    mov r2, r8
    mov r0, #12
    mov r1, #23
    bl native_fn_021f7050
ov000_021f6e84_L178:
    ldr r0, [sp]
    cmp r0, #1
    addeq r0, r8, #2
    moveq r0, r0, lsl #24
    moveq r8, r0, asr #24
    ldr r0, [sp, #0x4]
    add r1, r8, #5
    add r2, r0, r6
    add r0, r5, #1
    mov r3, r0, lsl #24
    ldr r0, [sp, #0x8]
    mov r1, r1, lsl #24
    mov r2, r2, lsl #24
    cmp r0, r3, asr #24
    mov r0, r2, asr #24
    mov r8, r1, asr #24
    str r0, [sp, #0x4]
    mov r5, r3, asr #24
    bgt ov000_021f6e84_L8c
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
