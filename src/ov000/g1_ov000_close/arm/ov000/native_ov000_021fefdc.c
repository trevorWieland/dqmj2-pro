/* ov000 row 0x021fefdc: 916 bytes.
 *
 * What it does: 226 instructions; 29 call(s) to 0x02062aa0, 0x02062ad0, 0x02216434, +26 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x388 -> constant 0x0223756c (image word 0x0223756c)
 *   pool +0x38c -> constant 0x02237564 (image word 0x02237564)
 *   pool +0x390 -> constant 0x0223765c (image word 0x0223765c)
 *   branch +0x38 -> +0x4c
 *   branch +0x44 -> +0x1fc
 *   branch +0x48 -> +0x334
 *   branch +0xd4 -> +0x1d0
 *   branch +0xe4 -> +0xf4
 *   branch +0xf0 -> +0xfc
 *   branch +0x12c -> +0x154
 *   back edge +0x1cc -> +0xe0
 *   branch +0x1f8 -> +0x334
 *   branch +0x21c -> +0x250
 *   back edge +0x24c -> +0x224
 *   branch +0x29c -> +0x334
 *   back edge +0x330 -> +0x2b4
 *   test +0x34 cmp r1, #1
 *   test +0x40 cmp r0, #3
 *   test +0xd0 cmp r0, #0
 *   test +0xe0 cmp r9, r7
 *   test +0x128 cmp r5, #0
 *   test +0x1c8 cmp r1, r0, asr #24
 *   test +0x210 cmp r1, #0
 *   test +0x248 cmp r1, r0, asr #24
 *   test +0x298 cmp r0, #0
 *   test +0x32c cmp r1, r0, asr #24
 *   test +0x33c cmp r0, #1
 *   1 block transfer(s), 28 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fefdc; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02216434(void);
extern void native_fn_0204a644(void);
extern void native_fn_02049008(void);
extern void native_fn_0221742c(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020602ec(void);
extern void native_fn_02065818(void);
extern void native_fn_0204a574(void);
extern void native_fn_02217f14(void);
extern void native_fn_0207b460(void);
extern void native_fn_02008be0(void);
extern void native_fn_021fef08(void);
extern void native_fn_02217dbc(void);
extern void native_fn_02217f78(void);
extern void ov000_display_context_02215698(void);
extern void native_fn_0205fb3c(void);


asm u32 native_ov000_021fefdc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #156
    str r0, [sp, #0xc]
    bl native_fn_02062aa0
    mov r7, r0
    bl native_fn_02062ad0
    bl native_fn_02216434
    mov r1, #0
    str r1, [sp, #0x10]
    str r1, [sp, #0x14]
    strh r1, [sp, #24]
    strh r1, [sp, #26]
    ldr r1, [sp, #0xc]
    cmp r1, #1
    beq ov000_021fefdc_L4c
    mov r0, r1
    cmp r0, #3
    beq ov000_021fefdc_L1fc
    b ov000_021fefdc_L334
ov000_021fefdc_L4c:
    ldr r1, [sp, #0x14]
    mov r2, #1
    strh r1, [sp, #24]
    ldrh r3, [r0, #2]
    add r1, sp, #24
    ldr r6, =0x0223756c
    str r3, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    ldrb r2, [r0]
    ldrb r3, [r0, #0x1]
    mov r0, #23
    bl native_fn_0204a644
    ldrsh r3, [sp, #24]
    mov r1, #5
    mov r2, r1
    add r3, r3, r0
    strh r3, [sp, #24]
    mov r4, #0
    mov r0, r6
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    mov r1, #1
    str r1, [sp]
    mov r0, r6
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    ldrh r2, [r6, #12]
    mov r9, r4
    sub r0, r2, #1
    cmp r0, #0
    ble ov000_021fefdc_L1d0
    ldr r11, =0x02237564
    mov r8, #5
ov000_021fefdc_Le0:
    cmp r9, r7
    bge ov000_021fefdc_Lf4
    mov r0, #7
    bl native_fn_0221742c
    b ov000_021fefdc_Lfc
ov000_021fefdc_Lf4:
    mov r0, #8
    bl native_fn_0221742c
ov000_021fefdc_Lfc:
    mov r10, r0
    add r0, r11, r9, lsl #2
    ldr r5, [r0, #0x1f0]
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r4, r0
    bl native_fn_02049f4c
    mov r0, #24
    strh r0, [sp, #24]
    cmp r5, #0
    beq ov000_021fefdc_L154
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r5, #24]
    ldrsh r3, [sp, #24]
    ldr r0, [r4]
    mov r2, r5
    bl native_fn_020602ec
ov000_021fefdc_L154:
    mov r2, r8, lsl #24
    mov r0, r10
    mov r1, #4
    mov r2, r2, asr #24
    bl native_fn_02065818
    mov r0, #8
    strh r0, [sp, #24]
    ldrb r1, [r5, #0x32]
    add r0, r9, #12
    mov r0, r0, lsl #24
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    mov r0, r0, asr #24
    add r1, sp, #24
    mov r2, #0
    mov r3, #1
    bl native_fn_0204a574
    ldrsh r2, [sp, #24]
    add r1, r9, #1
    add r8, r8, #2
    add r0, r2, r0
    strh r0, [sp, #24]
    mov r0, r1, lsl #24
    ldrh r2, [r6, #12]
    mov r9, r0, asr #24
    sub r1, r2, #1
    cmp r1, r0, asr #24
    bgt ov000_021fefdc_Le0
ov000_021fefdc_L1d0:
    add r0, r2, #4
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #5
    mov r2, #2
    mov r3, #34
    bl native_fn_02217f14
    str r0, [sp, #0x14]
    mov r0, #28
    str r0, [sp, #0x10]
    b ov000_021fefdc_L334
ov000_021fefdc_L1fc:
    ldr r6, =0x0223765c
    ldr r0, =0x02237564
    ldrh r1, [r6, #12]
    ldr r2, [r0, #0x8]
    ldr r7, [sp, #0x14]
    cmp r1, #0
    and r5, r2, #255
    ldr r10, [r0, #0x1e8]
    ble ov000_021fefdc_L250
    add r4, sp, #28
ov000_021fefdc_L224:
    ldrsh r0, [r10, #24]
    ldrb r1, [r10, #0x1a]
    mov r3, r4
    add r2, r10, #122
    bl native_fn_0207b460
    add r0, r7, #1
    mov r0, r0, lsl #24
    ldrh r1, [r6, #12]
    mov r7, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_021fefdc_L224
ov000_021fefdc_L250:
    mov r4, #4
    mov r0, r6
    mov r1, #5
    mov r2, #0
    mov r3, #1
    str r4, [sp]
    bl native_fn_02049008
    mov r0, #0
    add r1, sp, #92
    mov r2, #64
    strh r0, [sp, #24]
    strh r0, [sp, #26]
    bl native_fn_02008be0
    mov r0, r10
    mov r1, r5
    bl native_fn_021fef08
    ldrh r0, [r6, #12]
    mov r9, #0
    cmp r0, #0
    ble ov000_021fefdc_L334
    mov r8, #6
    add r11, sp, #28
    mov r7, #24
    mov r5, #1
    mov r4, r9
ov000_021fefdc_L2b4:
    ldrsh r0, [r10, #24]
    ldrb r1, [r10, #0x1a]
    add r2, r10, #122
    mov r3, r11
    bl native_fn_0207b460
    mov r0, r9, lsl #16
    strh r7, [sp, #24]
    mov r0, r0, lsr #16
    stmia sp, {r0, r5}
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    add r1, sp, #24
    mov r2, r4
    mov r3, r5
    str r4, [sp, #0x8]
    bl native_fn_0204a574
    add r0, r9, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0221742c
    mov r2, r8, lsl #24
    mov r1, #2
    mov r2, r2, asr #24
    bl native_fn_02065818
    add r0, r9, #1
    mov r0, r0, lsl #24
    ldrh r1, [r6, #12]
    add r8, r8, #2
    mov r9, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_021fefdc_L2b4
ov000_021fefdc_L334:
    bl native_fn_02217dbc
    ldr r0, [sp, #0xc]
    cmp r0, #1
    addne sp, sp, #156
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrh r0, [r6, #12]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x10]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    mov r1, r6
    mov r0, r0, asr #24
    bl native_fn_02217f78
    ldr r1, =0x02237564
    strb r0, [r1, #0x1ed]
    bl ov000_display_context_02215698
    add r0, r0, #16
    mov r1, #0
    bl native_fn_0205fb3c
    add sp, sp, #156
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
