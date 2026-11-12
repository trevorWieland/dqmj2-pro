/* ov001 row 0x021dab28: 424 bytes.
 *
 * What it does: 106 instructions; 15 call(s) to 0x021d8dec, 0x022094bc, 0x021dabf0, +12 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 15 calls (106 instructions, 15 calls, 12 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0xdc
 *   branch +0x50 -> +0xc8
 *   branch +0x68 -> +0x178
 *   branch +0x74 -> +0x84
 *   branch +0x80 -> +0x88
 *   branch +0x9c -> +0xac
 *   branch +0xc4 -> +0x178
 *   branch +0xd8 -> +0x178
 *   branch +0xe0 -> +0x178
 *   branch +0x110 -> +0x15c
 *   branch +0x11c -> +0x12c
 *   branch +0x128 -> +0x130
 *   branch +0x144 -> +0x158
 *   back edge +0x174 -> +0xf4
 *   test +0x4c cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x8c tst r0, #1
 *   test +0x98 cmp r0, #0
 *   test +0xdc cmp r9, #54
 *   test +0x10c cmp r1, #0
 *   test +0x118 cmp r0, #0
 *   test +0x124 cmp r0, #0
 *   test +0x134 tst r0, #1
 *   test +0x140 cmp r0, #0
 *   test +0x170 cmp r6, #4
 *   test +0x184 tst r0, #64
 *   test +0x194 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dab28; the literal pool and
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

extern void native_fn_021d8dec(void);
extern void native_fn_022094bc(void);
extern void native_fn_021daa90(void);
extern void native_fn_0205d7cc(void);
extern void native_fn_0205d718(void);
extern void native_fn_022048fc(void);
extern void native_fn_021daae0(void);


asm u32 native_ov001_021dab28 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r9, r1
    mov r10, r0
    mov r0, r9
    bl native_fn_021d8dec
    add r1, r10, #158
    add r2, r10, r9
    add r6, r1, #768
    add r2, r2, #512
    mov r5, r0
    ldrsb r1, [r6, r9]
    ldrsb r2, [r2, #104]
    mov r0, r9
    bl native_fn_022094bc
    movs r7, r0
    bmi ov001_021dab28_Ldc
    add r0, r10, #218
    add r4, r0, #768
    ldrsb r0, [r4, r7]
    cmp r0, #0
    ble ov001_021dab28_Lc8
    mov r2, r7
    add r0, r10, #556
    add r1, r10, #616
    bl native_fn_021daa90
    cmp r0, #0
    bne ov001_021dab28_L178
    ldrsb r0, [r6, r9]
    cmp r0, #0
    bgt ov001_021dab28_L84
    ldrsh r0, [r5, #10]
    cmp r0, #0
    bne ov001_021dab28_L88
ov001_021dab28_L84:
    ldrsh r0, [r5, #4]
ov001_021dab28_L88:
    bl native_fn_0205d7cc
    tst r0, #1
    movne r0, #1
    moveq r0, #0
    cmp r0, #0
    beq ov001_021dab28_Lac
    ldrsb r0, [r4, r7]
    sub r0, r0, #1
    bl native_fn_0205d718
ov001_021dab28_Lac:
    mov r0, #0
    strb r0, [r4, r7]
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r7
    bl native_fn_022048fc
    b ov001_021dab28_L178
ov001_021dab28_Lc8:
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r7
    bl native_fn_022048fc
    b ov001_021dab28_L178
ov001_021dab28_Ldc:
    cmp r9, #54
    bne ov001_021dab28_L178
    add r0, r10, r9
    mov r6, #0
    add r4, r0, #768
    mov r11, r6
ov001_021dab28_Lf4:
    add r0, r6, #15
    mov r0, r0, lsl #24
    add r7, r10, r0, asr #24
    add r1, r7, #768
    ldrsb r1, [r1, #218]
    mov r8, r0, asr #24
    cmp r1, #0
    ble ov001_021dab28_L15c
    ldrsb r0, [r4, #158]
    cmp r0, #0
    bgt ov001_021dab28_L12c
    ldrsh r0, [r5, #10]
    cmp r0, #0
    bne ov001_021dab28_L130
ov001_021dab28_L12c:
    ldrsh r0, [r5, #4]
ov001_021dab28_L130:
    bl native_fn_0205d7cc
    tst r0, #1
    movne r0, #1
    moveq r0, #0
    cmp r0, #0
    beq ov001_021dab28_L158
    add r0, r7, #768
    ldrsb r0, [r0, #218]
    sub r0, r0, #1
    bl native_fn_0205d718
ov001_021dab28_L158:
    strb r11, [r7, #0x3da]
ov001_021dab28_L15c:
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r8
    bl native_fn_022048fc
    add r6, r6, #1
    cmp r6, #4
    blt ov001_021dab28_Lf4
ov001_021dab28_L178:
    mov r0, r9
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #64
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r0, r10, #556
    bl native_fn_021daae0
    cmp r0, #0
    ldreqb r0, [r10, #0x35d]
    biceq r0, r0, #2
    streqb r0, [r10, #0x35d]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
