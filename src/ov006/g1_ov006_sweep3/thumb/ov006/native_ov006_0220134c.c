/* ov006 row 0x0220134c: 72 bytes.
 *
 * What it does: 28 instructions; 4 call(s) to 0x02201270, 0x02014008, 0x022012c0, +1 more; loops (back edge at +0x04); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0x44 -> native_fn_02201394+1 (image word 0x02201395)
 *   branch +0x2c -> +0x3c
 *   test +0x2a cmp r0, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220134c; the literal pool and
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

extern void native_fn_02201270(void);
extern void native_fn_02201394(void);
extern void native_fn_02014008(void);
extern void native_fn_022012c0(void);


asm u32 native_ov006_0220134c (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x3
    bl native_fn_02201270
    ldr r0, =0x0221c164
    mov r2, #0x4f
    ldr r1, [r0, #0x4]
    lsl r2, r2, #0x6
    add r0, r1, r2
    sub r2, #0x14
    ldr r2, [r1, r2]
    blx r2
    ldr r2, =0x0221c164
    add r1, r0, #0x0
    ldr r3, [r2, #0x4]
    mov r2, #0x4f
    lsl r2, r2, #0x6
    ldr r0, =native_fn_02201394+1
    add r2, r3, r2
    blx native_fn_02014008
    cmp r0, #0x2
    beq ov006_0220134c_L3c
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    mov r0, #0x0
    pop {r3, pc}
ov006_0220134c_L3c:
    mov r0, #0x1
    pop {r3, pc}
}
