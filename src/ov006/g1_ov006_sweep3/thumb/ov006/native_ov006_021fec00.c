/* ov006 row 0x021fec00: 68 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x021fec44, 0x021feb34, 0x021feb34, +1 more; loops (back edge at +0x28); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3c -> constant 0x0221c144 (image word 0x0221c144)
 *   pool +0x40 -> constant 0x00001e5c (image word 0x00001e5c)
 *   branch +0x06 -> +0x38
 *   branch +0x12 -> +0x38
 *   branch +0x18 -> +0x38
 *   branch +0x1e -> +0x2e
 *   branch +0x22 -> +0x34
 *   test +0x04 cmp r1, #0x0
 *   test +0x10 cmp r1, #0x0
 *   test +0x16 cmp r1, #0x26
 *   test +0x1c cmp r1, #0x4
 *   test +0x20 cmp r1, #0x5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fec00; the literal pool and
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

extern void native_fn_021fec44(void);
extern void native_fn_021feb34(void);
extern void native_fn_02008430(void);


asm u32 native_ov006_021fec00 (register u32 a0)
{
    push {r3, lr}
    ldrh r1, [r0, #0x2]
    cmp r1, #0x0
    bne ov006_021fec00_L38
    ldr r1, =0x0221c144
    ldr r2, [r1, #0]
    ldr r1, =0x00001e5c
    ldrb r1, [r2, r1]
    cmp r1, #0x0
    bne ov006_021fec00_L38
    ldrh r1, [r0, #0]
    cmp r1, #0x26
    bne ov006_021fec00_L38
    ldrh r1, [r0, #0x8]
    cmp r1, #0x4
    beq ov006_021fec00_L2e
    cmp r1, #0x5
    bne ov006_021fec00_L34
    bl native_fn_021fec44
    bl native_fn_021feb34
    pop {r3, pc}
ov006_021fec00_L2e:
    bl native_fn_021feb34
    pop {r3, pc}
ov006_021fec00_L34:
    blx native_fn_02008430
ov006_021fec00_L38:
    pop {r3, pc}
    mov r8, r8
}
