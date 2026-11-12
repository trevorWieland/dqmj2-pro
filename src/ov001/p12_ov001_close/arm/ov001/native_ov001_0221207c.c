/* ov001 row 0x0221207c: 200 bytes.
 *
 * What it does: 47 instructions; 5 call(s) to 0x0205f98c, 0x02048a60, 0x02048a94, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (47 instructions, 5 calls, 1 branch, 5 back edges, 3 literal slots).
 *
 *   pool +0xbc -> constant 0x0223e124 (image word 0x0223e124)
 *   pool +0xc0 -> constant 0x0223e128 (image word 0x0223e128)
 *   pool +0xc4 -> constant 0x0223e130 (image word 0x0223e130)
 *   back edge +0xb4 -> +0x8c
 *   test +0x58 cmp r0, #4
 *   test +0xa0 cmp r1, #0
 *   test +0xb0 cmp r0, #8
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221207c; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov001_0221207c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldr r0, [r4, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldrsh r1, [r4, #20]
    ldrsh r2, [r4, #22]
    mov r5, r0
    bl native_fn_02048a60
    ldr r1, [r5, #0x7c]
    mov r0, r5
    bic r1, r1, #2
    str r1, [r5, #0x7c]
    ldrb r1, [r4, #0x20]
    bl native_fn_02048a94
    ldrb r1, [r4, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    mov r1, #0
    str r1, [r5, #0x84]
    ldr r0, [r4]
    ldr r2, =0x0223e124
    cmp r0, #4
    streqh r1, [r4, #38]
    movne r0, #30
    strneh r0, [r4, #38]
    ldr r1, =0x0223e128
    mov r0, #0
    ldr r3, [r1]
    add r3, r3, #1
    str r3, [r1]
    ldr r3, [r4, #0x2c]
    ldr r1, =0x0223e130
    ldrb r5, [r2, r3]
    add r3, r1, r3, lsl #5
ov001_0221207c_L8c:
    add r1, r0, r5
    mov r2, r1, lsr #31
    rsb r1, r2, r1, lsl #29
    add r2, r2, r1, ror #29
    ldr r1, [r3, r2, lsl #2]
    cmp r1, #0
    streq r4, [r3, r2, lsl #2]
    ldmeqia sp!, {r3, r4, r5, pc}
    add r0, r0, #1
    cmp r0, #8
    blt ov001_0221207c_L8c
    ldmia sp!, {r3, r4, r5, pc}
}
