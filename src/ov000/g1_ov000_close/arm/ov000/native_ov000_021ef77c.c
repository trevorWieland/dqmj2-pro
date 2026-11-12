/* ov000 row 0x021ef77c: 140 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x02049ad0, 0x02049f4c, 0x0204a04c, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x3c -> +0x6c
 *   test +0x38 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ef77c; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0204a04c(void);
extern void native_fn_0206dbdc(void);
extern void native_fn_02085270(void);


asm u32 native_ov000_021ef77c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_02049ad0
    ldr r1, [r0]
    ldr r4, [r1, #0x4]
    bl native_fn_02049f4c
    mov r0, r4
    mov r1, r7
    mov r2, r6
    mov r3, r5
    bl native_fn_0204a04c
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    beq ov000_021ef77c_L6c
    mov r0, r7
    mov r1, r6
    mov r2, r5
    bl native_fn_0206dbdc
    ldrb r1, [r4, #0x1e]
    ldrsh r2, [sp, #24]
    rsb r0, r0, r1, lsl #3
    add r0, r0, r0, lsr #31
    mov r0, r0, lsl #15
    add r0, r2, r0, lsr #16
    strh r0, [sp, #24]
ov000_021ef77c_L6c:
    ldrsh r1, [sp, #24]
    add r0, r4, #60
    mov r2, #0
    bl native_fn_02085270
    ldr r0, [r4, #0x18]
    orr r0, r0, #2
    str r0, [r4, #0x18]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
