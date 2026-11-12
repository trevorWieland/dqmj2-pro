/* ov006 row 0x021e81e8: 1580 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x604 -> constant 0x02218d90 (image word 0x02218d90)
 *   pool +0x608 -> native_fn_021e8130 (image word 0x021e8130)
 *   pool +0x60c -> native_fn_021e819c (image word 0x021e819c)
 *   pool +0x610 -> native_data_02207dc4 (image word 0x02207dc4)
 *   pool +0x614 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x618 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x61c -> constant 0x02218e18 (image word 0x02218e18)
 *   pool +0x620 -> constant 0x02218e60 (image word 0x02218e60)
 *   pool +0x624 -> constant 0x02218f38 (image word 0x02218f38)
 *   pool +0x628 -> constant 0x02218ea8 (image word 0x02218ea8)
 *   branch +0x94 -> +0x134
 *   back edge +0x130 -> +0x9c
 *   branch +0x13c -> +0x1a8
 *   branch +0x1e4 -> +0x1f4
 *   branch +0x1f8 -> +0x210
 *   branch +0x20c -> +0x214
 *   branch +0x24c -> +0x274
 *   branch +0x27c -> +0x320
 *   branch +0x2bc -> +0x2f8
 *   branch +0x2f4 -> +0x30c
 *   back edge +0x31c -> +0x284
 *   branch +0x328 -> +0x3ec
 *   test +0x38 cmp r8, #0
 *   test +0x68 cmp r3, #0
 *   test +0x78 cmp r1, #0
 *   test +0x88 cmp r10, #0
 *   test +0x9c cmp r5, #0
 *   test +0xa8 cmp r5, #0
 *   test +0xb8 cmp r5, #0
 *   test +0x12c cmp r5, r10
 *   test +0x138 cmp r0, #0
 *   test +0x1e0 cmp r0, #0
 *   test +0x1e8 cmp r0, r8
 *   test +0x200 cmp r0, #0
 *   test +0x238 cmp r8, #6
 *   test +0x248 cmp r9, #0
 *   test +0x274 cmp r9, #0
 *   test +0x2b8 cmp r5, r8
 *   test +0x2c4 cmp r5, r0
 *   test +0x314 cmp r4, r9
 *   test +0x324 cmp r0, #0
 *   test +0x3fc cmp r0, #0
 *   test +0x5d0 cmp r0, #6
 *   test +0x5e0 cmp r1, r8
 *   1 block transfer(s), 53 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e81e8; the literal pool and
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

extern void native_fn_021e6b6c(void);
extern void native_fn_021e8130(void);
extern void native_fn_021e819c(void);
extern void native_fn_021e73ac(void);
extern void native_fn_021e7b8c(void);
extern void native_fn_021e791c(void);
extern u8 native_data_02207dc4[];
extern void native_fn_021e7ab0(void);
extern void native_fn_021e7a88(void);
extern void native_fn_021e7b00(void);
extern void native_fn_02008be0(void);
extern void native_fn_021e6530(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087720(void);
extern void native_fn_021e80c4(void);
extern void native_fn_02008c58(void);
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0204b85c(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_020485c8(void);
extern void native_fn_0204b1b0(void);
extern void native_fn_02048644(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048f5c(void);
extern void native_fn_02048a9c(void);
extern void native_fn_02048a94(void);


asm u32 native_ov006_021e81e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #160
    mov r9, r1
    ldr r1, [sp, #0xc8]
    ldr r4, =0x02218d90
    str r1, [sp, #0xc8]
    ldr r1, [sp, #0xcc]
    mov r10, r0
    mov r8, r2
    mov r0, #0
    str r3, [sp, #0x10]
    str r1, [sp, #0xcc]
    ldr r4, [r4, #0x80]
    bl native_fn_021e6b6c
    cmp r8, #0
    movne r1, #0
    ldr r0, =0x02218d90
    moveq r1, #3
    str r1, [r0, #0x64]
    str r1, [r0, #0x14]
    mov r2, #0
    ldr r3, [sp, #0xd4]
    str r2, [r0, #0x20]
    mov r1, #1
    str r1, [r0, #0x10]
    str r2, [r0, #0x4]
    cmp r3, #0
    ldreq r3, =native_fn_021e8130
    ldr r1, [sp, #0xd8]
    ldr r0, =0x02218d90
    cmp r1, #0
    str r3, [r0, #0x48]
    ldreq r1, =native_fn_021e819c
    ldr r0, =0x02218d90
    cmp r10, #0
    str r1, [r0, #0x50]
    mov r5, #0
    ble ov006_021e81e8_L134
    mov r6, #1
ov006_021e81e8_L9c:
    cmp r5, #0
    movne r1, #3
    moveq r1, #15
    cmp r5, #0
    movne r2, r5
    moveq r2, #1
    rsb r11, r2, #31
    cmp r5, #0
    movne r7, #2
    str r11, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, r5
    mov r3, r6
    moveq r7, #1
    str r4, [sp, #0xc]
    bl native_fn_021e73ac
    mov r4, r0
    mov r0, r5
    bl native_fn_021e7b8c
    sub r0, r11, #1
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r2, r7
    mov r0, r5
    mov r1, r9
    mov r3, #0
    bl native_fn_021e791c
    add r5, r5, #1
    add r6, r6, #2
    add r9, r9, #4
    cmp r5, r10
    blt ov006_021e81e8_L9c
ov006_021e81e8_L134:
    ldr r0, [sp, #0xd0]
    cmp r0, #0
    beq ov006_021e81e8_L1a8
    mov r0, #10
    str r0, [sp]
    mov r1, #2
    mov r0, #4
    str r1, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    mov r1, r0
    mov r2, #22
    mov r3, #1
    str r4, [sp, #0xc]
    bl native_fn_021e73ac
    mov r4, r0
    mov r0, #4
    bl native_fn_021e7b8c
    mov r0, #6
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    mov r0, #4
    ldr r1, =native_data_02207dc4
    mov r2, #3
    mov r3, #0
    bl native_fn_021e791c
ov006_021e81e8_L1a8:
    mov r0, #28
    str r0, [sp]
    mov r2, #2
    str r2, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #5
    mov r1, #3
    mov r3, #21
    str r4, [sp, #0xc]
    bl native_fn_021e73ac
    ldr r1, =0x02218d90
    mov r7, r0
    ldr r0, [r1, #0x5c]
    cmp r0, #0
    bge ov006_021e81e8_L1f4
    cmp r0, r8
    movge r0, #0
    strge r0, [r1, #0x5c]
ov006_021e81e8_L1f4:
    subs r0, r10, #1
    beq ov006_021e81e8_L210
    ldr r0, [sp, #0xcc]
    cmp r0, #0
    movne r1, #3
    moveq r1, #1
    b ov006_021e81e8_L214
ov006_021e81e8_L210:
    mov r1, #2
ov006_021e81e8_L214:
    mov r0, r10, lsl #1
    str r0, [sp, #0x14]
    ldr r0, =0x02218d90
    add r6, r1, r10, lsl #1
    ldr r1, =0x2aaaaaab
    ldr r3, [r0, #0x5c]
    mov r2, #6
    smull r0, r4, r1, r3
    add r4, r4, r3, lsr #31
    cmp r8, #6
    movhi r9, #6
    movls r9, r8
    mul r5, r4, r2
    cmp r9, #0
    beq ov006_021e81e8_L274
    mov r0, r9, lsl #1
    add r1, r0, #2
    ldr r0, [sp, #0xc8]
    str r1, [sp]
    add r3, r0, #2
    mov r2, r6
    mov r0, #0
    mov r1, #1
    bl native_fn_021e7ab0
ov006_021e81e8_L274:
    cmp r9, #0
    mov r4, #0
    ble ov006_021e81e8_L320
    ldr r11, =0x02218d90
ov006_021e81e8_L284:
    ldr r0, [sp, #0xc8]
    mov r1, #2
    str r0, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    add r0, r4, #7
    mov r2, r1
    add r3, r6, #1
    str r7, [sp, #0xc]
    bl native_fn_021e73ac
    mov r7, r0
    cmp r5, r8
    bhs ov006_021e81e8_L2f8
    ldr r0, [r11, #0x5c]
    cmp r5, r0
    moveq r1, #1
    movne r1, #2
    add r0, r4, #7
    bl native_fn_021e7a88
    ldr r2, [sp, #0x10]
    ldr r3, [r11, #0x48]
    add r0, r4, #7
    mov r1, r5
    blx r3
    add r0, r4, #7
    bl native_fn_021e7b00
    b ov006_021e81e8_L30c
ov006_021e81e8_L2f8:
    add r0, r4, #7
    mov r1, #13
    bl native_fn_021e7a88
    add r0, r4, #7
    bl native_fn_021e7b00
ov006_021e81e8_L30c:
    add r6, r6, #2
    add r4, r4, #1
    cmp r4, r9
    add r5, r5, #1
    blt ov006_021e81e8_L284
ov006_021e81e8_L320:
    ldr r0, [sp, #0xcc]
    cmp r0, #0
    beq ov006_021e81e8_L3ec
    add r1, sp, #32
    mov r0, #0
    mov r2, #128
    bl native_fn_02008be0
    ldr r0, [sp, #0xcc]
    bl native_fn_021e6530
    add r2, sp, #32
    mov r1, r0
    str r2, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    mov r2, #64
    mov r3, #0
    bl native_fn_02046af4
    ldr r0, =0x021c9698
    add r1, sp, #32
    mov r2, #64
    bl native_fn_02087720
    mov r0, r0, lsr #3
    add r4, r0, #4
    subs r0, r10, #1
    add r0, r4, #1
    rsb r2, r0, #32
    ldrne r0, [sp, #0x14]
    str r4, [sp]
    addne r3, r0, #2
    mov r0, #2
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    moveq r3, #3
    mov r0, #6
    mov r1, #3
    str r7, [sp, #0xc]
    bl native_fn_021e73ac
    mov r0, #6
    bl native_fn_021e7b8c
    mov r2, #0
    str r4, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    ldr r1, [sp, #0xcc]
    mov r0, #6
    mov r3, r2
    bl native_fn_021e791c
ov006_021e81e8_L3ec:
    ldr r0, =0x02218d90
    add r1, sp, #28
    ldr r0, [r0, #0x5c]
    bl native_fn_021e80c4
    cmp r0, #0
    movne r5, #1
    ldr r1, =0x02218e18
    mov r0, #0
    mov r2, #72
    moveq r5, #0
    bl native_fn_02008c58
    ldr r0, [sp, #0xc8]
    mov r3, #2
    mov r2, r0, lsl #3
    ldr r0, =0x02218e18
    add r1, sp, #28
    str r3, [sp]
    mov r4, #36
    and r2, r2, #255
    str r4, [sp, #0x4]
    bl native_fn_0204b4f4
    ldr r0, =0x02218e18
    mov r1, r5
    bl native_fn_0204b61c
    add r1, sp, #24
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    ldr r1, =0x02218e60
    mov r2, #72
    bl native_fn_02008c58
    mov r1, #0
    str r1, [sp]
    mov r0, #51
    stmib sp, {r0, r1}
    ldr r0, =0x02218e60
    add r1, sp, #24
    mov r2, #8
    mov r3, #1
    bl native_fn_0204b85c
    ldr r0, =0x02218e60
    mov r1, #0
    bl native_fn_0205fa4c
    ldr r1, =0x02218f38
    mov r0, #0
    mov r2, #144
    bl native_fn_02008c58
    ldr r1, =0x02218ea8
    mov r0, #0
    mov r2, #144
    bl native_fn_02008c58
    ldr r1, =0x02218f38
    mov r0, #1
    bl native_fn_020485c8
    ldr r1, =0x02218ea8
    mov r0, #1
    bl native_fn_020485c8
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =0x02218f38
    mov r2, #21
    bl native_fn_02048644
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =0x02218ea8
    mov r2, #22
    bl native_fn_02048644
    subs r0, r10, #1
    ldr r0, [sp, #0xc8]
    movne r2, #1
    add r1, r0, #2
    ldr r0, [sp, #0x14]
    moveq r2, #2
    add r0, r0, r2
    add r2, r0, #1
    mov r4, r1, lsl #3
    ldr r0, =0x02218f38
    mov r1, r4
    mov r2, r2, lsl #3
    bl native_fn_02048a60
    subs r0, r10, #1
    movne r1, #1
    ldr r0, [sp, #0x14]
    moveq r1, #2
    add r0, r0, r1
    add r2, r0, #12
    ldr r0, =0x02218ea8
    mov r1, r4
    mov r2, r2, lsl #3
    bl native_fn_02048a60
    mov r0, #1
    bl native_fn_02048f5c
    mov r1, r0
    ldr r0, =0x02218f38
    bl native_fn_02048a9c
    mov r0, #1
    bl native_fn_02048f5c
    mov r1, r0
    ldr r0, =0x02218ea8
    bl native_fn_02048a9c
    ldr r0, =0x02218f38
    mov r1, #1
    bl native_fn_02048a94
    ldr r0, =0x02218ea8
    mov r1, #1
    bl native_fn_02048a94
    ldr r3, =0x02218f38
    ldr r2, =0x02218ea8
    ldr r1, [r3, #0x7c]
    ldr r0, =0x02218d90
    bic r6, r1, #2
    str r6, [r3, #0x7c]
    ldr r4, [r2, #0x7c]
    ldr r1, =0x2aaaaaab
    bic r4, r4, #2
    str r4, [r2, #0x7c]
    ldr r4, [r0, #0x5c]
    mov r2, #6
    smull r0, r5, r1, r4
    add r5, r5, r4, lsr #31
    mul r0, r5, r2
    cmp r0, #6
    add r1, r0, #6
    orrge r0, r6, #2
    strge r0, [r3, #0x7c]
    cmp r1, r8
    addhs sp, sp, #160
    ldmhsia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, =0x02218ea8
    ldr r1, [r0, #0x7c]
    orr r1, r1, #2
    str r1, [r0, #0x7c]
    add sp, sp, #160
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
