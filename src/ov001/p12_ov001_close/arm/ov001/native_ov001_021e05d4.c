/* ov001 row 0x021e05d4: 336 bytes.
 *
 * What it does: 83 instructions; 13 call(s) to 0x0220b70c, 0x021de590, 0x0204448c, +10 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (83 instructions, 13 calls, 13 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x14c -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x10 -> +0x48
 *   branch +0x24 -> +0x38
 *   branch +0x34 -> +0x48
 *   branch +0x54 -> +0x6c
 *   branch +0x78 -> +0x144
 *   branch +0x8c -> +0x114
 *   branch +0x9c -> +0x114
 *   branch +0xac -> +0x114
 *   branch +0xbc -> +0xd8
 *   branch +0xd4 -> +0xfc
 *   branch +0xdc -> +0xf8
 *   branch +0xf4 -> +0xfc
 *   branch +0x120 -> +0x134
 *   test +0x0c cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x50 cmp r0, #10
 *   test +0x5c cmp r0, #0
 *   test +0x74 cmp r0, #20
 *   test +0x84 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xa4 cmp r0, #0
 *   test +0xb8 cmp r4, #1
 *   test +0xc8 cmp r0, #5
 *   test +0xd8 cmp r4, #2
 *   test +0xe8 cmp r0, #3
 *   test +0x114 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e05d4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0220b70c(void);
extern void native_fn_021de590(void);
extern void native_fn_0204448c(void);
extern void native_fn_02210e08(void);
extern void native_fn_02044424(void);
extern void native_fn_021e0584(void);
extern void native_fn_021e2afc(void);
extern void native_fn_0204447c(void);
extern void native_fn_0203d294(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_0220f354(void);
extern void native_fn_021e66f8(void);


asm u32 native_ov001_021e05d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x022388ec
    ldrb r0, [r0, #0x26]
    cmp r0, #0
    bne ov001_021e05d4_L48
    mov r0, #1
    bl native_fn_0220b70c
    bl native_fn_021de590
    cmp r0, #0
    beq ov001_021e05d4_L38
    ldr r0, =0x022388ec
    mov r1, #31
    strb r1, [r0, #0x8]
    b ov001_021e05d4_L48
ov001_021e05d4_L38:
    bl native_fn_0204448c
    ldr r0, =0x022388ec
    mov r1, #10
    strb r1, [r0, #0x26]
ov001_021e05d4_L48:
    ldr r0, =0x022388ec
    ldrb r0, [r0, #0x26]
    cmp r0, #10
    bne ov001_021e05d4_L6c
    bl native_fn_02210e08
    cmp r0, #0
    ldreq r0, =0x022388ec
    moveq r1, #20
    streqb r1, [r0, #0x26]
ov001_021e05d4_L6c:
    ldr r0, =0x022388ec
    ldrb r0, [r0, #0x26]
    cmp r0, #20
    bne ov001_021e05d4_L144
    mov r0, #16
    bl native_fn_02044424
    cmp r0, #0
    movne r0, #0
    bne ov001_021e05d4_L114
    bl native_fn_021e0584
    cmp r0, #0
    movne r0, #1
    bne ov001_021e05d4_L114
    bl native_fn_021e2afc
    cmp r0, #0
    movne r0, #1
    bne ov001_021e05d4_L114
    bl native_fn_0204447c
    mov r4, r0
    cmp r4, #1
    bgt ov001_021e05d4_Ld8
    mov r0, #8
    bl native_fn_0203d294
    cmp r0, #5
    movlt r5, #1
    movge r5, #0
    b ov001_021e05d4_Lfc
ov001_021e05d4_Ld8:
    cmp r4, #2
    bgt ov001_021e05d4_Lf8
    mov r0, #4
    bl native_fn_0203d294
    cmp r0, #3
    movlt r5, #1
    movge r5, #0
    b ov001_021e05d4_Lfc
ov001_021e05d4_Lf8:
    mov r5, #1
ov001_021e05d4_Lfc:
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    mov r1, r4
    mov r2, r5
    bl native_fn_0220f354
ov001_021e05d4_L114:
    cmp r0, #0
    ldreq r0, =0x022388ec
    moveq r1, #30
    beq ov001_021e05d4_L134
    mov r0, #2
    bl native_fn_021e66f8
    ldr r0, =0x022388ec
    mov r1, #54
ov001_021e05d4_L134:
    strb r1, [r0, #0x8]
    ldr r0, =0x022388ec
    mov r1, #0
    strb r1, [r0, #0x26]
ov001_021e05d4_L144:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
