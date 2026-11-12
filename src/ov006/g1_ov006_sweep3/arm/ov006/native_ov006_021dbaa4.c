/* ov006 row 0x021dbaa4: 196 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x02041800, 0x021d8328, 0x021d8328, +5 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> constant 0x0220f3b8 (image word 0x0220f3b8)
 *   branch +0x18 -> +0x28
 *   branch +0x24 -> +0x30
 *   branch +0x3c -> +0x58
 *   branch +0x44 -> +0xa4
 *   branch +0x54 -> +0xb8
 *   back edge +0x8c -> +0x70
 *   branch +0xa0 -> +0xb8
 *   test +0x08 cmp r0, #1
 *   test +0x14 cmpne r0, #0
 *   test +0x38 cmp r1, #1
 *   test +0x40 cmp r1, #2
 *   test +0x48 cmp r1, #3
 *   test +0x84 cmp r6, #10
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dbaa4; the literal pool and
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

extern void native_fn_02041800(void);
extern void native_fn_021d8328(void);
extern void native_fn_021d7de4(void);
extern void native_fn_021d7e34(void);
extern void native_fn_021d7ebc(void);
extern void native_fn_021db6a8(void);


asm u32 native_ov006_021dbaa4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_02041800
    cmp r0, #1
    ldrne r0, =0x0220f3b8
    ldrnesb r0, [r0]
    cmpne r0, #0
    bne ov006_021dbaa4_L28
    mov r0, #0
    bl native_fn_021d8328
    b ov006_021dbaa4_L30
ov006_021dbaa4_L28:
    mov r0, #1
    bl native_fn_021d8328
ov006_021dbaa4_L30:
    ldr r0, =0x0220f3b8
    ldr r1, [r0, #0x1c]
    cmp r1, #1
    beq ov006_021dbaa4_L58
    cmp r1, #2
    beq ov006_021dbaa4_La4
    cmp r1, #3
    moveq r1, #0
    streq r1, [r0, #0x1c]
    b ov006_021dbaa4_Lb8
ov006_021dbaa4_L58:
    bl native_fn_021d7de4
    bl native_fn_021d7e34
    mov r6, #0
    mov r7, #3
    mov r5, r6
    mov r4, #11
ov006_021dbaa4_L70:
    mov r0, r5
    mov r1, r4
    mov r2, r7
    bl native_fn_021d7ebc
    add r6, r6, #1
    cmp r6, #10
    add r7, r7, #2
    blt ov006_021dbaa4_L70
    ldr r0, =0x0220f3b8
    ldr r1, [r0, #0x1c]
    add r1, r1, #1
    str r1, [r0, #0x1c]
    b ov006_021dbaa4_Lb8
ov006_021dbaa4_La4:
    bl native_fn_021db6a8
    ldr r0, =0x0220f3b8
    ldr r1, [r0, #0x1c]
    add r1, r1, #1
    str r1, [r0, #0x1c]
ov006_021dbaa4_Lb8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
