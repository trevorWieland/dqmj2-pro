/* ov006 row 0x021ff468: 112 bytes.
 *
 * What it does: 49 instructions; 8 call(s) to 0x02008be0, 0x021ff484, 0x020a5300, +5 more; loops (back edge at +0x0e); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> constant 0x0221c148 (image word 0x0221c148)
 *   back edge +0x2a -> +0x1c
 *   back edge +0x58 -> +0x40
 *   back edge +0x66 -> +0x5c
 *   test +0x28 cmp r4, #0x3
 *   test +0x56 cmp r5, #0x2
 *   test +0x64 cmp r4, #0x4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff468; the literal pool and
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

extern void native_fn_02008be0(void);
extern void native_fn_020a5300(void);
extern void native_fn_020a4dec(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021ff4d8(void);


asm u32 native_ov006_021ff468 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    ldr r1, =0x0221c148
    mov r2, #0x1
    ldr r1, [r1, #0]
    mov r0, #0x0
    lsl r2, r2, #0xa
    blx native_fn_02008be0
    mov r4, #0x0
    mov r3, #0xff
    ldr r2, =0x0221c148
    add r5, r4, #0x0
    add r1, r3, #0x1
ov006_021ff468_L1c:
    ldr r0, [r2, #0]
    add r4, r4, #0x1
    add r0, r0, r5
    add r0, #0xe7
    add r5, r5, r1
    strb r3, [r0, #0]
    cmp r4, #0x3
    blt ov006_021ff468_L1c
    add r0, sp, #0x0
    bl native_fn_020a5300
    add r0, sp, #0x0
    bl native_fn_020a4dec
    mov r5, #0x0
    ldr r7, =0x0221c148
    add r6, r0, #0x0
    add r4, r5, #0x0
ov006_021ff468_L40:
    ldr r1, [r7, #0]
    add r0, r6, #0x0
    add r1, r1, r4
    add r1, #0xf0
    mov r2, #0xe
    blx native_fn_02008e0c
    mov r0, #0x1
    lsl r0, r0, #0x8
    add r5, r5, #0x1
    add r4, r4, r0
    cmp r5, #0x2
    blt ov006_021ff468_L40
    mov r4, #0x0
ov006_021ff468_L5c:
    add r0, r4, #0x0
    bl native_fn_021ff4d8
    add r4, r4, #0x1
    cmp r4, #0x4
    blt ov006_021ff468_L5c
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
}
