/* ov006 row 0x021ef210: 292 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x110 -> native_data5_0221aad0 (image word 0x0221aad0)
 *   pool +0x114 -> constant 0x003fec42 (image word 0x003fec42)
 *   pool +0x118 -> native_fn_021ef108+1 (image word 0x021ef109)
 *   pool +0x11c -> native_data_0220d480 (image word 0x0220d480)
 *   pool +0x120 -> native_data_0220d494 (image word 0x0220d494)
 *   branch +0x16 -> +0x1e
 *   branch +0x2a -> +0x32
 *   branch +0x54 -> +0x5c
 *   branch +0x5a -> +0xdc
 *   branch +0x62 -> +0x6a
 *   branch +0x68 -> +0xdc
 *   branch +0x76 -> +0xd8
 *   branch +0x7a -> +0x8e
 *   branch +0x7c -> +0xa2
 *   branch +0x80 -> +0xce
 *   branch +0x84 -> +0xce
 *   branch +0x86 -> +0xd0
 *   branch +0x8a -> +0xd0
 *   branch +0x8c -> +0xce
 *   branch +0x90 -> +0xce
 *   branch +0x94 -> +0xce
 *   branch +0x96 -> +0xa8
 *   branch +0x9a -> +0xd0
 *   branch +0x9e -> +0xd0
 *   branch +0xa0 -> +0xce
 *   branch +0xa6 -> +0xd0
 *   branch +0xae -> +0xb8
 *   branch +0xb6 -> +0xd0
 *   branch +0xc6 -> +0xd0
 *   back edge +0xd6 -> +0x78
 *   back edge +0xda -> +0x4a
 *   back edge +0xe8 -> +0xe2
 *   branch +0xec -> +0x10a
 *   branch +0xfc -> +0x104
 *   branch +0x102 -> +0x10a
 *   test +0x28 cmp r0, #0x0
 *   test +0x52 cmp r0, r1
 *   test +0x60 cmp r0, #0x0
 *   test +0x74 cmp r0, #0x0
 *   test +0x78 cmp r0, #0xc
 *   test +0x7e cmp r0, #0x5
 *   test +0x82 cmp r0, #0x4
 *   test +0x88 cmp r0, #0x5
 *   test +0x8e cmp r0, #0x13
 *   test +0x92 cmp r0, #0xd
 *   test +0x98 cmp r0, #0x12
 *   test +0x9c cmp r0, #0x13
 *   test +0xac cmp r0, #0x0
 *   test +0xc4 cmp r0, #0x0
 *   test +0xd4 cmp r0, #0x0
 *   test +0xd8 cmp r4, #0x0
 *   test +0xe6 cmp r0, #0x0
 *   test +0xea cmp r5, #0x0
 *   test +0xfa cmp r0, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef210; the literal pool and
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

extern u8 native_data5_0221aad0[];
extern void native_fn_021eeed4(void);
extern void native_fn_02007c68(void);
extern void native_fn_021ef108(void);
extern void native_fn_02007da4(void);
extern void native_fn_021f1ef0(void);
extern u8 native_data_0220d480[];
extern void native_fn_02006b7c(void);
extern void native_fn_021ef0a0(void);
extern void native_fn_02007e10(void);
extern u8 native_data_0220d494[];
extern void native_fn_0209063c(void);


asm u32 native_ov006_021ef210 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x30
    ldr r0, =native_data5_0221aad0
    mov r4, #0x1
    ldr r3, [r0, #0x5c]
    ldr r0, [r0, #0x18]
    mov r2, #0xc0
    add r1, r0, #0x0
    mul r1, r2
    sub r5, r4, #0x3
    add r6, r3, r1
    bne ov006_021ef210_L1e
    add sp, #0x30
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ef210_L1e:
    add r0, r6, #0x0
    mov r1, #0x0
    lsl r2, r2, #0xa
    bl native_fn_021eeed4
    cmp r0, #0x0
    bne ov006_021ef210_L32
    add sp, #0x30
    sub r0, r4, #0x3
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ef210_L32:
    add r0, sp, #0x4
    blx native_fn_02007c68
    mov r0, #0x12
    str r0, [sp]
    ldr r1, =0x003fec42
    ldr r3, =native_fn_021ef108+1
    add r0, sp, #0x4
    mov r2, #0x0
    blx native_fn_02007da4
    mov r7, #0x0
ov006_021ef210_L4a:
    bl native_fn_021f1ef0
    ldr r1, =native_data_0220d480
    ldr r1, [r1, #0xc]
    cmp r0, r1
    blo ov006_021ef210_L5c
    mov r5, #0x2
    mvn r5, r5
    b ov006_021ef210_Ldc
ov006_021ef210_L5c:
    ldr r0, =native_data5_0221aad0
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    beq ov006_021ef210_L6a
    mov r5, #0x7
    mvn r5, r5
    b ov006_021ef210_Ldc
ov006_021ef210_L6a:
    mov r0, #0xa
    blx native_fn_02006b7c
    bl native_fn_021ef0a0
    cmp r0, #0x0
    beq ov006_021ef210_Ld8
ov006_021ef210_L78:
    cmp r0, #0xc
    bgt ov006_021ef210_L8e
    bge ov006_021ef210_La2
    cmp r0, #0x5
    bgt ov006_021ef210_Lce
    cmp r0, #0x4
    blt ov006_021ef210_Lce
    beq ov006_021ef210_Ld0
    cmp r0, #0x5
    beq ov006_021ef210_Ld0
    b ov006_021ef210_Lce
ov006_021ef210_L8e:
    cmp r0, #0x13
    bgt ov006_021ef210_Lce
    cmp r0, #0xd
    blt ov006_021ef210_Lce
    beq ov006_021ef210_La8
    cmp r0, #0x12
    beq ov006_021ef210_Ld0
    cmp r0, #0x13
    beq ov006_021ef210_Ld0
    b ov006_021ef210_Lce
ov006_021ef210_La2:
    add r4, r7, #0x0
    mov r5, #0x1
    b ov006_021ef210_Ld0
ov006_021ef210_La8:
    ldr r0, =native_data5_0221aad0
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    beq ov006_021ef210_Lb8
    mov r4, #0x0
    add r5, r4, #0x0
    sub r5, #0x8
    b ov006_021ef210_Ld0
ov006_021ef210_Lb8:
    mov r2, #0x3
    add r0, r6, #0x0
    mov r1, #0x0
    lsl r2, r2, #0x10
    bl native_fn_021eeed4
    cmp r0, #0x0
    bne ov006_021ef210_Ld0
    add sp, #0x30
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ef210_Lce:
    mov r4, #0x0
ov006_021ef210_Ld0:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne ov006_021ef210_L78
ov006_021ef210_Ld8:
    cmp r4, #0x0
    bne ov006_021ef210_L4a
ov006_021ef210_Ldc:
    add r0, sp, #0x4
    blx native_fn_02007e10
ov006_021ef210_Le2:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne ov006_021ef210_Le2
    cmp r5, #0x0
    ble ov006_021ef210_L10a
    ldr r0, =native_data5_0221aad0
    mov r1, #0x1
    str r1, [r0, #0x20]
    ldr r0, =native_data_0220d494
    bl native_fn_0209063c
    cmp r0, #0x0
    bge ov006_021ef210_L104
    mov r5, #0x1
    mvn r5, r5
    b ov006_021ef210_L10a
ov006_021ef210_L104:
    ldr r0, =native_data5_0221aad0
    mov r1, #0x1
    str r1, [r0, #0x24]
ov006_021ef210_L10a:
    add r0, r5, #0x0
    add sp, #0x30
    pop {r3, r4, r5, r6, r7, pc}
}
