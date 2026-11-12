/* ov006 row 0x021ef398: 460 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c8 -> native_data3_0220d4ec (image word 0x0220d4ec)
 *   branch +0x22 -> +0xd4
 *   back edge +0x32 -> +0x2c
 *   branch +0x52 -> +0xb8
 *   branch +0x60 -> +0xb8
 *   branch +0x64 -> +0xb8
 *   branch +0x68 -> +0x74
 *   branch +0x6e -> +0xb8
 *   branch +0x72 -> +0xb8
 *   branch +0x8a -> +0xae
 *   branch +0x9a -> +0xae
 *   branch +0xa2 -> +0xae
 *   branch +0xa6 -> +0xae
 *   branch +0xac -> +0xb8
 *   back edge +0xb6 -> +0x5e
 *   branch +0xbc -> +0xd4
 *   back edge +0xd2 -> +0x24
 *   branch +0xd8 -> +0x1b0
 *   back edge +0xe6 -> +0xe0
 *   branch +0xfc -> +0x13c
 *   branch +0x122 -> +0x130
 *   branch +0x128 -> +0x130
 *   branch +0x12e -> +0x13c
 *   back edge +0x13a -> +0x100
 *   branch +0x146 -> +0x1a0
 *   branch +0x16c -> +0x18e
 *   branch +0x180 -> +0x18e
 *   branch +0x186 -> +0x18e
 *   branch +0x18c -> +0x1a0
 *   back edge +0x19e -> +0x14c
 *   branch +0x1a4 -> +0x1b0
 *   branch +0x1aa -> +0x1b0
 *   branch +0x1b4 -> +0x1c0
 *   test +0x20 cmp r0, #0x0
 *   test +0x50 cmp r0, #0x0
 *   test +0x5e cmp r5, #0x0
 *   test +0x62 cmp r5, #0x20
 *   test +0x66 cmp r5, #0x1
 *   test +0x6c cmp r0, #0x0
 *   test +0x70 cmp r0, #0x20
 *   test +0x88 cmp r0, #0x0
 *   test +0x98 cmp r0, #0x0
 *   test +0xa0 cmp r1, r0
 *   test +0xa4 cmp r1, #0x0
 *   test +0xb4 cmp r7, r0
 *   test +0xba cmp r0, #0x0
 *   test +0xd0 cmp r0, r1
 *   test +0xd6 cmp r0, #0x0
 *   test +0xfa cmp r0, #0x0
 *   test +0x120 cmp r0, #0x0
 *   test +0x126 cmp r0, #0x0
 *   test +0x138 cmp r6, r0
 *   test +0x144 cmp r0, #0x0
 *   test +0x16a cmp r6, r0
 *   test +0x17e cmp r0, #0x0
 *   test +0x184 cmp r0, #0x0
 *   test +0x19c cmp r0, r1
 *   test +0x1a2 cmp r0, #0x0
 *   test +0x1a8 cmp r0, #0x0
 *   test +0x1b2 cmp r0, #0x0
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef398; the literal pool and
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

extern void native_fn_0201b19c(void);
extern void native_fn_0201d69c(void);
extern void native_fn_0201b248(void);
extern u8 native_data3_0220d4ec[];


asm u32 native_ov006_021ef398 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x6c
    str r0, [sp]
    mov r0, #0x0
    str r0, [sp, #0x20]
    str r0, [sp, #0x1c]
    ldr r0, [sp]
    str r1, [sp, #0x4]
    add r6, r0, #0x4
    add r0, r1, #0x0
    add r4, r0, #0x4
    ldr r0, [sp, #0x20]
    str r2, [sp, #0x8]
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldr r0, [r0, #0]
    cmp r0, #0x0
    bls ov006_021ef398_Ld4
ov006_021ef398_L24:
    add r2, sp, #0x48
    add r2, #0x2
    mov r1, #0x22
    mov r0, #0x0
ov006_021ef398_L2c:
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021ef398_L2c
    add r0, sp, #0x48
    add r0, #0x2
    add r1, r6, #0x4
    mov r2, #0x20
    blx native_fn_0201b19c
    add r0, sp, #0x48
    ldr r1, [r6, #0]
    mov r7, #0x0
    add r0, #0x2
    strb r7, [r0, r1]
    ldr r0, [sp, #0x4]
    ldr r0, [r0, #0]
    str r0, [sp, #0x10]
    cmp r0, #0x0
    bls ov006_021ef398_Lb8
    add r0, r6, #0x0
    str r0, [sp, #0x24]
    add r0, #0x28
    ldr r5, [r6, #0]
    str r0, [sp, #0x24]
ov006_021ef398_L5e:
    cmp r5, #0x0
    beq ov006_021ef398_Lb8
    cmp r5, #0x20
    bhi ov006_021ef398_Lb8
    cmp r5, #0x1
    bne ov006_021ef398_L74
    ldrb r0, [r6, #0x4]
    cmp r0, #0x0
    beq ov006_021ef398_Lb8
    cmp r0, #0x20
    beq ov006_021ef398_Lb8
ov006_021ef398_L74:
    add r0, sp, #0x48
    add r0, #0x2
    blx native_fn_0201d69c
    add r2, r0, #0x0
    add r0, sp, #0x48
    add r0, #0x2
    add r1, r4, #0x4
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021ef398_Lae
    add r1, r4, #0x0
    ldr r0, [sp, #0x24]
    add r1, #0x28
    mov r2, #0x6
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021ef398_Lae
    ldrh r1, [r6, #0x2e]
    ldrh r0, [r4, #0x2e]
    cmp r1, r0
    beq ov006_021ef398_Lae
    cmp r1, #0x0
    bne ov006_021ef398_Lae
    mov r0, #0x1
    str r0, [sp, #0x20]
    b ov006_021ef398_Lb8
ov006_021ef398_Lae:
    ldr r0, [sp, #0x10]
    add r7, r7, #0x1
    add r4, #0x30
    cmp r7, r0
    blo ov006_021ef398_L5e
ov006_021ef398_Lb8:
    ldr r0, [sp, #0x20]
    cmp r0, #0x0
    bne ov006_021ef398_Ld4
    ldr r0, [sp, #0x4]
    add r6, #0x30
    add r4, r0, #0x4
    ldr r0, [sp, #0xc]
    add r0, r0, #0x1
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldr r1, [r0, #0]
    ldr r0, [sp, #0xc]
    cmp r0, r1
    blo ov006_021ef398_L24
ov006_021ef398_Ld4:
    ldr r0, [sp, #0x20]
    cmp r0, #0x0
    bne ov006_021ef398_L1b0
    add r2, sp, #0x28
    mov r1, #0x22
    mov r0, #0x0
ov006_021ef398_Le0:
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021ef398_Le0
    mov r0, #0x0
    str r0, [sp, #0x18]
    str r0, [sp, #0x14]
    ldr r0, [sp]
    ldr r6, [sp, #0x18]
    add r4, r0, #0x4
    ldr r0, [sp, #0x4]
    add r5, r0, #0x4
    ldr r0, [r0, #0]
    cmp r0, #0x0
    bls ov006_021ef398_L13c
    add r7, sp, #0x28
ov006_021ef398_L100:
    add r0, r7, #0x0
    add r1, r5, #0x4
    mov r2, #0x20
    blx native_fn_0201b19c
    ldr r1, [r5, #0]
    mov r0, #0x0
    strb r0, [r7, r1]
    ldr r0, =native_data3_0220d4ec
    blx native_fn_0201d69c
    add r2, r0, #0x0
    ldr r1, =native_data3_0220d4ec
    add r0, r7, #0x0
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021ef398_L130
    ldrh r0, [r5, #0x2e]
    cmp r0, #0x0
    bne ov006_021ef398_L130
    mov r0, #0x1
    str r0, [sp, #0x14]
    b ov006_021ef398_L13c
ov006_021ef398_L130:
    ldr r0, [sp, #0x4]
    add r6, r6, #0x1
    ldr r0, [r0, #0]
    add r5, #0x30
    cmp r6, r0
    blo ov006_021ef398_L100
ov006_021ef398_L13c:
    mov r0, #0x0
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldr r0, [r0, #0]
    cmp r0, #0x0
    bls ov006_021ef398_L1a0
    ldr r7, =native_data3_0220d4ec
    add r5, sp, #0x28
ov006_021ef398_L14c:
    add r0, r5, #0x0
    add r1, r4, #0x4
    mov r2, #0x20
    blx native_fn_0201b19c
    ldr r1, [r4, #0]
    mov r0, #0x0
    strb r0, [r5, r1]
    add r0, r5, #0x0
    blx native_fn_0201d69c
    add r6, r0, #0x0
    add r0, r7, #0x0
    blx native_fn_0201d69c
    cmp r6, r0
    bne ov006_021ef398_L18e
    add r0, r7, #0x0
    blx native_fn_0201d69c
    add r2, r0, #0x0
    add r0, r5, #0x0
    add r1, r7, #0x0
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_021ef398_L18e
    ldrh r0, [r4, #0x2e]
    cmp r0, #0x0
    bne ov006_021ef398_L18e
    mov r0, #0x1
    str r0, [sp, #0x18]
    b ov006_021ef398_L1a0
ov006_021ef398_L18e:
    ldr r0, [sp, #0xc]
    add r4, #0x30
    add r0, r0, #0x1
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldr r1, [r0, #0]
    ldr r0, [sp, #0xc]
    cmp r0, r1
    blo ov006_021ef398_L14c
ov006_021ef398_L1a0:
    ldr r0, [sp, #0x18]
    cmp r0, #0x0
    beq ov006_021ef398_L1b0
    ldr r0, [sp, #0x14]
    cmp r0, #0x0
    bne ov006_021ef398_L1b0
    mov r0, #0x1
    str r0, [sp, #0x20]
ov006_021ef398_L1b0:
    ldr r0, [sp, #0x20]
    cmp r0, #0x0
    beq ov006_021ef398_L1c0
    ldr r1, [sp, #0xc]
    ldr r0, [sp, #0x8]
    str r1, [r0, #0]
    mov r0, #0x1
    str r0, [sp, #0x1c]
ov006_021ef398_L1c0:
    ldr r0, [sp, #0x1c]
    add sp, #0x6c
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
