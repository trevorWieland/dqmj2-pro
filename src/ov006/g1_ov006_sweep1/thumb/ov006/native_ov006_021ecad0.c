/* ov006 row 0x021ecad0: 220 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd4 -> constant 0x02219b8c (image word 0x02219b8c)
 *   pool +0xd8 -> constant 0x02219b4c (image word 0x02219b4c)
 *   branch +0x08 -> +0x12
 *   branch +0x26 -> +0x32
 *   branch +0x3a -> +0x46
 *   branch +0x4a -> +0x84
 *   branch +0x58 -> +0x62
 *   branch +0x60 -> +0x7e
 *   branch +0x6e -> +0x78
 *   branch +0x76 -> +0x7e
 *   branch +0x86 -> +0x92
 *   branch +0x9c -> +0xbc
 *   branch +0xa4 -> +0xb2
 *   test +0x06 cmp r6, #0x0
 *   test +0x24 cmp r0, #0x0
 *   test +0x38 cmp r0, #0x0
 *   test +0x48 cmp r0, #0x7
 *   test +0x56 cmp r0, r1
 *   test +0x6c cmp r0, r1
 *   test +0x84 cmp r0, #0x1
 *   test +0x9a cmp r0, #0x0
 *   test +0xa2 cmp r0, r1
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ecad0; the literal pool and
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
extern void native_fn_021eceac(void);
extern void native_fn_021ed2d8(void);


asm u32 native_ov006_021ecad0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r6, r0, #0x0
    add r5, r2, #0x0
    cmp r6, #0x0
    beq ov006_021ecad0_L12
    ldr r1, [r5, #0]
    add r1, r1, #0x1
    str r1, [r5, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_L12:
    add r7, r1, #0x0
    add r7, #0xc
    add r4, r1, #0x0
    add r1, r7, #0x0
    add r0, r3, #0x0
    add r1, #0x10
    add r4, #0x24
    bl native_fn_021ece60
    cmp r0, #0x0
    bge ov006_021ecad0_L32
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_L32:
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    cmp r0, #0x0
    bne ov006_021ecad0_L46
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_L46:
    ldrb r0, [r4, #0]
    cmp r0, #0x7
    bne ov006_021ecad0_L84
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x1
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecad0_L62
    mov r0, #0x14
    bl native_fn_021ec6e0
    b ov006_021ecad0_L7e
ov006_021ecad0_L62:
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x2
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecad0_L78
    mov r0, #0x15
    bl native_fn_021ec6e0
    b ov006_021ecad0_L7e
ov006_021ecad0_L78:
    mov r0, #0x18
    bl native_fn_021ec6e0
ov006_021ecad0_L7e:
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_L84:
    cmp r0, #0x1
    beq ov006_021ecad0_L92
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_L92:
    ldr r1, =0x02219b8c
    add r0, r4, #0x4
    bl native_fn_021eceac
    cmp r0, #0x0
    bge ov006_021ecad0_Lbc
    mov r1, #0x1
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecad0_Lb2
    mov r0, #0x16
    bl native_fn_021ec6e0
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_Lb2:
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecad0_Lbc:
    ldrh r0, [r7, #0xc]
    bl native_fn_021edcb8
    bl native_fn_021ed2d8
    ldr r1, =0x02219b4c
    str r0, [r1, #0]
    mov r0, #0x0
    str r0, [r5, #0]
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
