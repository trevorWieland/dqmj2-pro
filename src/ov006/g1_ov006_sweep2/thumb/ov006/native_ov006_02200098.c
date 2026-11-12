/* ov006 row 0x02200098: 252 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xec -> native_data_0220ba30 (image word 0x0220ba30)
 *   pool +0xf0 -> constant 0x0221c158 (image word 0x0221c158)
 *   pool +0xf4 -> constant 0x00001306 (image word 0x00001306)
 *   pool +0xf8 -> native_data_0220ba28 (image word 0x0220ba28)
 *   branch +0x10 -> +0xe8
 *   branch +0x30 -> +0xd2
 *   branch +0x4e -> +0x7a
 *   branch +0x60 -> +0xd2
 *   branch +0x68 -> +0xd2
 *   branch +0x72 -> +0xe8
 *   back edge +0x80 -> +0x42
 *   branch +0x9a -> +0xca
 *   branch +0xba -> +0xbe
 *   branch +0xc8 -> +0xd2
 *   back edge +0xd0 -> +0x8e
 *   back edge +0xe6 -> +0x16
 *   test +0x0e cmp r0, #0x0
 *   test +0x2e cmp r0, #0x0
 *   test +0x4c cmp r0, #0x0
 *   test +0x5e cmp r0, #0x0
 *   test +0x66 tst r1, r0
 *   test +0x70 cmp r1, #0x0
 *   test +0x7e cmp r4, #0x10
 *   test +0x98 cmp r0, #0x0
 *   test +0xb8 tst r1, r0
 *   test +0xce cmp r5, #0x10
 *   test +0xe4 cmp r0, r1
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200098; the literal pool and
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

extern void native_fn_020072d0(void);
extern u8 native_data_0220ba30[];
extern void native_fn_0201b248(void);
extern u8 native_data_0220ba28[];
extern void native_fn_02008e0c(void);


asm u32 native_ov006_02200098 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    str r0, [sp]
    mov r0, #0x0
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldrh r0, [r0, #0xe]
    cmp r0, #0x0
    ble ov006_02200098_Le8
    ldr r0, [sp]
    str r0, [sp, #0x8]
ov006_02200098_L16:
    ldr r0, [sp, #0x8]
    mov r1, #0xc0
    ldr r6, [r0, #0x10]
    add r0, r6, #0x0
    blx native_fn_020072d0
    add r0, r6, #0x0
    ldr r1, =native_data_0220ba30
    add r0, #0xc
    mov r2, #0x8
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_02200098_Ld2
    ldr r0, =0x0221c158
    mov r1, #0x13
    ldr r0, [r0, #0]
    lsl r1, r1, #0x8
    mov r4, #0x0
    str r0, [sp, #0x4]
    add r5, r0, r1
    mov r7, #0x6
ov006_02200098_L42:
    add r0, r6, #0x4
    add r1, r5, #0x0
    add r2, r7, #0x0
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_02200098_L7a
    mov r0, #0x7
    add r1, r4, #0x0
    mul r1, r0
    ldr r0, [sp, #0x4]
    ldr r2, =0x00001306
    add r0, r0, r1
    ldrb r0, [r0, r2]
    cmp r0, #0x0
    bne ov006_02200098_Ld2
    ldrb r1, [r6, #0x15]
    mov r0, #0x1
    tst r1, r0
    beq ov006_02200098_Ld2
    ldr r1, [sp, #0x4]
    add r2, #0x6a
    ldr r1, [r1, r2]
    cmp r1, #0x0
    beq ov006_02200098_Le8
    blx r1
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
ov006_02200098_L7a:
    add r4, r4, #0x1
    add r5, r5, #0x7
    cmp r4, #0x10
    blt ov006_02200098_L42
    mov r1, #0x13
    ldr r0, [sp, #0x4]
    lsl r1, r1, #0x8
    ldr r7, =native_data_0220ba28
    mov r5, #0x0
    add r4, r0, r1
ov006_02200098_L8e:
    add r0, r4, #0x0
    add r1, r7, #0x0
    mov r2, #0x6
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_02200098_Lca
    mov r2, #0x13
    ldr r1, [sp, #0x4]
    lsl r2, r2, #0x8
    add r1, r1, r2
    mov r0, #0x7
    add r4, r5, #0x0
    mul r4, r0
    add r0, r6, #0x4
    add r1, r1, r4
    mov r2, #0x6
    blx native_fn_02008e0c
    ldrb r1, [r6, #0x15]
    mov r0, #0x1
    tst r1, r0
    bne ov006_02200098_Lbe
    mov r0, #0x0
ov006_02200098_Lbe:
    ldr r1, =0x0221c158
    ldr r1, [r1, #0]
    add r2, r1, r4
    ldr r1, =0x00001306
    strb r0, [r2, r1]
    b ov006_02200098_Ld2
ov006_02200098_Lca:
    add r5, r5, #0x1
    add r4, r4, #0x7
    cmp r5, #0x10
    blt ov006_02200098_L8e
ov006_02200098_Ld2:
    ldr r0, [sp, #0x8]
    add r0, r0, #0x4
    str r0, [sp, #0x8]
    ldr r0, [sp, #0xc]
    add r0, r0, #0x1
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldrh r1, [r0, #0xe]
    ldr r0, [sp, #0xc]
    cmp r0, r1
    blt ov006_02200098_L16
ov006_02200098_Le8:
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
