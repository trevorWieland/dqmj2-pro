/* ov001 row 0x022154d8: 568 bytes.
 *
 * What it does: 139 instructions; 22 call(s) to 0x0202ac08, 0x021eea10, 0x021d7f54, +19 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 22 calls (139 instructions, 22 calls, 16 branches, 22 back edges, 3 literal slots).
 *
 *   pool +0x22c -> constant 0x02242ba0 (image word 0x02242ba0)
 *   pool +0x230 -> constant 0x02242bb4 (image word 0x02242bb4)
 *   pool +0x234 -> constant 0x02242be4 (image word 0x02242be4)
 *   branch +0x10 -> +0x40
 *   branch +0x3c -> +0x224
 *   branch +0x44 -> +0xec
 *   branch +0x9c -> +0xb8
 *   back edge +0xc4 -> +0x84
 *   branch +0xe8 -> +0x224
 *   branch +0xf0 -> +0x114
 *   branch +0x110 -> +0x224
 *   branch +0x118 -> +0x190
 *   branch +0x13c -> +0x168
 *   back edge +0x174 -> +0x134
 *   branch +0x18c -> +0x224
 *   branch +0x194 -> +0x1b8
 *   branch +0x1b4 -> +0x224
 *   branch +0x1bc -> +0x1d4
 *   branch +0x1d0 -> +0x224
 *   branch +0x1d8 -> +0x224
 *   branch +0x1e4 -> +0x224
 *   test +0x0c cmp r1, #0
 *   test +0x40 cmp r1, #5
 *   test +0x98 cmp r0, #0
 *   test +0xbc cmp r8, #3
 *   test +0xec cmp r1, #10
 *   test +0x100 cmp r1, #30
 *   test +0x114 cmp r1, #20
 *   test +0x138 cmp r0, #0
 *   test +0x16c cmp r5, #3
 *   test +0x190 cmp r1, #30
 *   test +0x1a4 cmp r1, #40
 *   test +0x1b8 cmp r1, #40
 *   test +0x1d4 cmp r1, #100
 *   test +0x1e0 cmp r0, #0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022154d8; the literal pool and
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

extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_021d7f54(void);
extern void native_fn_02041898(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f1414(void);
extern void native_fn_021f1438(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_022025a4(void);
extern void native_fn_021f949c(void);
extern void native_fn_0205c904(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021f14a4(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_0203d0d8(void);
extern void native_fn_021e6720(void);


asm u32 native_ov001_022154d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r0, =0x02242ba0
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov001_022154d8_L40
    ldr r0, =0x02242bb4
    bl native_fn_0202ac08
    mov r0, #240
    mov r1, #0
    bl native_fn_021eea10
    mov r0, #1
    bl native_fn_021d7f54
    ldr r0, =0x02242ba0
    mov r1, #5
    strb r1, [r0, #0x1]
    b ov001_022154d8_L224
ov001_022154d8_L40:
    cmp r1, #5
    bne ov001_022154d8_Lec
    mov r0, #0
    bl native_fn_02041898
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #21
    bl native_fn_021f1354
    mov r0, #1
    bl native_fn_021f1414
    bl native_fn_021f1438
    mov r5, #1
    ldr r9, =0x02242be4
    mov r8, #0
    mov r4, r5
    mov r7, r5
ov001_022154d8_L84:
    mov r0, r7
    mov r1, r8
    bl native_fn_021db438
    mov r6, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022154d8_Lb8
    mov r0, r5
    mov r1, r8
    mov r2, r5
    strb r5, [r6, #0x325]
    bl native_fn_022025a4
    strb r4, [r9]
ov001_022154d8_Lb8:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #1
    blt ov001_022154d8_L84
    mov r0, #222
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x02242ba0
    mov r1, #10
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_022154d8_L224
ov001_022154d8_Lec:
    cmp r1, #10
    bne ov001_022154d8_L114
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0]
    movhs r1, #20
    strhsb r1, [r0, #0x1]
    b ov001_022154d8_L224
ov001_022154d8_L114:
    cmp r1, #20
    bne ov001_022154d8_L190
    mov r10, #1
    mov r8, #240
    ldr r4, =0x02242be4
    mov r5, #0
    mov r7, r8
    mov r6, r10
ov001_022154d8_L134:
    ldrb r0, [r4]
    cmp r0, #0
    beq ov001_022154d8_L168
    mov r0, r10
    mov r1, r5
    bl native_fn_021db438
    mov r9, r0
    mov r0, r8
    bl native_fn_0205c904
    mov r0, r7
    mov r1, r9
    mov r2, r6
    bl native_fn_021eec7c
ov001_022154d8_L168:
    add r5, r5, #1
    cmp r5, #3
    add r4, r4, #1
    blt ov001_022154d8_L134
    ldr r0, =0x02242ba0
    mov r1, #30
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    b ov001_022154d8_L224
ov001_022154d8_L190:
    cmp r1, #30
    bne ov001_022154d8_L1b8
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #40
    strb r2, [r0]
    movhs r1, #40
    strhsb r1, [r0, #0x1]
    b ov001_022154d8_L224
ov001_022154d8_L1b8:
    cmp r1, #40
    bne ov001_022154d8_L1d4
    bl native_fn_021f14a4
    ldr r0, =0x02242ba0
    mov r1, #100
    strb r1, [r0, #0x1]
    b ov001_022154d8_L224
ov001_022154d8_L1d4:
    cmp r1, #100
    bne ov001_022154d8_L224
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_022154d8_L224
    mov r0, #240
    bl native_fn_021eeb70
    ldr r0, =0x02242bb4
    bl native_fn_0202ac4c
    mov r0, #3
    mov r1, #1
    bl native_fn_0203d0d8
    ldr r0, =0x02242be4
    bl native_fn_021e6720
    ldr r1, =0x02242ba0
    mov r0, #0
    strb r0, [r1, #0x1]
    mov r0, #1
    str r0, [r1, #0x8]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_022154d8_L224:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
