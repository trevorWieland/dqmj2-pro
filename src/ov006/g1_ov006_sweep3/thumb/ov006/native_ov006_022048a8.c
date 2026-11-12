/* ov006 row 0x022048a8: 100 bytes.
 *
 * What it does: 46 instructions; 4 call(s) to 0x02204904, 0x02203114, 0x02204994, +1 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x60 -> constant 0x0221c1e8 (image word 0x0221c1e8)
 *   branch +0x14 -> +0x5c
 *   branch +0x1c -> +0x32
 *   back edge +0x30 -> +0x1e
 *   branch +0x3a -> +0x5c
 *   branch +0x48 -> +0x5c
 *   back edge +0x5a -> +0x3e
 *   test +0x12 cmp r2, #0x0
 *   test +0x1a cmp r5, r1
 *   test +0x2e cmp r5, r1
 *   test +0x38 cmp r1, #0x0
 *   test +0x58 cmp r5, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022048a8; the literal pool and
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

extern void native_fn_02203114(void);
extern void native_fn_02204994(void);


asm u32 native_ov006_022048a8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r7, =0x0221c1e8
    add r6, r0, #0x0
    ldr r0, [r7, #0]
    lsl r4, r6, #0x6
    add r1, r0, r4
    add r2, r1, #0x0
    add r2, #0x38
    ldrb r2, [r2, #0]
    cmp r2, #0x0
    beq ov006_022048a8_L5c
    ldr r5, [r1, #0x10]
    add r1, #0x20
    cmp r5, r1
    beq ov006_022048a8_L32
ov006_022048a8_L1e:
    ldr r1, [r5, #0xc]
    ldr r2, [r5, #0x8]
    add r0, r5, #0x0
    blx r2
    ldr r0, [r7, #0]
    ldr r5, [r5, #0x4]
    add r1, r0, r4
    add r1, #0x20
    cmp r5, r1
    bne ov006_022048a8_L1e
ov006_022048a8_L32:
    add r1, r0, r4
    ldr r1, [r1, #0x34]
    mov r5, #0x0
    cmp r1, #0x0
    ble ov006_022048a8_L5c
    ldr r7, =0x0221c1e8
ov006_022048a8_L3e:
    add r0, r4, r0
    ldr r0, [r0, #0x4]
    bl native_fn_02203114
    add r1, r0, #0x0
    beq ov006_022048a8_L5c
    add r0, r6, #0x0
    bl native_fn_02204994
    ldr r0, [r7, #0]
    add r5, r5, #0x1
    add r1, r4, r0
    ldr r1, [r1, #0x34]
    cmp r5, r1
    blt ov006_022048a8_L3e
ov006_022048a8_L5c:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
