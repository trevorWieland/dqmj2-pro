/* ov000 row 0x021d9864: 140 bytes.
 *
 * What it does: 34 instructions; 7 call(s) to 0x020298a8, 0x02029d84, 0x02029df0, +4 more; loops (back edge at +0x18); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x04000358 (image word 0x04000358)
 *   branch +0x10 -> +0x78
 *   test +0x0c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d9864; the literal pool and
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

extern void native_fn_020298a8(void);
extern void native_fn_02029d84(void);
extern void native_fn_02029df0(void);
extern void native_fn_02029e2c(void);
extern void native_fn_02029e68(void);
extern void native_fn_020046e0(void);


asm u32 native_ov000_021d9864 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrb r0, [r4, #0xd]
    cmp r0, #0
    beq ov000_021d9864_L78
    mov r0, #32768
    bl native_fn_020298a8
    mov r0, #1
    bl native_fn_02029d84
    ldrb r0, [r4, #0xc]
    bl native_fn_02029df0
    ldr r0, [r4, #0x8]
    bl native_fn_02029e2c
    ldr r0, [r4, #0x4]
    bl native_fn_02029e68
    ldrb r0, [r4, #0x3]
    ldrb r3, [r4]
    ldrb r1, [r4, #0x1]
    mov r2, r0, lsl #16
    ldrb r12, [r4, #0x2]
    orr r0, r3, r1, lsl #5
    ldr r1, =0x04000358
    orr r0, r0, r12, lsl #10
    mov r0, r0, lsl #16
    orr r2, r2, r0, lsr #16
    add r0, r4, #16
    str r2, [r1]
    bl native_fn_020046e0
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_021d9864_L78:
    mov r0, #0
    bl native_fn_02029d84
    mov r0, #0
    ldmia sp!, {r4, pc}
}
