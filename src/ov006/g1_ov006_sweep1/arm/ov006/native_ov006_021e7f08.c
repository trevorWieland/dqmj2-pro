/* ov006 row 0x021e7f08: 216 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> constant 0x02218fc8 (image word 0x02218fc8)
 *   pool +0xcc -> constant 0x0204594c (image word 0x0204594c)
 *   pool +0xd0 -> constant 0x02045994 (image word 0x02045994)
 *   pool +0xd4 -> constant 0x02218d8c (image word 0x02218d8c)
 *   branch +0x5c -> +0xbc
 *   branch +0x70 -> +0xa4
 *   back edge +0xa0 -> +0x80
 *   back edge +0xb8 -> +0x68
 *   test +0x40 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x6c cmp r6, #0
 *   test +0x9c cmp r7, r6
 *   test +0xb4 cmp r1, r0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e7f08; the literal pool and
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

extern void native_fn_02065d14(void);
extern void native_fn_02065d00(void);
extern void native_fn_02087544(void);


asm u32 native_ov006_021e7f08 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r4, =0x02218fc8
    mov r3, #12
    mla r4, r0, r3, r4
    ldrsb r0, [r4, #8]
    mov r10, r1
    str r2, [sp]
    ldrb r8, [r4, #0xb]
    bl native_fn_02065d14
    str r0, [sp, #0x8]
    ldrsb r0, [r4, #8]
    bl native_fn_02065d00
    mov r6, r0
    ldrb r0, [r4, #0xa]
    bl native_fn_02087544
    cmp r0, #0
    ldrne r9, =0x0204594c
    ldr r0, [sp, #0x8]
    ldreq r9, =0x02045994
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x4]
    ble ov006_021e7f08_Lbc
    ldr r4, =0x02218d8c
    mov r11, #2
ov006_021e7f08_L68:
    mov r7, #0
    cmp r6, #0
    ble ov006_021e7f08_La4
    ldr r1, [sp, #0x4]
    ldr r0, [sp]
    add r5, r1, r0
ov006_021e7f08_L80:
    add r1, r7, r10
    mov r0, r8
    add r2, r1, r5, lsl #5
    mov r1, r4
    mov r3, r11
    blx r9
    add r7, r7, #1
    cmp r7, r6
    blt ov006_021e7f08_L80
ov006_021e7f08_La4:
    ldr r0, [sp, #0x4]
    add r1, r0, #1
    ldr r0, [sp, #0x8]
    str r1, [sp, #0x4]
    cmp r1, r0
    blt ov006_021e7f08_L68
ov006_021e7f08_Lbc:
    mov r0, #1
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
