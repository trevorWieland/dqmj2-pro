/* ov000 row 0x0222728c: 284 bytes.
 *
 * What it does: 70 instructions; 16 call(s) to 0x01ffb340, 0x02227334, 0x02049ad0, +13 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x118 -> native_data_0222df84 (image word 0x0222df84)
 *   branch +0x2c -> +0xa8
 *   back edge +0xa4 -> +0x3c
 *   test +0x28 cmp r0, #0
 *   test +0xa0 cmp r0, r7, asr #24
 *   1 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222728c; the literal pool and
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

extern u8 native_data_0222df84[];
extern void native_fn_01ffb340(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_01ffb334(void);
extern void native_fn_0204a574(void);
extern void native_fn_0222390c(void);
extern void native_fn_02049604(void);


asm u32 native_ov000_0222728c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #20
    ldr r0, =native_data_0222df84
    mov r8, #0
    ldrh r1, [r0, #2]
    ldrh r0, [r0]
    strh r1, [sp, #18]
    strh r0, [sp, #16]
    bl native_fn_01ffb340
    ldrh r0, [r0, #12]
    cmp r0, #0
    ble ov000_0222728c_La8
    mov r6, #1
    add r5, sp, #16
    mov r4, #16
ov000_0222728c_L3c:
    add r9, r8, #5
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    bl native_fn_02049f4c
    bl native_fn_01ffb334
    mov r7, r0
    bl native_fn_01ffb334
    ldrsh r2, [r0, #2]
    mov r1, r9, lsl #24
    mov r0, r1, asr #24
    add r2, r8, r2
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    stmia sp, {r2, r6}
    str r6, [sp, #0x8]
    ldrb r3, [r7]
    mov r1, r5
    mov r2, r4
    bl native_fn_0204a574
    add r0, r8, #1
    mov r7, r0, lsl #24
    mov r8, r7, asr #24
    bl native_fn_01ffb340
    ldrh r0, [r0, #12]
    cmp r0, r7, asr #24
    bgt ov000_0222728c_L3c
ov000_0222728c_La8:
    bl native_fn_0222390c
    ldr r1, =native_data_0222df84
    mov r0, #0
    ldrh r2, [r1, #6]
    ldrh r1, [r1, #4]
    strh r2, [sp, #14]
    strh r1, [sp, #12]
    bl native_fn_02049ad0
    bl native_fn_02049f4c
    bl native_fn_01ffb334
    mov r4, r0
    bl native_fn_01ffb334
    ldrh r2, [r0, #6]
    mov r1, #1
    mov r0, #0
    str r2, [sp]
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    ldrsh r3, [r4, #4]
    add r1, sp, #12
    mov r2, #16
    and r3, r3, #255
    bl native_fn_0204a574
    bl native_fn_01ffb340
    mov r1, #0
    bl native_fn_02049604
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
