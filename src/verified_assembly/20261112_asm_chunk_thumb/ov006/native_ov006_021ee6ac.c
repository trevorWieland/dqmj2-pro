/* ov006 row 0x021ee6ac: 240 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xdc -> native_data8_0221aa80 (image word 0x0221aa80)
 *   pool +0xe0 -> native_data3_0221aaa8 (image word 0x0221aaa8)
 *   pool +0xe4 -> constant 0x020dc3c8 (image word 0x020dc3c8)
 *   pool +0xe8 -> native_data4_0221aab0 (image word 0x0221aab0)
 *   pool +0xec -> constant 0x020dc3d0 (image word 0x020dc3d0)
 *   branch +0x18 -> +0x34
 *   back edge +0x2a -> +0x1e
 *   branch +0x32 -> +0x44
 *   branch +0x46 -> +0x82
 *   branch +0x4a -> +0x82
 *   branch +0x4e -> +0x82
 *   branch +0x54 -> +0x66
 *   back edge +0x64 -> +0x58
 *   branch +0x68 -> +0x7a
 *   back edge +0x78 -> +0x70
 *   branch +0x80 -> +0x92
 *   branch +0x98 -> +0xb8
 *   branch +0xa6 -> +0xd0
 *   branch +0xbe -> +0xd0
 *   test +0x14 cmp r5, #0x0
 *   test +0x28 cmp r1, #0x6
 *   test +0x44 cmp r4, #0x0
 *   test +0x48 cmp r6, #0x0
 *   test +0x4c cmp r6, #0x20
 *   test +0x52 cmp r6, #0x0
 *   test +0x62 cmp r0, r6
 *   test +0x66 cmp r0, #0x20
 *   test +0x76 cmp r0, #0x20
 *   test +0x96 cmp r0, #0x3
 *   test +0xa4 cmp r0, #0x3
 *   test +0xbc cmp r0, #0x1
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ee6ac; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 240 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02007ff4(void);
extern u8 native_data8_0221aa80[];
extern u8 native_data3_0221aaa8[];
extern void native_fn_02008d78(void);
extern u8 native_data4_0221aab0[];
extern void native_fn_02089d8c(void);
extern void native_fn_02008008(void);
extern void native_fn_021ee600(void);


asm u32 native_ov006_021ee6ac (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    str r3, [sp]
    add r5, r0, #0x0
    add r4, r1, #0x0
    add r6, r2, #0x0
    blx native_fn_02007ff4
    add r7, r0, #0x0
    ldr r1, =native_data8_0221aa80
    ldr r0, [sp]
    cmp r5, #0x0
    str r0, [r1, #0x4]
    beq ov006_021ee6ac_L34
    ldr r2, =native_data3_0221aaa8
    mov r1, #0x0
ov006_021ee6ac_L1e:
    ldrb r0, [r5, #0]
    add r1, r1, #0x1
    add r5, r5, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    cmp r1, #0x6
    blt ov006_021ee6ac_L1e
    ldr r1, =native_data3_0221aaa8
    ldr r0, =native_data8_0221aa80
    str r1, [r0, #0x10]
    b ov006_021ee6ac_L44
ov006_021ee6ac_L34:
    ldr r0, =native_data3_0221aaa8
    mov r1, #0xff
    mov r2, #0x6
    blx native_fn_02008d78
    ldr r1, =0x020dc3c8
    ldr r0, =native_data8_0221aa80
    str r1, [r0, #0x10]
ov006_021ee6ac_L44:
    cmp r4, #0x0
    beq ov006_021ee6ac_L82
    cmp r6, #0x0
    ble ov006_021ee6ac_L82
    cmp r6, #0x20
    bgt ov006_021ee6ac_L82
    mov r0, #0x0
    cmp r6, #0x0
    ble ov006_021ee6ac_L66
    ldr r2, =native_data4_0221aab0
ov006_021ee6ac_L58:
    ldrb r1, [r4, #0]
    add r0, r0, #0x1
    add r4, r4, #0x1
    strb r1, [r2, #0]
    add r2, r2, #0x1
    cmp r0, r6
    blt ov006_021ee6ac_L58
ov006_021ee6ac_L66:
    cmp r0, #0x20
    bge ov006_021ee6ac_L7a
    ldr r1, =native_data4_0221aab0
    add r2, r1, r0
    mov r1, #0x0
ov006_021ee6ac_L70:
    add r0, r0, #0x1
    strb r1, [r2, #0]
    add r2, r2, #0x1
    cmp r0, #0x20
    blt ov006_021ee6ac_L70
ov006_021ee6ac_L7a:
    ldr r1, =native_data4_0221aab0
    ldr r0, =native_data8_0221aa80
    str r1, [r0, #0x14]
    b ov006_021ee6ac_L92
ov006_021ee6ac_L82:
    ldr r0, =native_data4_0221aab0
    mov r1, #0xff
    mov r2, #0x20
    blx native_fn_02008d78
    ldr r1, =0x020dc3d0
    ldr r0, =native_data8_0221aa80
    str r1, [r0, #0x14]
ov006_021ee6ac_L92:
    ldr r2, =native_data8_0221aa80
    ldr r0, [r2, #0x18]
    cmp r0, #0x3
    bne ov006_021ee6ac_Lb8
    ldr r0, [r2, #0x10]
    ldr r1, [r2, #0x14]
    ldr r2, [r2, #0x4]
    bl native_fn_02089d8c
    cmp r0, #0x3
    bne ov006_021ee6ac_Ld0
    ldr r0, =native_data8_0221aa80
    mov r1, #0x6
    str r1, [r0, #0x18]
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ee6ac_Lb8:
    bl native_fn_021ee600
    cmp r0, #0x1
    bne ov006_021ee6ac_Ld0
    ldr r0, =native_data8_0221aa80
    mov r1, #0x6
    str r1, [r0, #0x18]
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ee6ac_Ld0:
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
