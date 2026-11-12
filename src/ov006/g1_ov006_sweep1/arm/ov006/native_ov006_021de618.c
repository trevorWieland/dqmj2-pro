/* ov006 row 0x021de618: 328 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x138 -> native_data2_0220f594 (image word 0x0220f594)
 *   pool +0x13c -> native_data2_0220f654 (image word 0x0220f654)
 *   pool +0x140 -> constant 0x0220f738 (image word 0x0220f738)
 *   pool +0x144 -> constant 0x0220f69c (image word 0x0220f69c)
 *   branch +0x18 -> +0x84
 *   branch +0x2c -> +0x84
 *   branch +0x4c -> +0x84
 *   branch +0xc0 -> +0x11c
 *   branch +0xcc -> +0x11c
 *   branch +0xdc -> +0x11c
 *   branch +0xe4 -> +0x104
 *   branch +0xf0 -> +0x11c
 *   branch +0x100 -> +0x11c
 *   back edge +0x130 -> +0xa0
 *   test +0x14 cmp r1, #0
 *   test +0x28 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0xbc cmp r1, #255
 *   test +0xc8 cmp r1, #0
 *   test +0xd8 cmp r1, r3
 *   test +0xe0 cmp r5, #0
 *   test +0xec cmp r1, #0
 *   test +0x10c cmp r2, r1
 *   test +0x128 cmp r5, #2
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021de618; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021df140(void);
extern void native_fn_0205f9e4(void);
extern u8 native_data2_0220f594[];
extern u8 native_data2_0220f654[];
extern void native_fn_0205f98c(void);
extern void native_fn_02049ae4(void);
extern void native_fn_02048a60(void);


asm u32 native_ov006_021de618 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_021df140
    bl native_fn_0205f9e4
    ldr r0, =native_data2_0220f594
    ldrsb r1, [r0]
    cmp r1, #0
    ble ov006_021de618_L84
    sub r1, r1, #1
    strb r1, [r0]
    ldrsb r0, [r0]
    cmp r0, #0
    bne ov006_021de618_L84
    ldr r0, =native_data2_0220f654
    mov r1, #0
    ldr r0, [r0, #0x1c]
    bl native_fn_0205f98c
    mov r4, r0
    bl native_fn_02049ae4
    cmp r0, #0
    beq ov006_021de618_L84
    ldr r2, [r4, #0x7c]
    mov r1, #224
    orr r2, r2, #2
    str r2, [r4, #0x7c]
    ldr r2, [r0, #0x4]
    mov r0, r4
    ldrb r3, [r2, #0x33]
    ldrb r2, [r2, #0x35]
    add r2, r3, r2
    sub r2, r2, #3
    mov r2, r2, lsl #3
    add r2, r2, #4
    bl native_fn_02048a60
ov006_021de618_L84:
    ldr r0, =native_data2_0220f654
    bl native_fn_0205f9e4
    mov r5, #0
    ldr r6, =0x0220f738
    ldr r7, =0x0220f69c
    ldr r8, =native_data2_0220f594
    mov r4, r5
ov006_021de618_La0:
    ldr r0, [r7, #0x1c]
    mov r1, r4
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    ldrb r1, [r8, #0x1]
    cmp r1, #255
    beq ov006_021de618_L11c
    ldr r1, [r8, #0x40]
    cmp r1, #0
    bne ov006_021de618_L11c
    ldrh r3, [r6, #14]
    ldrh r1, [r6, #12]
    cmp r1, r3
    beq ov006_021de618_L11c
    cmp r5, #0
    bne ov006_021de618_L104
    ldr r1, [r6, #0x4]
    cmp r1, #0
    beq ov006_021de618_L11c
    ldr r1, [r0, #0x7c]
    orr r1, r1, #2
    str r1, [r0, #0x7c]
    b ov006_021de618_L11c
ov006_021de618_L104:
    ldr r2, [r6, #0x4]
    sub r1, r3, r1
    cmp r2, r1
    ldrlt r1, [r0, #0x7c]
    orrlt r1, r1, #2
    strlt r1, [r0, #0x7c]
ov006_021de618_L11c:
    mov r0, r7
    bl native_fn_0205f9e4
    add r5, r5, #1
    cmp r5, #2
    add r7, r7, #72
    blt ov006_021de618_La0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
