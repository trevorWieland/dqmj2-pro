/* ov006 row 0x021eed5c: 232 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd4 -> native_data7_0221aad0 (image word 0x0221aad0)
 *   pool +0xd8 -> native_data2_0221af88 (image word 0x0221af88)
 *   pool +0xdc -> constant 0x020dc3c8 (image word 0x020dc3c8)
 *   pool +0xe0 -> native_data3_0221afc0 (image word 0x0221afc0)
 *   pool +0xe4 -> constant 0x020dc3d0 (image word 0x020dc3d0)
 *   branch +0x1c -> +0x30
 *   back edge +0x2c -> +0x20
 *   branch +0x2e -> +0x3e
 *   branch +0x46 -> +0x7a
 *   branch +0x4a -> +0x7a
 *   branch +0x4e -> +0x7a
 *   branch +0x54 -> +0x64
 *   back edge +0x62 -> +0x56
 *   branch +0x66 -> +0x8a
 *   back edge +0x76 -> +0x6e
 *   branch +0x78 -> +0x8a
 *   branch +0x90 -> +0xb0
 *   branch +0x9e -> +0xc8
 *   branch +0xb6 -> +0xc8
 *   test +0x14 cmp r5, #0x0
 *   test +0x2a cmp r2, #0x6
 *   test +0x42 cmp r4, #0x0
 *   test +0x48 cmp r6, #0x0
 *   test +0x4c cmp r6, #0x20
 *   test +0x52 cmp r6, #0x0
 *   test +0x60 cmp r0, r6
 *   test +0x64 cmp r0, #0x20
 *   test +0x74 cmp r0, #0x20
 *   test +0x8e cmp r0, #0x3
 *   test +0x9c cmp r0, #0x3
 *   test +0xb4 cmp r0, #0x1
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eed5c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 232 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02007ff4(void);
extern u8 native_data7_0221aad0[];
extern u8 native_data2_0221af88[];
extern void native_fn_02008d78(void);
extern u8 native_data3_0221afc0[];
extern void native_fn_02089d8c(void);
extern void native_fn_02008008(void);
extern void native_fn_021eecb0(void);


asm u32 native_ov006_021eed5c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    str r3, [sp]
    add r5, r0, #0x0
    add r4, r1, #0x0
    add r6, r2, #0x0
    blx native_fn_02007ff4
    add r7, r0, #0x0
    ldr r1, =native_data7_0221aad0
    ldr r0, [sp]
    cmp r5, #0x0
    str r0, [r1, #0x60]
    ldr r0, =native_data2_0221af88
    str r0, [r1, #0x44]
    beq ov006_021eed5c_L30
    mov r2, #0x0
ov006_021eed5c_L20:
    ldrb r1, [r5, #0]
    add r2, r2, #0x1
    add r5, r5, #0x1
    strb r1, [r0, #0]
    add r0, r0, #0x1
    cmp r2, #0x6
    blt ov006_021eed5c_L20
    b ov006_021eed5c_L3e
ov006_021eed5c_L30:
    mov r1, #0xff
    mov r2, #0x6
    blx native_fn_02008d78
    ldr r1, =0x020dc3c8
    ldr r0, =native_data7_0221aad0
    str r1, [r0, #0x44]
ov006_021eed5c_L3e:
    ldr r2, =native_data3_0221afc0
    ldr r0, =native_data7_0221aad0
    cmp r4, #0x0
    str r2, [r0, #0x48]
    beq ov006_021eed5c_L7a
    cmp r6, #0x0
    ble ov006_021eed5c_L7a
    cmp r6, #0x20
    bge ov006_021eed5c_L7a
    mov r0, #0x0
    cmp r6, #0x0
    ble ov006_021eed5c_L64
ov006_021eed5c_L56:
    ldrb r1, [r4, #0]
    add r0, r0, #0x1
    add r4, r4, #0x1
    strb r1, [r2, #0]
    add r2, r2, #0x1
    cmp r0, r6
    blt ov006_021eed5c_L56
ov006_021eed5c_L64:
    cmp r0, #0x20
    bge ov006_021eed5c_L8a
    ldr r1, =native_data3_0221afc0
    add r2, r1, r0
    mov r1, #0x0
ov006_021eed5c_L6e:
    add r0, r0, #0x1
    strb r1, [r2, #0]
    add r2, r2, #0x1
    cmp r0, #0x20
    blt ov006_021eed5c_L6e
    b ov006_021eed5c_L8a
ov006_021eed5c_L7a:
    ldr r0, =native_data3_0221afc0
    mov r1, #0xff
    mov r2, #0x20
    blx native_fn_02008d78
    ldr r1, =0x020dc3d0
    ldr r0, =native_data7_0221aad0
    str r1, [r0, #0x48]
ov006_021eed5c_L8a:
    ldr r2, =native_data7_0221aad0
    ldr r0, [r2, #0x2c]
    cmp r0, #0x3
    bne ov006_021eed5c_Lb0
    ldr r1, [r2, #0x48]
    ldr r0, =native_data2_0221af88
    ldr r2, [r2, #0x60]
    bl native_fn_02089d8c
    cmp r0, #0x3
    bne ov006_021eed5c_Lc8
    ldr r0, =native_data7_0221aad0
    mov r1, #0x6
    str r1, [r0, #0x2c]
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
ov006_021eed5c_Lb0:
    bl native_fn_021eecb0
    cmp r0, #0x1
    bne ov006_021eed5c_Lc8
    ldr r0, =native_data7_0221aad0
    mov r1, #0x6
    str r1, [r0, #0x2c]
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
ov006_021eed5c_Lc8:
    add r0, r7, #0x0
    blx native_fn_02008008
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
