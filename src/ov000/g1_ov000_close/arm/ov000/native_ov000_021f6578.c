/* ov000 row 0x021f6578: 108 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x020622ec, 0x0202a498, 0x021f7160; loops (back edge at +0x1c); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> native_data_0222eef0 (image word 0x0222eef0)
 *   pool +0x64 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   pool +0x68 -> constant 0x0400000c (image word 0x0400000c)
 *   branch +0x2c -> +0x44
 *   test +0x28 cmp r1, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f6578; the literal pool and
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

extern u8 native_data_0222eef0[];
extern void native_fn_020622ec(void);
extern void native_fn_0202a498(void);
extern void native_fn_021f7160(void);


asm u32 native_ov000_021f6578 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r3, =native_data_0222eef0
    mov r12, #11
    mov r0, #6
    mov r1, #15
    mov r2, #0
    strb r12, [r3, #0x1]
    bl native_fn_020622ec
    ldr r0, =0x02236ee4
    ldr r1, [r0, #0x1c]
    cmp r1, #0
    beq ov000_021f6578_L44
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x02236ee4
    mov r1, #0
    str r1, [r0, #0x1c]
ov000_021f6578_L44:
    bl native_fn_021f7160
    ldr r1, =0x0400000c
    ldrh r0, [r1]
    and r0, r0, #67
    orr r0, r0, #528
    strh r0, [r1]
    ldmia sp!, {r3, pc}
}
