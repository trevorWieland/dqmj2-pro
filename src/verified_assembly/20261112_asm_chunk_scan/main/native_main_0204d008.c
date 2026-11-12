/* main row 0x0204d008: 592 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x24c -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x70 -> +0x8c
 *   branch +0x88 -> +0x9c
 *   branch +0xb0 -> +0xc8
 *   branch +0xc4 -> +0xd4
 *   branch +0xec -> +0x104
 *   branch +0x100 -> +0x110
 *   branch +0x128 -> +0x140
 *   branch +0x13c -> +0x14c
 *   branch +0x1ac -> +0x1e4
 *   branch +0x1b4 -> +0x1dc
 *   branch +0x1c8 -> +0x1e4
 *   branch +0x1d8 -> +0x1e4
 *   test +0x1b0 cmp r4, #1000
 *   test +0x1c4 cmp r0, #0
 *   21 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204d008; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020259b4(void);
extern void native_fn_020259e8(void);
extern void native_fn_0202537c(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_02209fd8(void);
extern void native_fn_020449d4(void);
extern void native_fn_021dfdc4(void);
extern void native_fn_021e7b08(void);
extern void native_fn_02210c8c(void);
extern void native_fn_02025a28(void);


asm u32 native_main_0204d008 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #36
    mov r10, r0
    ldr r0, [r10, #0x10]
    str r1, [sp, #0x14]
    bl native_fn_020259b4
    mov r4, r0
    ldr r0, [r10, #0x14]
    bl native_fn_020259b4
    str r0, [sp, #0x20]
    ldr r0, [r10, #0x28]
    ldr r6, [r10, #0x18]
    ldr r7, [r10, #0x1c]
    ldr r8, [r10, #0x20]
    ldr r9, [r10, #0x24]
    bl native_fn_020259b4
    str r0, [sp, #0x1c]
    ldr r0, [r10, #0x2c]
    bl native_fn_020259e8
    and r11, r0, #255
    ldr r0, [r10, #0x30]
    bl native_fn_020259e8
    and r5, r0, #255
    mov r0, r9
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r9
    bls main_0204d008_L8c
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    str r0, [sp, #0x18]
    b main_0204d008_L9c
main_0204d008_L8c:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
    str r0, [sp, #0x18]
main_0204d008_L9c:
    mov r0, r8
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r8
    bls main_0204d008_Lc8
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d008_Ld4
main_0204d008_Lc8:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d008_Ld4:
    mov r8, r0
    mov r0, r7
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r7
    bls main_0204d008_L104
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d008_L110
main_0204d008_L104:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d008_L110:
    mov r7, r0
    mov r0, r6
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r6
    bls main_0204d008_L140
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d008_L14c
main_0204d008_L140:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d008_L14c:
    bl native_fn_020259b4
    mov r6, r0
    mov r0, r7
    bl native_fn_020259b4
    mov r7, r0
    mov r0, r8
    bl native_fn_020259b4
    mov r8, r0
    ldr r0, [sp, #0x18]
    bl native_fn_020259b4
    str r8, [sp]
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x1c]
    ldr r1, [sp, #0x20]
    str r0, [sp, #0x8]
    mov r1, r1, lsl #16
    str r11, [sp, #0xc]
    mov r2, r6
    mov r3, r7
    mov r0, r4
    mov r1, r1, asr #16
    str r5, [sp, #0x10]
    bl native_fn_02209fd8
    movs r5, r0
    bmi main_0204d008_L1e4
    cmp r4, #1000
    bne main_0204d008_L1dc
    ldr r0, [sp, #0x20]
    bl native_fn_020449d4
    ldrb r0, [r0, #0x61]
    cmp r0, #0
    ble main_0204d008_L1e4
    add r0, r0, #13
    bl native_fn_021dfdc4
    bl native_fn_021e7b08
    b main_0204d008_L1e4
main_0204d008_L1dc:
    mov r0, r4
    bl native_fn_02210c8c
main_0204d008_L1e4:
    mov r0, r5
    bl native_fn_02025a28
    str r0, [r10, #0x10]
    mov r5, #0
    str r5, [r10, #0x14]
    str r5, [r10, #0x18]
    str r5, [r10, #0x1c]
    str r5, [r10, #0x20]
    str r5, [r10, #0x24]
    str r5, [r10, #0x28]
    str r5, [r10, #0x2c]
    str r5, [r10, #0x30]
    ldrb r0, [r10, #0x3]
    mov r1, #268
    add r4, r10, #1136
    mul r3, r0, r1
    ldr r0, [sp, #0x14]
    ldr r2, [r4, r3]
    ldr r0, [r0, #0x4]
    add r0, r2, r0
    str r0, [r4, r3]
    ldrb r2, [r10, #0x3]
    mla r0, r2, r1, r10
    strb r5, [r0, #0x477]
    add sp, sp, #36
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
