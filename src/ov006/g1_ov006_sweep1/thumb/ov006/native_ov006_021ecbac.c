/* ov006 row 0x021ecbac: 216 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xcc -> native_data2_0221a20c (image word 0x0221a20c)
 *   pool +0xd0 -> constant 0x02219b8c (image word 0x02219b8c)
 *   pool +0xd4 -> constant 0x02219b4c (image word 0x02219b4c)
 *   branch +0x08 -> +0x12
 *   branch +0x28 -> +0x34
 *   branch +0x3c -> +0x48
 *   branch +0x4c -> +0x86
 *   branch +0x5a -> +0x64
 *   branch +0x62 -> +0x80
 *   branch +0x70 -> +0x7a
 *   branch +0x78 -> +0x80
 *   branch +0xaa -> +0xb6
 *   branch +0xbe -> +0xc4
 *   test +0x06 cmp r6, #0x1
 *   test +0x26 cmp r0, #0x0
 *   test +0x3a cmp r0, #0x0
 *   test +0x4a cmp r0, #0x7
 *   test +0x58 cmp r0, r1
 *   test +0x6e cmp r0, r1
 *   test +0xa8 cmp r0, #0x0
 *   test +0xbc tst r0, r1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ecbac; the literal pool and
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
extern u8 native_data2_0221a20c[];
extern void native_fn_021edbac(void);
extern void native_fn_021ed1c8(void);


asm u32 native_ov006_021ecbac (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r6, r0, #0x0
    add r5, r2, #0x0
    cmp r6, #0x1
    beq ov006_021ecbac_L12
    ldr r1, [r5, #0]
    add r1, r1, #0x1
    str r1, [r5, #0]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_L12:
    add r7, r1, #0x0
    add r7, #0xc
    add r4, r1, #0x0
    add r3, #0x8
    add r1, r7, #0x0
    add r0, r3, #0x0
    add r1, #0x10
    add r4, #0x24
    bl native_fn_021ece60
    cmp r0, #0x0
    bge ov006_021ecbac_L34
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_L34:
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    cmp r0, #0x0
    bne ov006_021ecbac_L48
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_L48:
    ldrb r0, [r4, #0]
    cmp r0, #0x7
    bne ov006_021ecbac_L86
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x1
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecbac_L64
    mov r0, #0x14
    bl native_fn_021ec6e0
    b ov006_021ecbac_L80
ov006_021ecbac_L64:
    ldr r0, [r4, #0x4]
    bl native_fn_021edc90
    mov r1, #0x2
    mvn r1, r1
    cmp r0, r1
    bne ov006_021ecbac_L7a
    mov r0, #0x15
    bl native_fn_021ec6e0
    b ov006_021ecbac_L80
ov006_021ecbac_L7a:
    mov r0, #0x18
    bl native_fn_021ec6e0
ov006_021ecbac_L80:
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_L86:
    mov r2, #0x6a
    ldr r0, =native_data2_0221a20c
    mov r1, #0x0
    lsl r2, r2, #0x4
    bl native_fn_021edbac
    ldrh r0, [r7, #0xa]
    bl native_fn_021edcb8
    add r2, r0, #0x0
    ldr r0, =0x02219b8c
    ldr r3, =native_data2_0221a20c
    str r0, [sp]
    mov r0, #0x0
    add r1, r4, #0x0
    bl native_fn_021ed1c8
    cmp r0, #0x0
    bge ov006_021ecbac_Lb6
    ldr r0, [r5, #0]
    add r0, r0, #0x1
    str r0, [r5, #0]
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_Lb6:
    ldr r0, =0x02219b4c
    ldr r1, [r0, #0x30]
    ldr r0, [r0, #0x2c]
    tst r0, r1
    bne ov006_021ecbac_Lc4
    add r0, r6, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ecbac_Lc4:
    mov r0, #0x0
    str r0, [r5, #0]
    mov r0, #0x2
    pop {r3, r4, r5, r6, r7, pc}
}
