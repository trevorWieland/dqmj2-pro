/* ov006 row 0x021ef114: 164 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> native_data3_0221aad0 (image word 0x0221aad0)
 *   pool +0x98 -> constant 0x000024d0 (image word 0x000024d0)
 *   pool +0x9c -> constant 0x00002490 (image word 0x00002490)
 *   pool +0xa0 -> native_fn_021ef0d8+1 (image word 0x021ef0d9)
 *   branch +0x2a -> +0x30
 *   branch +0x56 -> +0x5c
 *   branch +0x6c -> +0x8c
 *   branch +0x70 -> +0x84
 *   branch +0x74 -> +0x84
 *   branch +0x78 -> +0x80
 *   branch +0x7e -> +0x84
 *   back edge +0x8a -> +0x6e
 *   back edge +0x8e -> +0x60
 *   test +0x26 cmp r0, #0x0
 *   test +0x54 cmp r0, #0x0
 *   test +0x6a cmp r0, #0x0
 *   test +0x6e cmp r0, #0x4
 *   test +0x72 cmp r0, #0x5
 *   test +0x76 cmp r0, #0x6
 *   test +0x88 cmp r0, #0x0
 *   test +0x8c cmp r4, #0x0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef114; the literal pool and
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

extern u8 native_data3_0221aad0[];
extern void native_fn_021ef078(void);
extern void native_fn_021ef0d8(void);
extern void native_fn_021eef58(void);
extern void native_fn_02006b7c(void);
extern void native_fn_021ef0a0(void);


asm u32 native_ov006_021ef114 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r6, r0, #0x0
    ldr r0, =native_data3_0221aad0
    mov r4, #0x1
    str r6, [r0, #0x70]
    bl native_fn_021ef078
    mov r0, #0xd0
    add r7, r6, #0x0
    mul r7, r0
    ldr r0, =0x000024d0
    add r1, r7, r0
    mov r0, #0xc0
    mul r0, r6
    add r0, r1, r0
    ldr r1, =native_data3_0221aad0
    ldr r1, [r1, #0x4]
    blx r1
    ldr r6, =native_data3_0221aad0
    cmp r0, #0x0
    str r0, [r6, #0x54]
    bne ov006_021ef114_L30
    sub r0, r4, #0x2
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ef114_L30:
    mov r1, #0x1f
    add r2, r0, r1
    add r0, r1, #0x0
    sub r0, #0x3f
    add r3, r2, #0x0
    and r3, r0
    ldr r0, =0x00002490
    str r3, [r6, #0x40]
    add r2, r7, r0
    add r0, r3, r2
    add r0, r0, r1
    sub r1, #0x3f
    and r0, r1
    str r0, [r6, #0x5c]
    ldr r0, =native_fn_021ef0d8+1
    add r1, r3, #0x0
    bl native_fn_021eef58
    cmp r0, #0x0
    bne ov006_021ef114_L5c
    sub r0, r4, #0x3
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ef114_L5c:
    mov r6, #0x0
    add r7, r4, #0x0
ov006_021ef114_L60:
    mov r0, #0xa
    blx native_fn_02006b7c
    bl native_fn_021ef0a0
    cmp r0, #0x0
    beq ov006_021ef114_L8c
ov006_021ef114_L6e:
    cmp r0, #0x4
    beq ov006_021ef114_L84
    cmp r0, #0x5
    beq ov006_021ef114_L84
    cmp r0, #0x6
    bne ov006_021ef114_L80
    add r4, r6, #0x0
    add r5, r7, #0x0
    b ov006_021ef114_L84
ov006_021ef114_L80:
    mov r4, #0x0
    sub r5, r4, #0x2
ov006_021ef114_L84:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne ov006_021ef114_L6e
ov006_021ef114_L8c:
    cmp r4, #0x0
    bne ov006_021ef114_L60
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
}
