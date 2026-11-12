/* ov000 row 0x021f6ce0: 420 bytes.
 *
 * What it does: 102 instructions; 21 call(s) to 0x02061944, 0x0201d444, 0x0202a8e0, +18 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x198 -> native_data_0222f30c (image word 0x0222f30c)
 *   pool +0x19c -> native_data_0222f320 (image word 0x0222f320)
 *   pool +0x1a0 -> native_data_0222b96e (image word 0x0222b96e)
 *   branch +0x28 -> +0x70
 *   back edge +0xdc -> +0x98
 *   branch +0xf8 -> +0x104
 *   branch +0x130 -> +0x13c
 *   branch +0x148 -> +0x17c
 *   back edge +0x18c -> +0x11c
 *   test +0xd8 cmp r8, #12
 *   test +0xf4 cmp r1, #28
 *   test +0x12c cmp r1, #28
 *   test +0x13c cmp r0, #0
 *   test +0x144 cmpne r1, #0
 *   test +0x164 cmp r8, r7
 *   test +0x188 cmp r10, #3
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f6ce0; the literal pool and
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
extern u8 native_data_0222f30c[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern u8 native_data_0222f320[];
extern void native_fn_0205ff80(void);
extern u8 native_data_0222b96e[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02061de4(void);


asm u32 native_ov000_021f6ce0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    bl native_fn_02061944
    mov r4, r0
    ldr r1, =native_data_0222f30c
    add r0, sp, #6
    bl native_fn_0201d444
    add r0, sp, #6
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_021f6ce0_L70
    mov r2, #0
    add r0, sp, #6
    mov r1, #2
    strh r2, [sp, #4]
    bl native_fn_0203cc2c
    mov r2, r5
    mov r1, #0
    mov r5, r0
    bl native_fn_020481b8
    add r0, sp, #4
    mov r1, #0
    mov r2, #2
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r1, r5
    mov r0, #2
    bl native_fn_0202a498
ov000_021f6ce0_L70:
    ldr r1, =native_data_0222f320
    add r0, sp, #6
    bl native_fn_0201d444
    add r0, sp, #6
    bl native_fn_0205ff80
    mov r8, #0
    ldr r6, =native_data_0222b96e
    add r7, r4, #16
    mov r5, r8
    mov r9, #12
ov000_021f6ce0_L98:
    add r1, r8, #1
    ldr r2, [r4, #0x25c]
    mla r0, r1, r9, r7
    str r2, [sp]
    mov r1, r8, lsl #1
    add r2, r6, r8, lsl #1
    ldrsb r1, [r6, r1]
    ldrb r3, [r2, #0x1]
    mov r2, r5
    bl native_fn_02065730
    add r1, r8, #1
    ldr r2, [r4, #0x25c]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r4, #0x25c]
    cmp r8, #12
    blt ov000_021f6ce0_L98
    bl native_fn_0205ff9c
    bl native_fn_02062aa0
    add r1, r4, #512
    ldrsb r1, [r1, #105]
    mov r7, r0
    cmp r1, #28
    blt ov000_021f6ce0_L104
    bl native_fn_02062ad0
    mov r7, r0
ov000_021f6ce0_L104:
    mov r8, #0
    add r5, r4, #16
    mov r10, r8
    add r4, r4, #512
    mov r6, r8
    mov r11, #12
ov000_021f6ce0_L11c:
    mov r0, r8
    add r9, r10, #2
    bl native_fn_02062a50
    ldrsb r1, [r4, #105]
    cmp r1, #28
    blt ov000_021f6ce0_L13c
    mov r0, r8
    bl native_fn_02062a88
ov000_021f6ce0_L13c:
    cmp r0, #0
    ldrnesh r1, [r0, #24]
    cmpne r1, #0
    beq ov000_021f6ce0_L17c
    mla r0, r9, r11, r5
    mov r2, r10
    mov r3, #1
    str r6, [sp]
    bl native_fn_02061de4
    add r8, r8, #1
    cmp r8, r7
    addge sp, sp, #40
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r10, r0
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
ov000_021f6ce0_L17c:
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #3
    blt ov000_021f6ce0_L11c
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
