/* ov000 row 0x021e889c: 148 bytes.
 *
 * What it does: 36 instructions; 8 call(s) to 0x021e03f4, 0x020430b4, 0x021e88fc, +5 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x90 -> constant 0x0223526c (image word 0x0223526c)
 *   branch +0x1c -> +0x78
 *   branch +0x2c -> +0x74
 *   branch +0x4c -> +0x60
 *   back edge +0x5c -> +0x38
 *   back edge +0x84 -> +0x14
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x58 cmp r9, #5
 *   test +0x7c cmp r4, #8
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e889c; the literal pool and
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

extern void native_fn_021e03f4(void);
extern void native_fn_020430b4(void);
extern void native_fn_021e044c(void);
extern void native_fn_021e0420(void);


asm u32 native_ov000_021e889c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r4, #0
    ldr r5, =0x0223526c
    mov r8, r4
    mov r7, r4
ov000_021e889c_L14:
    ldrb r0, [r5, #0x274]
    cmp r0, #0
    beq ov000_021e889c_L78
    mov r0, r5
    bl native_fn_021e03f4
    cmp r0, #0
    beq ov000_021e889c_L74
    mov r9, r8
    add r6, r5, #256
ov000_021e889c_L38:
    ldrsh r0, [r6, #106]
    bl native_fn_020430b4
    add r0, r0, r9, lsl #1
    ldrsh r0, [r0, #4]
    cmp r0, #0
    ble ov000_021e889c_L60
    bl native_fn_021e044c
    add r9, r9, #1
    cmp r9, #5
    blt ov000_021e889c_L38
ov000_021e889c_L60:
    add r0, r5, #256
    ldrsh r0, [r0, #106]
    bl native_fn_020430b4
    ldrsh r0, [r0, #2]
    bl native_fn_021e0420
ov000_021e889c_L74:
    strb r7, [r5, #0x274]
ov000_021e889c_L78:
    add r4, r4, #1
    cmp r4, #8
    add r5, r5, #716
    blt ov000_021e889c_L14
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
