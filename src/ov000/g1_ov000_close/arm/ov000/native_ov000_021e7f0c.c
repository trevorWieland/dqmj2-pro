/* ov000 row 0x021e7f0c: 272 bytes.
 *
 * What it does: 66 instructions; 3 call(s) to 0x021d8a50, 0x021d8c18, 0x021e7f34; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x108 -> constant 0x0223526c (image word 0x0223526c)
 *   pool +0x10c -> constant 0x00bd1000 (image word 0x00bd1000)
 *   branch +0x30 -> +0xf0
 *   branch +0x48 -> +0xf0
 *   branch +0x5c -> +0x9c
 *   branch +0xa8 -> +0xf0
 *   branch +0xb0 -> +0xf0
 *   branch +0xc0 -> +0xd0
 *   branch +0xcc -> +0xf0
 *   back edge +0xfc -> +0x28
 *   test +0x2c cmp r0, #0
 *   test +0x44 cmp r0, #3
 *   test +0x50 cmp r0, #0
 *   test +0xac cmp r0, #2
 *   test +0xbc cmp r0, #0
 *   test +0xc8 cmp r0, #1
 *   test +0xf4 cmp r4, #8
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e7f0c; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_021d8c18(void);


asm u32 native_ov000_021e7f0c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r0, #0
    mov r4, r1
    bl native_fn_021d8a50
    mov r1, #20
    mla r9, r10, r1, r4
    ldr r8, =0x0223526c
    mov r5, r0
    mov r4, #0
ov000_021e7f0c_L28:
    ldrb r0, [r8, #0x274]
    cmp r0, #0
    beq ov000_021e7f0c_Lf0
    ldrb r11, [r8, #0x1e2]
    mov r0, #0
    strb r0, [r8, #0x1e2]
    ldrb r0, [r8, #0x2a9]
    cmp r0, #3
    beq ov000_021e7f0c_Lf0
    ldrb r0, [r8, #0x1e4]
    cmp r0, #0
    movne r7, #0
    movne r6, r7
    bne ov000_021e7f0c_L9c
    ldr r2, [r5, #0x4]
    ldr r1, [r8, #0x74]
    ldr r7, [r5]
    sub r3, r2, r1
    smull r2, r1, r3, r3
    ldr r3, [r8, #0x70]
    ldr r6, [r5, #0x8]
    sub r3, r7, r3
    smlal r2, r1, r3, r3
    ldr r3, [r8, #0x78]
    sub r3, r6, r3
    smlal r2, r1, r3, r3
    mov r7, r2, lsr #12
    mov r6, r1, asr #12
    orr r7, r7, r1, lsl #20
ov000_021e7f0c_L9c:
    ldr r1, =0x00bd1000
    subs r1, r7, r1
    sbcs r1, r6, #0
    bge ov000_021e7f0c_Lf0
    cmp r0, #2
    beq ov000_021e7f0c_Lf0
    add r0, r8, #112
    bl native_fn_021d8c18
    cmp r0, #0
    bne ov000_021e7f0c_Ld0
    ldrb r0, [r8, #0x1e4]
    cmp r0, #1
    bne ov000_021e7f0c_Lf0
ov000_021e7f0c_Ld0:
    str r4, [r9]
    str r7, [r9, #0x8]
    str r6, [r9, #0xc]
    str r11, [r9, #0x10]
    mov r0, #0
    str r0, [r9, #0x4]
    add r9, r9, #20
    add r10, r10, #1
ov000_021e7f0c_Lf0:
    add r4, r4, #1
    cmp r4, #8
    add r8, r8, #716
    blt ov000_021e7f0c_L28
    mov r0, r10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
