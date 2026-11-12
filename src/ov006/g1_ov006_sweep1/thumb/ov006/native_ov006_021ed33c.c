/* ov006 row 0x021ed33c: 324 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x134 -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0x138 -> constant 0x000005dc (image word 0x000005dc)
 *   pool +0x13c -> native_data2_0221a8ac (image word 0x0221a8ac)
 *   pool +0x140 -> native_data_0220d448 (image word 0x0220d448)
 *   branch +0x28 -> +0x38
 *   branch +0x6c -> +0x86
 *   branch +0x76 -> +0x7e
 *   branch +0xce -> +0xe8
 *   branch +0xd8 -> +0xe0
 *   branch +0x124 -> +0x12c
 *   test +0x6a cmp r0, #0x0
 *   test +0x74 cmp r4, #0x0
 *   test +0xcc cmp r0, #0x0
 *   test +0xd6 cmp r4, #0x0
 *   test +0x122 cmp r4, #0x0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed33c; the literal pool and
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

extern void native_fn_021edbac(void);
extern void native_fn_021ebb1c(void);
extern void native_fn_021ec6e0(void);
extern u8 native_data2_0221a8ac[];
extern void native_fn_021edb9c(void);
extern void native_fn_021ed5c8(void);
extern void native_fn_021ebb2c(void);
extern void native_fn_021edc78(void);
extern void native_fn_021ed654(void);
extern u8 native_data_0220d448[];
extern void native_fn_021ed9d4(void);
extern void native_fn_021ed6a8(void);
extern void native_fn_021ed700(void);


asm u32 native_ov006_021ed33c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x20
    add r7, r1, #0x0
    mov r1, #0x0
    add r0, sp, #0x10
    strb r1, [r0, #0]
    strh r1, [r0, #0x4]
    strh r1, [r0, #0x2]
    ldr r0, =0x02219b4c
    str r2, [sp, #0xc]
    ldr r5, [r0, #0x14]
    ldr r2, =0x000005dc
    add r0, r5, #0x0
    bl native_fn_021edbac
    mov r0, #0x21
    lsl r0, r0, #0x4
    bl native_fn_021ebb1c
    add r4, r0, #0x0
    bne ov006_021ed33c_L38
    mov r0, #0x2
    bl native_fn_021ec6e0
    mov r0, #0x0
    add sp, #0x20
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed33c_L38:
    mov r2, #0x21
    mov r1, #0x0
    lsl r2, r2, #0x4
    bl native_fn_021edbac
    add r6, r5, #0x0
    ldr r0, =native_data2_0221a8ac
    add r1, r7, #0x0
    mov r2, #0x8
    add r6, #0x18
    bl native_fn_021edb9c
    add r0, sp, #0x14
    ldr r1, =native_data2_0221a8ac
    add r0, #0x2
    mov r2, #0x8
    bl native_fn_021edb9c
    add r0, r4, #0x4
    bl native_fn_021ed5c8
    add r1, sp, #0x10
    strh r0, [r1, #0x4]
    mov r0, #0x4
    ldrsh r0, [r1, r0]
    cmp r0, #0x0
    bge ov006_021ed33c_L86
    mov r0, #0x3
    bl native_fn_021ec6e0
    cmp r4, #0x0
    beq ov006_021ed33c_L7e
    add r0, r4, #0x0
    bl native_fn_021ebb2c
ov006_021ed33c_L7e:
    mov r0, #0x0
    add sp, #0x20
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed33c_L86:
    mov r0, #0x0
    strb r0, [r4, #0]
    ldrh r0, [r1, #0x4]
    bl native_fn_021edc78
    strh r0, [r4, #0x2]
    add r1, sp, #0x10
    mov r0, #0x4
    ldrsh r0, [r1, r0]
    add r2, r4, #0x0
    add r3, sp, #0x14
    add r0, r0, #0x4
    strh r0, [r1, #0x4]
    add r0, sp, #0x10
    add r0, #0x2
    str r0, [sp]
    add r0, sp, #0x10
    str r0, [sp, #0x4]
    mov r0, #0x0
    add r1, r6, #0x0
    bl native_fn_021ed654
    add r1, sp, #0x10
    mov r0, #0x2
    ldrsh r2, [r1, r0]
    mov r0, #0x10
    mov r3, #0x6
    orr r0, r2
    strh r0, [r1, #0x2]
    add r0, sp, #0x14
    ldr r2, =native_data_0220d448
    add r0, #0x2
    mov r1, #0x8
    bl native_fn_021ed9d4
    cmp r0, #0x0
    beq ov006_021ed33c_Le8
    mov r0, #0x2
    bl native_fn_021ec6e0
    cmp r4, #0x0
    beq ov006_021ed33c_Le0
    add r0, r4, #0x0
    bl native_fn_021ebb2c
ov006_021ed33c_Le0:
    mov r0, #0x0
    add sp, #0x20
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed33c_Le8:
    add r3, sp, #0x10
    mov r0, #0x0
    ldrsb r0, [r3, r0]
    mov r1, #0x1
    mov r2, #0x4
    str r0, [sp]
    mov r0, #0x11
    str r0, [sp, #0x4]
    add r0, sp, #0x14
    add r0, #0x2
    str r0, [sp, #0x8]
    mov r6, #0x2
    ldrsh r2, [r3, r2]
    ldrsh r3, [r3, r6]
    add r0, r5, #0x0
    lsl r1, r1, #0xc
    bl native_fn_021ed6a8
    add r2, sp, #0x10
    mov r1, #0x4
    ldrsh r0, [r2, r1]
    ldr r3, [sp, #0xc]
    add r0, #0x18
    strh r0, [r2, #0x4]
    ldrsh r1, [r2, r1]
    add r0, r5, #0x0
    mov r2, #0xff
    bl native_fn_021ed700
    cmp r4, #0x0
    beq ov006_021ed33c_L12c
    add r0, r4, #0x0
    bl native_fn_021ebb2c
ov006_021ed33c_L12c:
    mov r0, #0x0
    add sp, #0x20
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
