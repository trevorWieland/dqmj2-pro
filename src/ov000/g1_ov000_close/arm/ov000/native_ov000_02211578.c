/* ov000 row 0x02211578: 84 bytes.
 *
 * What it does: 20 instructions; 3 call(s) to 0x022115c0, 0x02040838, 0x0204106c; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> constant 0x02240fbc (image word 0x02240fbc)
 *   branch +0x14 -> +0x48
 *   branch +0x30 -> +0x48
 *   test +0x10 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211578; the literal pool and
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

extern void native_fn_02040838(void);
extern void native_fn_0204106c(void);


asm u32 native_ov000_02211578 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrsh r0, [r5]
    mov r4, #0
    cmp r0, #0
    ble ov000_02211578_L48
    ldr r1, =0x02240fbc
    mov r2, #16
    bl native_fn_02040838
    mov r1, r0
    ldrb r0, [r1, #0x39]
    cmp r0, #0
    beq ov000_02211578_L48
    add r0, r5, #20
    mov r2, r4
    bl native_fn_0204106c
    cmp r0, #0
    movne r4, #1
ov000_02211578_L48:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
