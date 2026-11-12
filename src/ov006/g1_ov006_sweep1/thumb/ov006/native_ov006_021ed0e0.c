/* ov006 row 0x021ed0e0: 184 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x22 -> +0x2c
 *   branch +0x24 -> +0x46
 *   branch +0x28 -> +0x3a
 *   branch +0x2a -> +0x52
 *   branch +0x2e -> +0x34
 *   branch +0x30 -> +0x3a
 *   branch +0x32 -> +0x52
 *   branch +0x36 -> +0x46
 *   branch +0x38 -> +0x52
 *   branch +0x3c -> +0x52
 *   branch +0x48 -> +0x52
 *   branch +0x54 -> +0x5e
 *   branch +0x56 -> +0x7a
 *   branch +0x5a -> +0x6c
 *   branch +0x5c -> +0x9a
 *   branch +0x60 -> +0x66
 *   branch +0x62 -> +0x6c
 *   branch +0x64 -> +0x9a
 *   branch +0x68 -> +0x7a
 *   branch +0x6a -> +0x9a
 *   branch +0x78 -> +0xa2
 *   branch +0x7c -> +0x8e
 *   branch +0x84 -> +0x8e
 *   branch +0x98 -> +0xa2
 *   branch +0xa6 -> +0xb2
 *   back edge +0xb0 -> +0x16
 *   test +0x20 cmp r0, #0x35
 *   test +0x26 cmp r0, #0x30
 *   test +0x2c cmp r0, #0x40
 *   test +0x34 cmp r0, #0x45
 *   test +0x3a cmp r5, #0x40
 *   test +0x46 cmp r5, #0x21
 *   test +0x52 cmp r0, #0x35
 *   test +0x58 cmp r0, #0x30
 *   test +0x5e cmp r0, #0x40
 *   test +0x66 cmp r0, #0x45
 *   test +0x7a cmp r5, #0x0
 *   test +0x82 cmp r0, #0x0
 *   test +0xa4 cmp r0, #0x0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed0e0; the literal pool and
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

extern void native_fn_021edcb8(void);
extern void native_fn_021edb9c(void);


asm u32 native_ov006_021ed0e0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    add r6, r1, #0x0
    add r4, r0, #0x6
    add r0, r6, #0x0
    str r0, [sp]
    add r0, #0x8
    add r7, r6, #0x0
    str r0, [sp]
    add r7, #0x30
    str r4, [sp, #0x4]
ov006_021ed0e0_L16:
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    add r5, r0, #0x0
    ldrb r0, [r4, #0]
    cmp r0, #0x35
    bgt ov006_021ed0e0_L2c
    bge ov006_021ed0e0_L46
    cmp r0, #0x30
    beq ov006_021ed0e0_L3a
    b ov006_021ed0e0_L52
ov006_021ed0e0_L2c:
    cmp r0, #0x40
    bgt ov006_021ed0e0_L34
    beq ov006_021ed0e0_L3a
    b ov006_021ed0e0_L52
ov006_021ed0e0_L34:
    cmp r0, #0x45
    beq ov006_021ed0e0_L46
    b ov006_021ed0e0_L52
ov006_021ed0e0_L3a:
    cmp r5, #0x40
    bls ov006_021ed0e0_L52
    mov r0, #0x0
    add sp, #0x8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed0e0_L46:
    cmp r5, #0x21
    bls ov006_021ed0e0_L52
    mov r0, #0x0
    add sp, #0x8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed0e0_L52:
    cmp r0, #0x35
    bgt ov006_021ed0e0_L5e
    bge ov006_021ed0e0_L7a
    cmp r0, #0x30
    beq ov006_021ed0e0_L6c
    b ov006_021ed0e0_L9a
ov006_021ed0e0_L5e:
    cmp r0, #0x40
    bgt ov006_021ed0e0_L66
    beq ov006_021ed0e0_L6c
    b ov006_021ed0e0_L9a
ov006_021ed0e0_L66:
    cmp r0, #0x45
    beq ov006_021ed0e0_L7a
    b ov006_021ed0e0_L9a
ov006_021ed0e0_L6c:
    add r0, r7, #0x0
    add r1, r4, #0x6
    add r2, r5, #0x0
    bl native_fn_021edb9c
    str r5, [r6, #0x4]
    b ov006_021ed0e0_La2
ov006_021ed0e0_L7a:
    cmp r5, #0x0
    beq ov006_021ed0e0_L8e
    add r0, r4, r5
    ldrb r0, [r0, #0x5]
    cmp r0, #0x0
    beq ov006_021ed0e0_L8e
    mov r0, #0x0
    add sp, #0x8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed0e0_L8e:
    ldr r0, [sp]
    add r1, r4, #0x6
    add r2, r5, #0x0
    bl native_fn_021edb9c
    b ov006_021ed0e0_La2
ov006_021ed0e0_L9a:
    mov r0, #0x0
    add sp, #0x8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed0e0_La2:
    ldrh r0, [r4, #0x4]
    cmp r0, #0x0
    beq ov006_021ed0e0_Lb2
    bl native_fn_021edcb8
    ldr r1, [sp, #0x4]
    add r4, r1, r0
    b ov006_021ed0e0_L16
ov006_021ed0e0_Lb2:
    mov r0, #0x0
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
