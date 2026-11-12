/* ov000 row 0x021e8a14: 268 bytes.
 *
 * What it does: 65 instructions; 3 call(s) to 0x0202818c, 0x02028158, 0x021e8a38; loops (back edge at +0xa8); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x0223526c (image word 0x0223526c)
 *   pool +0x108 -> native_data_0222edb8 (image word 0x0222edb8)
 *   branch +0x34 -> +0xec
 *   branch +0x9c -> +0xec
 *   branch +0xc0 -> +0xec
 *   branch +0xd0 -> +0xe4
 *   branch +0xe8 -> +0xfc
 *   back edge +0xf8 -> +0x24
 *   test +0x28 cmp r0, #0
 *   test +0x30 cmpne r0, #0
 *   test +0xbc cmp r0, #245760
 *   test +0xc8 cmp r6, #0
 *   test +0xf0 cmp r4, #8
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8a14; the literal pool and
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

extern void native_fn_0202818c(void);
extern void native_fn_02028158(void);
extern u8 native_data_0222edb8[];


asm u32 native_ov000_021e8a14 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r11, #0
    ldr r5, =0x0223526c
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r4, r11
    mov r10, r11
    mov r9, #2048
ov000_021e8a14_L24:
    ldrb r0, [r5, #0x274]
    cmp r0, #0
    ldrneb r0, [r5, #0x1e2]
    cmpne r0, #0
    beq ov000_021e8a14_Lec
    ldr r2, [r5, #0x74]
    ldr r1, [r8, #0x4]
    ldr r0, [r5, #0x29c]
    sub r3, r2, r1
    smull r2, r1, r3, r3
    ldr r12, [r5, #0x70]
    ldr r3, [r8]
    add r0, r0, r0, lsl #1
    sub r3, r12, r3
    mov r12, r0, asr #1
    smull r0, r14, r12, r12
    adds r0, r0, r9
    smlal r2, r1, r3, r3
    ldr r12, [r5, #0x78]
    ldr r3, [r8, #0x8]
    adc lr, lr, r10
    sub r3, r12, r3
    smlal r2, r1, r3, r3
    mov r2, r2, lsr #12
    mov r0, r0, lsr #12
    orr r0, r0, lr, lsl #20
    orr r2, r2, r1, lsl #20
    mov r3, r0, asr #31
    subs r0, r2, r0
    rscs r0, r3, r1, asr #12
    bge ov000_021e8a14_Lec
    mov r0, r8
    add r1, r5, #112
    bl native_fn_0202818c
    sub r0, r7, r0
    bl native_fn_02028158
    movs r7, r0
    rsbmi r0, r7, #0
    cmp r0, #245760
    bge ov000_021e8a14_Lec
    ldr r0, =native_data_0222edb8
    cmp r6, #0
    strb r4, [r0]
    beq ov000_021e8a14_Le4
    ldr r1, =0x0223526c
    mov r0, #716
    mla r0, r4, r0, r1
    str r0, [r6]
ov000_021e8a14_Le4:
    mov r11, #1
    b ov000_021e8a14_Lfc
ov000_021e8a14_Lec:
    add r4, r4, #1
    cmp r4, #8
    add r5, r5, #716
    blt ov000_021e8a14_L24
ov000_021e8a14_Lfc:
    mov r0, r11
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
