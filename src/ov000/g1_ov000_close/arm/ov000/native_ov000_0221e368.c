/* ov000 row 0x0221e368: 280 bytes.
 *
 * What it does: 68 instructions; 7 call(s) to 0x02221344, 0x02221358, 0x0221f3c0, +4 more; loops (back edge at +0x6c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x110 -> constant 0x02246318 (image word 0x02246318)
 *   pool +0x114 -> constant 0x02246348 (image word 0x02246348)
 *   branch +0x24 -> +0xd0
 *   branch +0x5c -> +0x80
 *   back edge +0x98 -> +0x38
 *   back edge +0xc8 -> +0xa4
 *   branch +0xcc -> +0x100
 *   back edge +0xfc -> +0xd8
 *   test +0x14 cmp r0, #8
 *   test +0x20 cmpeq r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x90 cmp r6, #6
 *   test +0xc4 cmp r4, #3
 *   test +0xf8 cmp r4, #6
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e368; the literal pool and
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
extern void native_fn_0221f3c0(void);
extern void native_fn_02048a60(void);


asm u32 native_ov000_0221e368 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r9, r0
    bl native_fn_02221344
    bl native_fn_02221358
    ldrsb r0, [r9, #16]
    cmp r0, #8
    ldreq r0, =0x02246318
    ldreqb r0, [r0]
    cmpeq r0, #0
    bne ov000_0221e368_Ld0
    ldr r5, =0x02246348
    mov r6, #0
    mov r8, #6
    mov r4, #8
ov000_0221e368_L38:
    ldr r0, [r9, #0x4]
    mov r7, r8, lsl #3
    add r0, r0, r6
    bl native_fn_0221f3c0
    cmp r0, #0
    add r0, r5, r6, lsl #2
    ldreq r1, [r0, #0x40]
    ldreq r0, [r1, #0x7c]
    biceq r0, r0, #2
    beq ov000_0221e368_L80
    ldr r0, [r0, #0x40]
    mov r1, r4
    mov r2, r7
    bl native_fn_02048a60
    add r0, r5, r6, lsl #2
    ldr r1, [r0, #0x40]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
ov000_0221e368_L80:
    str r0, [r1, #0x7c]
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #6
    add r8, r8, #2
    blt ov000_0221e368_L38
    ldr r3, =0x02246348
    mov r4, #0
ov000_0221e368_La4:
    add r0, r3, r4, lsl #2
    ldr r2, [r0, #0x34]
    add r0, r4, #1
    ldr r1, [r2, #0x7c]
    mov r0, r0, lsl #24
    bic r1, r1, #2
    mov r4, r0, asr #24
    str r1, [r2, #0x7c]
    cmp r4, #3
    blt ov000_0221e368_La4
    b ov000_0221e368_L100
ov000_0221e368_Ld0:
    ldr r3, =0x02246348
    mov r4, #0
ov000_0221e368_Ld8:
    add r0, r3, r4, lsl #2
    ldr r2, [r0, #0x40]
    add r0, r4, #1
    ldr r1, [r2, #0x7c]
    mov r0, r0, lsl #24
    bic r1, r1, #2
    mov r4, r0, asr #24
    str r1, [r2, #0x7c]
    cmp r4, #6
    blt ov000_0221e368_Ld8
ov000_0221e368_L100:
    ldrsb r1, [r9, #16]
    ldr r0, =0x02246318
    strb r1, [r0, #0x3]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
