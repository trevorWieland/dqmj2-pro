/* ov006 row 0x0220026c: 216 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xbc -> constant 0x0221c158 (image word 0x0221c158)
 *   pool +0xc0 -> constant 0x00001b88 (image word 0x00001b88)
 *   pool +0xc4 -> constant 0x0017f898 (image word 0x0017f898)
 *   pool +0xc8 -> native_data_0220ba28 (image word 0x0220ba28)
 *   pool +0xcc -> constant 0x00001306 (image word 0x00001306)
 *   pool +0xd0 -> constant 0x00001370 (image word 0x00001370)
 *   pool +0xd4 -> constant 0x00001b90 (image word 0x00001b90)
 *   branch +0x26 -> +0xb8
 *   branch +0x42 -> +0x54
 *   branch +0x4a -> +0x52
 *   branch +0x50 -> +0x54
 *   back edge +0x5c -> +0x36
 *   branch +0x62 -> +0x78
 *   branch +0x66 -> +0x78
 *   branch +0x70 -> +0xa0
 *   branch +0x76 -> +0xa0
 *   branch +0x7c -> +0x8e
 *   branch +0x86 -> +0xa0
 *   branch +0x8c -> +0xa0
 *   branch +0x90 -> +0xa0
 *   branch +0x9a -> +0xa0
 *   test +0x40 cmp r0, #0x0
 *   test +0x48 cmp r0, #0x0
 *   test +0x5a cmp r6, #0x10
 *   test +0x60 cmp r0, #0x0
 *   test +0x64 cmp r7, #0x0
 *   test +0x6e cmp r1, #0x0
 *   test +0x7a cmp r0, #0x0
 *   test +0x84 cmp r1, #0x0
 *   test +0x8e cmp r7, #0x0
 *   test +0x98 cmp r1, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220026c; the literal pool and
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

extern void native_fn_02007a9c(void);
extern u8 native_data_0220ba28[];
extern void native_fn_0201b248(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_0220026c (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    str r0, [sp]
    blx native_fn_02007a9c
    ldr r2, =0x0221c158
    ldr r3, =0x00001b88
    ldr r2, [r2, #0]
    add r4, r3, #0x4
    str r2, [sp, #0x4]
    ldr r2, [r2, r3]
    ldr r3, [sp, #0x4]
    mov r7, #0x0
    ldr r4, [r3, r4]
    ldr r3, =0x0017f898
    add r2, r2, r3
    adc r4, r7
    sub r0, r0, r2
    sbc r1, r4
    blo ov006_0220026c_Lb8
    mov r1, #0x13
    ldr r0, [sp, #0x4]
    lsl r1, r1, #0x8
    str r7, [sp, #0x8]
    add r6, r7, #0x0
    add r4, r0, r1
    add r5, r0, #0x0
ov006_0220026c_L36:
    ldr r1, =native_data_0220ba28
    add r0, r4, #0x0
    mov r2, #0x6
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_0220026c_L54
    ldr r0, =0x00001306
    ldrb r0, [r5, r0]
    cmp r0, #0x0
    beq ov006_0220026c_L52
    mov r0, #0x1
    str r0, [sp, #0x8]
    b ov006_0220026c_L54
ov006_0220026c_L52:
    mov r7, #0x1
ov006_0220026c_L54:
    add r6, r6, #0x1
    add r4, r4, #0x7
    add r5, r5, #0x7
    cmp r6, #0x10
    blt ov006_0220026c_L36
    ldr r0, [sp, #0x8]
    cmp r0, #0x0
    beq ov006_0220026c_L78
    cmp r7, #0x0
    beq ov006_0220026c_L78
    ldr r1, =0x00001370
    ldr r0, [sp, #0x4]
    ldr r1, [r0, r1]
    cmp r1, #0x0
    beq ov006_0220026c_La0
    mov r0, #0x2
    blx r1
    b ov006_0220026c_La0
ov006_0220026c_L78:
    ldr r0, [sp, #0x8]
    cmp r0, #0x0
    beq ov006_0220026c_L8e
    ldr r1, =0x00001370
    ldr r0, [sp, #0x4]
    ldr r1, [r0, r1]
    cmp r1, #0x0
    beq ov006_0220026c_La0
    mov r0, #0x1
    blx r1
    b ov006_0220026c_La0
ov006_0220026c_L8e:
    cmp r7, #0x0
    bne ov006_0220026c_La0
    ldr r1, =0x00001370
    ldr r0, [sp, #0x4]
    ldr r1, [r0, r1]
    cmp r1, #0x0
    beq ov006_0220026c_La0
    mov r0, #0x0
    blx r1
ov006_0220026c_La0:
    ldr r2, =0x0221c158
    ldr r1, =0x00001b90
    ldr r3, [r2, #0]
    mov r0, #0x0
    str r0, [r3, r1]
    ldr r2, [r2, #0]
    mov r3, #0x1
    add r1, r1, #0x6
    strb r3, [r2, r1]
    ldr r1, [sp]
    bl native_fn_02204974
ov006_0220026c_Lb8:
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
