/* ov006 row 0x021ecc84: 162 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x08 -> +0x12
 *   branch +0x24 -> +0x30
 *   branch +0x34 -> +0x40
 *   branch +0x48 -> +0x54
 *   branch +0x5c -> +0x62
 *   branch +0x6e -> +0x7c
 *   branch +0x88 -> +0x96
 *   test +0x06 cmp r6, #0x2
 *   test +0x22 cmp r0, #0x0
 *   test +0x32 cmp r0, #0x7
 *   test +0x46 cmp r0, #0x0
 *   test +0x5a cmp r0, #0x0
 *   test +0x6c cmp r0, r1
 *   test +0x86 cmp r0, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ecc84; the literal pool and
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

extern void native_fn_021ece60(void);
extern void native_fn_021edcb8(void);
extern void native_fn_021edc90(void);
extern void native_fn_021ec6e0(void);


asm u32 native_ov006_021ecc84 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r6, r0, #0x0
    add r5, r2, #0x0
    cmp r6, #0x2
    beq ov006_021ecc84_L12
    ldr r1, [r5, #0]
    add r1, r1, #0x1
    str r1, [r5, #0]
    pop {r4, r5, r6, pc}
ov006_021ecc84_L12:
    add r4, r1, #0x0
    add r3, #0x10
    add r1, #0xc
    add r0, r3, #0x0
    add r1, #0x10
    add r4, #0x24
    bl native_fn_021ece60
    cmp r0, #0x0
    bge ov006_021ecc84_L30
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r4, r5, r6, pc}
ov006_021ecc84_L30:
    ldrb r0, [r4, #0]
    cmp r0, #0x7
    beq ov006_021ecc84_L40
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r4, r5, r6, pc}
ov006_021ecc84_L40:
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    cmp r0, #0x0
    bne ov006_021ecc84_L54
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r4, r5, r6, pc}
ov006_021ecc84_L54:
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    cmp r0, #0x0
    bne ov006_021ecc84_L62
    mov r0, #0x64
    pop {r4, r5, r6, pc}
ov006_021ecc84_L62:
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x1
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecc84_L7c
    mov r0, #0x14
    bl native_fn_021ec6e0
    mov r0, #0x0
    mvn r0, r0
    pop {r4, r5, r6, pc}
ov006_021ecc84_L7c:
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x2
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecc84_L96
    mov r0, #0x15
    bl native_fn_021ec6e0
    mov r0, #0x0
    mvn r0, r0
    pop {r4, r5, r6, pc}
ov006_021ecc84_L96:
    mov r0, #0x18
    bl native_fn_021ec6e0
    mov r0, #0x0
    mvn r0, r0
    pop {r4, r5, r6, pc}
}
