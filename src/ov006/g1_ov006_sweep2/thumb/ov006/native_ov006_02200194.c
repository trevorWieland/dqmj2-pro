/* ov006 row 0x02200194: 216 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc4 -> constant 0x0221c158 (image word 0x0221c158)
 *   pool +0xc8 -> constant 0x00001b95 (image word 0x00001b95)
 *   pool +0xcc -> constant 0x00001370 (image word 0x00001370)
 *   pool +0xd0 -> native_data_0220ba30 (image word 0x0220ba30)
 *   pool +0xd4 -> constant 0x00001306 (image word 0x00001306)
 *   branch +0x10 -> +0x20
 *   branch +0x18 -> +0xc0
 *   branch +0x3a -> +0xc0
 *   branch +0x56 -> +0xae
 *   branch +0x5e -> +0xae
 *   branch +0x76 -> +0xa6
 *   branch +0x88 -> +0xae
 *   branch +0x92 -> +0x9c
 *   back edge +0xac -> +0x6a
 *   back edge +0xbe -> +0x44
 *   test +0x0e cmp r0, #0x0
 *   test +0x16 cmp r1, #0x0
 *   test +0x38 cmp r0, #0x0
 *   test +0x54 cmp r0, #0x0
 *   test +0x5c tst r0, r1
 *   test +0x74 cmp r0, #0x0
 *   test +0x86 cmp r0, #0x0
 *   test +0x90 cmp r1, #0x0
 *   test +0xaa cmp r4, #0x10
 *   test +0xbc cmp r1, r0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200194; the literal pool and
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


asm u32 native_ov006_02200194 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    str r0, [sp]
    ldr r0, =0x0221c158
    ldr r2, [r0, #0]
    ldr r0, =0x00001b95
    ldrb r0, [r2, r0]
    cmp r0, #0x0
    beq ov006_02200194_L20
    ldr r1, =0x00001370
    ldr r1, [r2, r1]
    cmp r1, #0x0
    beq ov006_02200194_Lc0
    blx r1
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
ov006_02200194_L20:
    mov r0, #0xf
    lsl r0, r0, #0x8
    mov r1, #0x1
    add r0, r2, r0
    lsl r1, r1, #0xa
    blx native_fn_020072d0
    mov r0, #0x0
    str r0, [sp, #0xc]
    ldr r0, [sp]
    ldrh r0, [r0, #0xe]
    str r0, [sp, #0x4]
    cmp r0, #0x0
    ble ov006_02200194_Lc0
    ldr r0, =0x0221c158
    mov r7, #0x6
    ldr r0, [r0, #0]
    str r0, [sp, #0x8]
ov006_02200194_L44:
    ldr r0, [sp]
    ldr r1, =native_data_0220ba30
    ldr r6, [r0, #0x10]
    mov r2, #0x8
    add r0, r6, #0x0
    add r0, #0xc
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_02200194_Lae
    ldrb r1, [r6, #0x15]
    mov r0, #0x1
    tst r0, r1
    beq ov006_02200194_Lae
    mov r0, #0x13
    ldr r1, [sp, #0x8]
    lsl r0, r0, #0x8
    mov r4, #0x0
    add r5, r1, r0
ov006_02200194_L6a:
    add r0, r6, #0x4
    add r1, r5, #0x0
    add r2, r7, #0x0
    blx native_fn_0201b248
    cmp r0, #0x0
    bne ov006_02200194_La6
    mov r0, #0x7
    add r1, r4, #0x0
    mul r1, r0
    ldr r0, [sp, #0x8]
    add r1, r0, r1
    ldr r0, =0x00001306
    ldrb r0, [r1, r0]
    cmp r0, #0x0
    bne ov006_02200194_Lae
    ldr r1, =0x00001370
    ldr r0, [sp, #0x8]
    ldr r1, [r0, r1]
    cmp r1, #0x0
    beq ov006_02200194_L9c
    mov r0, #0x1
    blx r1
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
ov006_02200194_L9c:
    ldr r1, =0x00001b95
    mov r2, #0x1
    strb r2, [r0, r1]
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
ov006_02200194_La6:
    add r4, r4, #0x1
    add r5, r5, #0x7
    cmp r4, #0x10
    blt ov006_02200194_L6a
ov006_02200194_Lae:
    ldr r0, [sp]
    add r0, r0, #0x4
    str r0, [sp]
    ldr r0, [sp, #0xc]
    add r1, r0, #0x1
    ldr r0, [sp, #0x4]
    str r1, [sp, #0xc]
    cmp r1, r0
    blt ov006_02200194_L44
ov006_02200194_Lc0:
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
