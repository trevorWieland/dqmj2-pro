/* ov006 row 0x021ff344: 240 bytes.
 *
 * What it does: 105 instructions; 13 call(s) to 0x02008d78, 0x02008e0c, 0x02008e0c, +10 more; loops (back edge at +0x12); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xec -> constant 0x0221c148 (image word 0x0221c148)
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff344; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021ff174(void);


asm u32 native_ov006_021ff344 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r6, r0, #0x0
    ldr r0, =0x0221c148
    mov r4, #0x1
    ldr r5, [r0, #0]
    lsl r4, r4, #0xa
    add r0, r5, r4
    mov r1, #0x0
    mov r2, #0xef
    blx native_fn_02008d78
    add r1, r5, r4
    add r0, r6, #0x0
    add r1, #0xd1
    mov r2, #0x5
    blx native_fn_02008e0c
    add r1, r5, r4
    add r0, r6, #0x6
    add r1, #0xd6
    mov r2, #0x5
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0xc
    add r1, #0xdb
    mov r2, #0x5
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x12
    add r1, #0xe0
    mov r2, #0x5
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x18
    add r1, #0x60
    mov r2, #0x20
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x39
    add r1, #0x80
    mov r2, #0xd
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x47
    add r1, #0x90
    mov r2, #0xd
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x55
    add r1, #0xa0
    mov r2, #0xd
    blx native_fn_02008e0c
    add r0, r6, #0x0
    add r1, r5, r4
    add r0, #0x63
    add r1, #0xb0
    mov r2, #0xd
    blx native_fn_02008e0c
    add r6, #0x71
    add r1, r5, r4
    add r0, r6, #0x0
    add r1, #0x40
    mov r2, #0x20
    blx native_fn_02008e0c
    add r0, r5, r4
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0x3
    mov r2, #0x4
    bic r1, r0
    mov r0, #0x2
    orr r1, r0
    add r0, r5, r4
    add r0, #0xe6
    strb r1, [r0, #0]
    add r0, r5, r4
    add r0, #0xe6
    ldrb r1, [r0, #0]
    mov r0, #0xfc
    bic r1, r0
    add r0, r5, r4
    add r0, #0xe6
    strb r1, [r0, #0]
    add r0, r5, r4
    mov r1, #0x1
    add r0, #0xe7
    strb r1, [r0, #0]
    add r0, r5, r4
    add r0, #0xf0
    mov r1, #0x0
    blx native_fn_02008d78
    add r0, r5, r4
    mov r1, #0x1
    add r0, #0xf5
    strb r1, [r0, #0]
    add r0, r5, r4
    add r0, #0xf6
    strb r1, [r0, #0]
    bl native_fn_021ff174
    pop {r4, r5, r6, pc}
    mov r8, r8
}
