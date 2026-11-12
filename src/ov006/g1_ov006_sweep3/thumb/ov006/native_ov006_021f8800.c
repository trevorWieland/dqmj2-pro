/* ov006 row 0x021f8800: 104 bytes.
 *
 * What it does: 44 instructions; 11 call(s) to 0x02002480, 0x0220383c, 0x021f8826, +8 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   branch +0x22 -> +0x26
 *   branch +0x2c -> +0x3e
 *   back edge +0x3c -> +0x2e
 *   branch +0x42 -> +0x54
 *   back edge +0x52 -> +0x44
 *   test +0x20 cmp r7, #0x5
 *   test +0x2a cmp r7, #0x0
 *   test +0x3a cmp r4, r7
 *   test +0x40 cmp r7, #0x0
 *   test +0x50 cmp r4, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8800; the literal pool and
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

extern void native_fn_02002480(void);
extern void native_fn_0220383c(void);
extern void native_fn_021f8868(void);
extern void native_fn_021f893c(void);
extern void native_fn_022038ac(void);
extern void native_fn_021f8998(void);


asm u32 native_ov006_021f8800 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0221c0d8
    mov r1, #0x1c
    ldrh r0, [r0, #0x2]
    blx native_fn_02002480
    add r5, r0, #0x0
    ldr r0, =0x0221c0d8
    ldr r1, [r0, #0x4]
    add r0, r1, #0x0
    add r0, #0x51
    ldrb r7, [r0, #0]
    ldr r0, [r1, #0xc]
    mov r1, #0x0
    bl native_fn_0220383c
    cmp r7, #0x5
    ble ov006_021f8800_L26
    mov r7, #0x5
ov006_021f8800_L26:
    mov r4, #0x0
    add r6, r5, #0x0
    cmp r7, #0x0
    ble ov006_021f8800_L3e
ov006_021f8800_L2e:
    add r0, r6, #0x0
    add r1, r4, #0x0
    bl native_fn_021f8868
    add r4, r4, #0x1
    add r6, r6, #0x1
    cmp r4, r7
    blt ov006_021f8800_L2e
ov006_021f8800_L3e:
    mov r4, #0x0
    cmp r7, #0x0
    ble ov006_021f8800_L54
ov006_021f8800_L44:
    add r0, r5, #0x0
    add r1, r4, #0x0
    bl native_fn_021f893c
    add r4, r4, #0x1
    add r5, r5, #0x1
    cmp r4, r7
    blt ov006_021f8800_L44
ov006_021f8800_L54:
    ldr r0, =0x0221c0d8
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0xc]
    bl native_fn_022038ac
    bl native_fn_021f8998
    pop {r3, r4, r5, r6, r7, pc}
}
