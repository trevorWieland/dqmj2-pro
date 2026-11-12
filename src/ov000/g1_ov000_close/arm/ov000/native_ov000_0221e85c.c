/* ov000 row 0x0221e85c: 108 bytes.
 *
 * What it does: 27 instructions; 5 call(s) to 0x02221344, 0x02221358, 0x02062ecc, +2 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x60 -> +0x20
 *   test +0x3c cmp r8, r0
 *   test +0x54 cmp r8, r0
 *   test +0x5c cmp r6, #5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e85c; the literal pool and
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

extern void native_fn_02221344(void);
extern void native_fn_02221358(void);
extern void native_fn_02062ecc(void);


asm u32 native_ov000_0221e85c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    bl native_fn_02221344
    mov r4, r0
    bl native_fn_02221358
    mov r7, #0
    mov r5, r0
    mov r6, r7
ov000_0221e85c_L20:
    mov r1, r6, lsl #24
    mov r0, r4
    mov r1, r1, asr #24
    bl native_fn_02062ecc
    ldrb r0, [r0]
    mov r1, r6, lsl #24
    mov r1, r1, asr #24
    cmp r8, r0
    mov r0, r5
    addeq r7, r7, #1
    bl native_fn_02062ecc
    ldrb r0, [r0]
    add r6, r6, #1
    cmp r8, r0
    addeq r7, r7, #2
    cmp r6, #5
    blt ov000_0221e85c_L20
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
