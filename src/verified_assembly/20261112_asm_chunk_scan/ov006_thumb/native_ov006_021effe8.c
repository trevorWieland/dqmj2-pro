/* ov006 row 0x021effe8: 392 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x168 -> native_data_0221ac3c (image word 0x0221ac3c)
 *   pool +0x16c -> native_data_0221ae24 (image word 0x0221ae24)
 *   pool +0x170 -> native_data_0221ae50 (image word 0x0221ae50)
 *   pool +0x174 -> native_data_0221ac50 (image word 0x0221ac50)
 *   pool +0x178 -> native_data_0221ae88 (image word 0x0221ae88)
 *   pool +0x17c -> native_data_0221ac64 (image word 0x0221ac64)
 *   pool +0x180 -> native_data_0221ace4 (image word 0x0221ace4)
 *   pool +0x184 -> native_data_0221af20 (image word 0x0221af20)
 *   branch +0x16 -> +0x1a
 *   branch +0x18 -> +0x15a
 *   branch +0x34 -> +0x160
 *   branch +0x3a -> +0x44
 *   branch +0x42 -> +0x160
 *   branch +0x68 -> +0x88
 *   branch +0x6c -> +0x7a
 *   branch +0x6e -> +0xb2
 *   branch +0x72 -> +0xc4
 *   branch +0x76 -> +0xf0
 *   branch +0x78 -> +0x11c
 *   branch +0x7c -> +0x82
 *   branch +0x7e -> +0x122
 *   branch +0x80 -> +0x11c
 *   branch +0x84 -> +0x96
 *   branch +0x86 -> +0x11c
 *   branch +0x8a -> +0x90
 *   branch +0x8c -> +0xde
 *   branch +0x8e -> +0x11c
 *   branch +0x92 -> +0x10a
 *   branch +0x94 -> +0x11c
 *   branch +0xb0 -> +0x122
 *   branch +0xc2 -> +0x122
 *   back edge +0xda -> +0xd0
 *   branch +0xdc -> +0x122
 *   branch +0xee -> +0x122
 *   back edge +0x106 -> +0xfc
 *   branch +0x108 -> +0x122
 *   branch +0x11a -> +0x122
 *   back edge +0x12a -> +0x50
 *   branch +0x12c -> +0x160
 *   back edge +0x140 -> +0x13a
 *   branch +0x142 -> +0x160
 *   back edge +0x156 -> +0x150
 *   branch +0x158 -> +0x160
 *   test +0x14 cmp r0, #0x3
 *   test +0x38 cmp r1, #0x0
 *   test +0x66 cmp r0, #0x10
 *   test +0x6a cmp r0, #0xa
 *   test +0x70 cmp r0, #0xd
 *   test +0x74 cmp r0, #0x10
 *   test +0x7a cmp r0, #0x0
 *   test +0x82 cmp r0, #0x5
 *   test +0x88 cmp r0, #0x1a
 *   test +0x90 cmp r0, #0x20
 *   test +0x128 cmp r7, #0x4
 *   22 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021effe8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0221ac3c[];
extern u8 native_data_0221ae24[];
extern void native_fn_0201d6b8(void);
extern u8 native_data_0221ae50[];
extern u8 native_data10_0221ac50[];
extern u8 native_data_0221ae88[];
extern u8 native_data_0221ac64[];
extern void native_fn_0201b19c(void);
extern void native_fn_0201d69c(void);
extern void native_fn_021eff34(void);
extern u8 native_data2_0221ace4[];
extern u8 native_data2_0221af20[];


asm u32 native_ov006_021effe8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x28
    mov r0, #0x1
    str r0, [sp, #0]
    ldr r0, =native_data_0221ac3c
    ldr r1, =native_data_0221ae24
    blx native_fn_0201d6b8
    ldr r1, =native_data_0221ae50
    ldr r0, [r1, #0]
    cmp r0, #0x3
    bls ov006_021effe8_L1a
    b ov006_021effe8_L15a
ov006_021effe8_L1a:
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    lsl r6, r0, #0
    lsl r6, r1, #0
    lsl r6, r0, #0x4
    lsl r4, r3, #0x4
    ldr r0, =native_data10_0221ac50
    mov r1, #0x0
    str r1, [r0, #0xc]
    b ov006_021effe8_L160
    ldr r1, [r1, #0x4]
    cmp r1, #0x0
    bne ov006_021effe8_L44
    mov r0, #0x6
    mvn r0, r0
    str r0, [sp, #0]
    b ov006_021effe8_L160
ov006_021effe8_L44:
    ldr r0, =native_data10_0221ac50
    ldr r6, =native_data_0221ae88
    ldr r5, =native_data_0221ac64
    str r1, [r0, #0x10]
    mov r7, #0x0
    add r4, sp, #0x4
ov006_021effe8_L50:
    add r0, sp, #0x4
    add r1, r6, #0x0
    mov r2, #0x20
    blx native_fn_0201b19c
    mov r1, #0x0
    add r0, sp, #0x24
    strb r1, [r0, #0]
    add r0, sp, #0x4
    blx native_fn_0201d69c
    cmp r0, #0x10
    bhi ov006_021effe8_L88
    cmp r0, #0xa
    blo ov006_021effe8_L7a
    beq ov006_021effe8_Lb2
    cmp r0, #0xd
    beq ov006_021effe8_Lc4
    cmp r0, #0x10
    beq ov006_021effe8_Lf0
    b ov006_021effe8_L11c
ov006_021effe8_L7a:
    cmp r0, #0x0
    bhi ov006_021effe8_L82
    beq ov006_021effe8_L122
    b ov006_021effe8_L11c
ov006_021effe8_L82:
    cmp r0, #0x5
    beq ov006_021effe8_L96
    b ov006_021effe8_L11c
ov006_021effe8_L88:
    cmp r0, #0x1a
    bhi ov006_021effe8_L90
    beq ov006_021effe8_Lde
    b ov006_021effe8_L11c
ov006_021effe8_L90:
    cmp r0, #0x20
    beq ov006_021effe8_L10a
    b ov006_021effe8_L11c
ov006_021effe8_L96:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x1
    str r1, [r0, #0xc]
    ldrb r0, [r4, #0]
    strb r0, [r5, #0]
    ldrb r0, [r4, #0x1]
    strb r0, [r5, #0x1]
    ldrb r0, [r4, #0x2]
    strb r0, [r5, #0x2]
    ldrb r0, [r4, #0x3]
    strb r0, [r5, #0x3]
    ldrb r0, [r4, #0x4]
    strb r0, [r5, #0x4]
    b ov006_021effe8_L122
ov006_021effe8_Lb2:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x1
    str r1, [r0, #0xc]
    add r0, r5, #0x0
    add r1, r4, #0x0
    mov r2, #0xa
    bl native_fn_021eff34
    b ov006_021effe8_L122
ov006_021effe8_Lc4:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x2
    str r1, [r0, #0xc]
    add r3, r4, #0x0
    add r2, r5, #0x0
    mov r1, #0xd
ov006_021effe8_Ld0:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021effe8_Ld0
    b ov006_021effe8_L122
ov006_021effe8_Lde:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x2
    str r1, [r0, #0xc]
    add r0, r5, #0x0
    add r1, r4, #0x0
    mov r2, #0x1a
    bl native_fn_021eff34
    b ov006_021effe8_L122
ov006_021effe8_Lf0:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x3
    str r1, [r0, #0xc]
    add r3, r4, #0x0
    add r2, r5, #0x0
    mov r1, #0x10
ov006_021effe8_Lfc:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021effe8_Lfc
    b ov006_021effe8_L122
ov006_021effe8_L10a:
    ldr r0, =native_data10_0221ac50
    mov r1, #0x3
    str r1, [r0, #0xc]
    add r0, r5, #0x0
    add r1, r4, #0x0
    mov r2, #0x20
    bl native_fn_021eff34
    b ov006_021effe8_L122
ov006_021effe8_L11c:
    mov r0, #0x6
    mvn r0, r0
    str r0, [sp, #0]
ov006_021effe8_L122:
    add r7, r7, #0x1
    add r6, #0x28
    add r5, #0x20
    cmp r7, #0x4
    blt ov006_021effe8_L50
    b ov006_021effe8_L160
    ldr r0, =native_data10_0221ac50
    mov r1, #0x4
    ldr r4, =native_data2_0221ace4
    ldr r3, =native_data2_0221af20
    str r1, [r0, #0xc]
    mov r2, #0x8
ov006_021effe8_L13a:
    ldmia r3!, {r0, r1}
    stmia r4!, {r0, r1}
    sub r2, r2, #0x1
    bne ov006_021effe8_L13a
    b ov006_021effe8_L160
    ldr r0, =native_data10_0221ac50
    mov r1, #0x5
    ldr r4, =native_data2_0221ace4
    ldr r3, =native_data2_0221af20
    str r1, [r0, #0xc]
    mov r2, #0x8
ov006_021effe8_L150:
    ldmia r3!, {r0, r1}
    stmia r4!, {r0, r1}
    sub r2, r2, #0x1
    bne ov006_021effe8_L150
    b ov006_021effe8_L160
ov006_021effe8_L15a:
    mov r0, #0x6
    mvn r0, r0
    str r0, [sp, #0]
ov006_021effe8_L160:
    ldr r0, [sp, #0]
    add sp, #0x28
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
