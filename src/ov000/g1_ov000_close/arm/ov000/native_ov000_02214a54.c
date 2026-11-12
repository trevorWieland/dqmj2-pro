/* ov000 row 0x02214a54: 120 bytes.
 *
 * What it does: 28 instructions; 6 call(s) to 0x02040424, 0x0205c098, 0x021df3d0, +3 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> native_data_0222f8a0 (image word 0x0222f8a0)
 *   pool +0x74 -> native_data_0222f8ac (image word 0x0222f8ac)
 *   branch +0x20 -> +0x34
 *   branch +0x28 -> +0x60
 *   branch +0x30 -> +0x68
 *   branch +0x5c -> +0x68
 *   test +0x1c cmp r0, #2
 *   test +0x24 cmp r0, #3
 *   test +0x2c cmp r0, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214a54; the literal pool and
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

extern void native_fn_02040424(void);
extern void native_fn_0205c098(void);
extern void native_fn_021df3d0(void);
extern void native_fn_0205c080(void);
extern u8 native_data_0222f8a0[];
extern void native_fn_0203d294(void);
extern u8 native_data_0222f8ac[];


asm u32 native_ov000_02214a54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mvn r5, #0
    bl native_fn_02040424
    mov r4, r0
    bl native_fn_0205c098
    mov r0, r4
    bl native_fn_021df3d0
    cmp r0, #2
    beq ov000_02214a54_L34
    cmp r0, #3
    beq ov000_02214a54_L60
    cmp r0, #4
    b ov000_02214a54_L68
ov000_02214a54_L34:
    mov r0, r4
    bl native_fn_0205c080
    ldr r0, =native_data_0222f8a0
    sub r4, r4, #5
    ldrb r0, [r0, r4]
    bl native_fn_0203d294
    ldr r2, =native_data_0222f8ac
    mov r1, r0, lsl #1
    add r0, r2, r4, lsl #3
    ldrsh r5, [r1, r0]
    b ov000_02214a54_L68
ov000_02214a54_L60:
    mov r0, r4
    bl native_fn_0205c080
ov000_02214a54_L68:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
