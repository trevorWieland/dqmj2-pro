/* ov000 row 0x021f3dac: 124 bytes.
 *
 * What it does: 31 instructions; 5 call(s) to 0x021f3cd0, 0x021f3d2c, 0x021f3d74, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x70
 *   branch +0x38 -> +0x6c
 *   branch +0x54 -> +0x6c
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3dac; the literal pool and
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

extern void native_fn_021f3cd0(void);
extern void native_fn_021f3d2c(void);
extern void native_fn_021f3d74(void);
extern void native_fn_021da5e4(void);
extern void native_fn_021f3d04(void);


asm u32 native_ov000_021f3dac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    mov r6, r1
    mov r4, #0
    bl native_fn_021f3cd0
    movs r5, r0
    beq ov000_021f3dac_L70
    mov r1, r6
    bl native_fn_021f3d2c
    mov r0, r5
    mov r1, r6
    bl native_fn_021f3d74
    ldrb r0, [r5, #0x274]
    cmp r0, #0
    bne ov000_021f3dac_L6c
    add r2, sp, #0
    add r0, r5, #112
    add r1, r5, #528
    mvn r3, #0
    bl native_fn_021da5e4
    cmp r0, #0
    beq ov000_021f3dac_L6c
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r5
    bl native_fn_021f3d04
ov000_021f3dac_L6c:
    add r4, r5, #112
ov000_021f3dac_L70:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
