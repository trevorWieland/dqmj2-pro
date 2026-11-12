/* ov006 row 0x021f2090: 148 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> native_data6_0221aad0 (image word 0x0221aad0)
 *   pool +0x90 -> native_data2_0221ab7c (image word 0x0221ab7c)
 *   branch +0x08 -> +0x70
 *   branch +0x12 -> +0x1a
 *   branch +0x1e -> +0x24
 *   back edge +0x22 -> +0x14
 *   branch +0x34 -> +0x4e
 *   back edge +0x4c -> +0x38
 *   branch +0x54 -> +0x60
 *   branch +0x6a -> +0x70
 *   branch +0x76 -> +0x84
 *   test +0x06 cmp r0, #0x0
 *   test +0x1c cmp r0, #0x1
 *   test +0x20 cmp r0, #0x5
 *   test +0x32 cmp r0, #0x0
 *   test +0x4a cmp r0, #0x0
 *   test +0x52 cmp r0, #0x0
 *   test +0x68 cmp r6, r0
 *   test +0x74 cmp r0, #0x0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2090; the literal pool and
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

extern u8 native_data6_0221aad0[];
extern void native_fn_02006b7c(void);
extern u8 native_data2_0221ab7c[];
extern void native_fn_020068c0(void);
extern void native_fn_0200698c(void);
extern void native_fn_02006890(void);
extern void native_fn_021f2170(void);
extern void native_fn_021ef1b8(void);


asm u32 native_ov006_021f2090 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r4, =native_data6_0221aad0
    ldr r0, [r4, #0x64]
    cmp r0, #0x0
    beq ov006_021f2090_L70
    ldr r6, [r4, #0x38]
    mov r0, #0x1
    str r0, [r4, #0x10]
    mov r5, #0x64
    b ov006_021f2090_L1a
ov006_021f2090_L14:
    add r0, r5, #0x0
    blx native_fn_02006b7c
ov006_021f2090_L1a:
    ldr r0, [r4, #0x38]
    cmp r0, #0x1
    blt ov006_021f2090_L24
    cmp r0, #0x5
    ble ov006_021f2090_L14
ov006_021f2090_L24:
    mov r0, #0x7d
    lsl r0, r0, #0x2
    blx native_fn_02006b7c
    ldr r0, =native_data2_0221ab7c
    blx native_fn_020068c0
    cmp r0, #0x0
    bne ov006_021f2090_L4e
    ldr r4, =native_data2_0221ab7c
ov006_021f2090_L38:
    add r0, r4, #0x0
    blx native_fn_0200698c
    add r0, r4, #0x0
    blx native_fn_02006890
    add r0, r4, #0x0
    blx native_fn_020068c0
    cmp r0, #0x0
    beq ov006_021f2090_L38
ov006_021f2090_L4e:
    ldr r1, =native_data6_0221aad0
    ldr r0, [r1, #0x30]
    cmp r0, #0x0
    beq ov006_021f2090_L60
    ldr r1, [r1, #0xc]
    blx r1
    ldr r0, =native_data6_0221aad0
    mov r1, #0x0
    str r1, [r0, #0x30]
ov006_021f2090_L60:
    ldr r0, =native_data6_0221aad0
    mov r1, #0x0
    str r1, [r0, #0x64]
    ldr r0, [r0, #0x38]
    cmp r6, r0
    beq ov006_021f2090_L70
    bl native_fn_021f2170
ov006_021f2090_L70:
    ldr r0, =native_data6_0221aad0
    ldr r0, [r0, #0x74]
    cmp r0, #0x0
    ble ov006_021f2090_L84
    bl native_fn_021ef1b8
    ldr r1, =native_data6_0221aad0
    mov r2, #0x0
    str r2, [r1, #0x74]
    pop {r4, r5, r6, pc}
ov006_021f2090_L84:
    mov r0, #0x9
    mvn r0, r0
    pop {r4, r5, r6, pc}
    mov r8, r8
}
