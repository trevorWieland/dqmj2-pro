/* ov006 row 0x021faf60: 200 bytes.
 *
 * What it does: Writes one block of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc0 -> constant 0x0000e01d (image word 0x0000e01d)
 *   pool +0xc4 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x1e -> +0x24
 *   branch +0x22 -> +0x26
 *   branch +0x2a -> +0x44
 *   branch +0x34 -> +0x3a
 *   branch +0x38 -> +0x3c
 *   back edge +0x42 -> +0x30
 *   branch +0x4c -> +0x50
 *   branch +0x6e -> +0xba
 *   branch +0x80 -> +0x9c
 *   branch +0x8c -> +0x92
 *   branch +0x90 -> +0x94
 *   back edge +0x9a -> +0x86
 *   test +0x1c cmp r4, #0x10
 *   test +0x28 cmp r6, #0x0
 *   test +0x32 cmp r1, #0x20
 *   test +0x40 cmp r2, r6
 *   test +0x4a cmp r4, #0x10
 *   test +0x6c cmp r4, #0x10
 *   test +0x7e cmp r4, #0x0
 *   test +0x8a cmp r3, #0x20
 *   test +0x98 cmp r1, r4
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021faf60; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_022045c8(void);
extern void native_fn_0220374c(void);


asm u32 native_ov006_021faf60 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x30
    add r5, r0, #0x0
    add r7, r1, #0x0
    add r0, sp, #0xc
    mov r1, #0x0
    mov r2, #0x22
    blx native_fn_02008d78
    add r0, r5, #0x0
    mov r1, #0x20
    bl native_fn_022045c8
    add r4, r0, #0x0
    cmp r4, #0x10
    bgt ov006_021faf60_L24
    add r6, r4, #0x0
    b ov006_021faf60_L26
ov006_021faf60_L24:
    mov r6, #0x10
ov006_021faf60_L26:
    mov r2, #0x0
    cmp r6, #0x0
    ble ov006_021faf60_L44
    ldr r0, =0x0000e01d
    add r3, sp, #0xc
ov006_021faf60_L30:
    ldrb r1, [r5, r2]
    cmp r1, #0x20
    bne ov006_021faf60_L3a
    strh r0, [r3, #0]
    b ov006_021faf60_L3c
ov006_021faf60_L3a:
    strh r1, [r3, #0]
ov006_021faf60_L3c:
    add r2, r2, #0x1
    add r3, r3, #0x2
    cmp r2, r6
    blt ov006_021faf60_L30
ov006_021faf60_L44:
    mov r0, #0x1d
    mul r0, r7
    add r6, r0, #0x2
    cmp r4, #0x10
    bgt ov006_021faf60_L50
    add r6, r6, #0x5
ov006_021faf60_L50:
    mov r0, #0x8
    str r0, [sp]
    add r0, sp, #0xc
    str r0, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r0, =0x0221c0ec
    mov r1, #0x48
    ldr r0, [r0, #0x8]
    add r2, r6, #0x0
    ldr r0, [r0, #0x14]
    mov r3, #0x2
    bl native_fn_0220374c
    cmp r4, #0x10
    ble ov006_021faf60_Lba
    add r0, sp, #0xc
    mov r1, #0x0
    mov r2, #0x22
    blx native_fn_02008d78
    sub r4, #0x10
    mov r1, #0x0
    cmp r4, #0x0
    ble ov006_021faf60_L9c
    ldr r2, =0x0000e01d
    add r0, sp, #0xc
ov006_021faf60_L86:
    add r3, r5, r1
    ldrb r3, [r3, #0x10]
    cmp r3, #0x20
    bne ov006_021faf60_L92
    strh r2, [r0, #0]
    b ov006_021faf60_L94
ov006_021faf60_L92:
    strh r3, [r0, #0]
ov006_021faf60_L94:
    add r1, r1, #0x1
    add r0, r0, #0x2
    cmp r1, r4
    blt ov006_021faf60_L86
ov006_021faf60_L9c:
    mov r0, #0x8
    str r0, [sp]
    add r0, sp, #0xc
    str r0, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r0, =0x0221c0ec
    add r6, #0xc
    ldr r0, [r0, #0x8]
    mov r1, #0x48
    ldr r0, [r0, #0x14]
    add r2, r6, #0x0
    mov r3, #0x2
    bl native_fn_0220374c
ov006_021faf60_Lba:
    add sp, #0x30
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
