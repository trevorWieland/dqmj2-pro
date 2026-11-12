/* ov000 row 0x022094e8: 108 bytes.
 *
 * What it does: 25 instructions; 2 call(s) to 0x02046120, 0x02046138; loops (back edge at +0x38); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x02238520 (image word 0x02238520)
 *   pool +0x68 -> constant 0x02238514 (image word 0x02238514)
 *   branch +0x18 -> +0x40
 *   test +0x04 cmp r0, #0
 *   test +0x14 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022094e8; the literal pool and
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

extern void native_fn_02046120(void);
extern void native_fn_02046138(void);


asm u32 native_ov000_022094e8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #0
    ldrlt r0, =0x02238520
    mov r1, #0
    ldrltsb r0, [r0, #8]
    cmp r0, #0
    bne ov000_022094e8_L40
    ldr r0, =0x02238514
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x44]
    ldr r2, [r0, #0x14]
    ldr r2, [r2, #0x4]
    blx r2
    mov r0, #0
    bl native_fn_02046120
    ldmia sp!, {r3, pc}
ov000_022094e8_L40:
    ldr r0, =0x02238514
    ldr r0, [r0]
    ldr r0, [r0, #0x44]
    ldr r2, [r0, #0x14]
    ldr r2, [r2, #0x4]
    blx r2
    mov r0, #0
    bl native_fn_02046138
    ldmia sp!, {r3, pc}
}
