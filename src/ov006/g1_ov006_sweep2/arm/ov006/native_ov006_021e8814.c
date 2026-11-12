/* ov006 row 0x021e8814: 476 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c8 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x1cc -> constant 0x02218e18 (image word 0x02218e18)
 *   pool +0x1d0 -> constant 0x02218d90 (image word 0x02218d90)
 *   pool +0x1d4 -> constant 0x02218f38 (image word 0x02218f38)
 *   pool +0x1d8 -> constant 0x02218ea8 (image word 0x02218ea8)
 *   branch +0x68 -> +0x164
 *   branch +0xac -> +0xbc
 *   branch +0xc8 -> +0xe4
 *   branch +0xe0 -> +0xec
 *   back edge +0x100 -> +0xa4
 *   branch +0x114 -> +0x124
 *   branch +0x13c -> +0x14c
 *   test +0x10 cmp r7, r4
 *   test +0x60 cmp r2, r5
 *   test +0x78 cmp r0, #6
 *   test +0xa4 cmp r7, r6
 *   test +0xb0 cmp r7, r9
 *   test +0xc4 cmp r7, r9
 *   test +0xf8 cmp r7, #6
 *   test +0x104 cmp r5, #0
 *   test +0x12c cmp r0, #6
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e8814; the literal pool and
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

extern void native_fn_021e80c4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0204b53c(void);
extern void native_fn_021e7a88(void);
extern void native_fn_021e75ec(void);
extern void native_fn_021e7b00(void);
extern void native_fn_0205e7a8(void);


asm u32 native_ov006_021e8814 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r7, r0
    mov r4, r1
    cmp r7, r4
    mov r6, r2
    mov r10, r3
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r2, =0x2aaaaaab
    add r1, sp, #4
    smull r0, r5, r2, r4
    mov r0, r4
    add r5, r5, r4, lsr #31
    bl native_fn_021e80c4
    ldr r0, =0x02218e18
    mov r1, #1
    bl native_fn_0204b61c
    ldr r0, =0x02218e18
    add r1, sp, #4
    bl native_fn_0204b53c
    ldr r1, =0x2aaaaaab
    smull r0, r2, r1, r7
    add r2, r2, r7, lsr #31
    cmp r2, r5
    mov r2, #6
    beq ov006_021e8814_L164
    mov r9, #6
    mul r8, r5, r9
    sub r0, r6, r8
    cmp r0, #6
    ldr r1, =0x2aaaaaab
    str r0, [sp]
    movlt r9, r0
    smull r0, r6, r1, r4
    add r6, r6, r4, lsr #31
    smull r0, r1, r2, r6
    sub r6, r4, r0
    ldr r4, =0x02218d90
    mov r7, #0
    mov r11, #1
ov006_021e8814_La4:
    cmp r7, r6
    moveq r1, r11
    beq ov006_021e8814_Lbc
    cmp r7, r9
    movlt r1, #2
    movge r1, #13
ov006_021e8814_Lbc:
    add r0, r7, #7
    bl native_fn_021e7a88
    cmp r7, r9
    bge ov006_021e8814_Le4
    ldr r3, [r4, #0x48]
    mov r1, r8
    mov r2, r10
    add r0, r7, #7
    blx r3
    b ov006_021e8814_Lec
ov006_021e8814_Le4:
    add r0, r7, #7
    bl native_fn_021e75ec
ov006_021e8814_Lec:
    add r0, r7, #7
    bl native_fn_021e7b00
    add r7, r7, #1
    cmp r7, #6
    add r8, r8, #1
    blt ov006_021e8814_La4
    cmp r5, #0
    ldreq r0, =0x02218f38
    ldreq r1, [r0, #0x7c]
    biceq r1, r1, #2
    beq ov006_021e8814_L124
    ldr r0, =0x02218f38
    ldr r1, [r0, #0x7c]
    orr r1, r1, #2
ov006_021e8814_L124:
    str r1, [r0, #0x7c]
    ldr r0, [sp]
    cmp r0, #6
    ldrle r0, =0x02218ea8
    ldrle r1, [r0, #0x7c]
    bicle r1, r1, #2
    ble ov006_021e8814_L14c
    ldr r0, =0x02218ea8
    ldr r1, [r0, #0x7c]
    orr r1, r1, #2
ov006_021e8814_L14c:
    str r1, [r0, #0x7c]
    mvn r0, #0
    mov r1, #86
    bl native_fn_0205e7a8
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov006_021e8814_L164:
    smull r0, r5, r1, r4
    add r5, r5, r4, lsr #31
    smull r0, r1, r2, r5
    sub r5, r4, r0
    add r0, r5, #7
    mov r1, #1
    bl native_fn_021e7a88
    ldr r1, =0x2aaaaaab
    mov r2, #6
    smull r0, r4, r1, r7
    add r4, r4, r7, lsr #31
    smull r0, r1, r2, r4
    sub r4, r7, r0
    add r0, r4, #7
    mov r1, #2
    bl native_fn_021e7a88
    add r0, r5, #7
    bl native_fn_021e7b00
    add r0, r4, #7
    bl native_fn_021e7b00
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
