/* ov006 row 0x021f2b64: 124 bytes.
 *
 * What it does: 47 instructions; 3 call(s) to 0x02203c08, 0x0220303c, 0x0220490c; no back edge; returns through pop {r4, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> constant 0x0221c058 (image word 0x0221c058)
 *   pool +0x68 -> native_data_0220b14c (image word 0x0220b14c)
 *   pool +0x6c -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x70 -> constant 0x00e50026 (image word 0x00e50026)
 *   pool +0x74 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x78 -> native_fn_021f2c0c+1 (image word 0x021f2c0d)
 *   branch +0x0a -> +0x60
 *   test +0x08 cmp r0, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2b64; the literal pool and
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

extern void native_fn_02203c08(void);
extern u8 native_data_0220b14c[];
extern void native_fn_0220303c(void);
extern void native_fn_021f2c0c(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f2b64 (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    ldr r0, =0x0221c058
    ldr r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f2b64_L60
    mov r0, #0xc
    mov r1, #0x4
    bl native_fn_02203c08
    ldr r1, =0x0221c058
    lsl r2, r4, #0x2
    str r0, [r1, #0]
    ldr r1, =native_data_0220b14c
    strb r4, [r0, #0x8]
    ldrb r1, [r1, r2]
    mov r0, #0x0
    bl native_fn_0220303c
    ldr r1, =0x0221c058
    ldr r2, [r1, #0]
    str r0, [r2, #0]
    ldr r0, [r1, #0]
    ldr r3, [r0, #0]
    ldr r0, =0xfe00ff00
    ldr r2, [r3, #0]
    and r2, r0
    ldr r0, =0x00e50026
    orr r0, r2
    str r0, [r3, #0]
    ldr r0, [r1, #0]
    mov r3, #0x78
    ldr r2, [r0, #0]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x2
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    mov r0, #0x0
    ldr r1, =native_fn_021f2c0c+1
    add r2, r0, #0x0
    bl native_fn_0220490c
    ldr r1, =0x0221c058
    ldr r1, [r1, #0]
    str r0, [r1, #0x4]
ov006_021f2b64_L60:
    pop {r4, pc}
    mov r8, r8
}
