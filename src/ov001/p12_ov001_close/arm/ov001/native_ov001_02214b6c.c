/* ov001 row 0x02214b6c: 584 bytes.
 *
 * What it does: 145 instructions; 16 call(s) to 0x0207afec, 0x021f1f1c, 0x02214a14, +13 more; loops (back edge at +0x0c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 16 calls (145 instructions, 16 calls, 28 branches, 15 back edges, 1 literal slot).
 *
 *   pool +0x244 -> constant 0x02242b94 (image word 0x02242b94)
 *   branch +0x1c -> +0x34
 *   branch +0x30 -> +0x23c
 *   branch +0x38 -> +0x58
 *   branch +0x54 -> +0x23c
 *   branch +0x5c -> +0x80
 *   branch +0x7c -> +0x23c
 *   branch +0x84 -> +0xbc
 *   branch +0x98 -> +0xac
 *   branch +0xa8 -> +0x23c
 *   branch +0xb8 -> +0x23c
 *   branch +0xc0 -> +0xe8
 *   branch +0xd4 -> +0x23c
 *   branch +0xe4 -> +0x23c
 *   branch +0xec -> +0x128
 *   branch +0xfc -> +0x118
 *   branch +0x114 -> +0x23c
 *   branch +0x124 -> +0x23c
 *   branch +0x12c -> +0x158
 *   branch +0x154 -> +0x23c
 *   branch +0x15c -> +0x17c
 *   branch +0x168 -> +0x23c
 *   branch +0x178 -> +0x23c
 *   branch +0x180 -> +0x1e4
 *   branch +0x190 -> +0x1d4
 *   branch +0x1d0 -> +0x23c
 *   branch +0x1e0 -> +0x23c
 *   branch +0x1e8 -> +0x218
 *   branch +0x200 -> +0x23c
 *   branch +0x214 -> +0x23c
 *   test +0x18 cmp r2, #0
 *   test +0x34 cmp r2, #10
 *   test +0x58 cmp r2, #20
 *   test +0x70 cmp r0, #30
 *   test +0x80 cmp r2, #30
 *   test +0x94 cmp r0, #0
 *   test +0xbc cmp r2, #40
 *   test +0xd0 cmp r0, #0
 *   test +0xe8 cmp r2, #50
 *   test +0xf8 cmp r0, #0
 *   test +0x128 cmp r2, #60
 *   test +0x158 cmp r2, #70
 *   test +0x164 cmp r0, #1
 *   test +0x17c cmp r2, #80
 *   test +0x18c cmp r0, #0
 *   test +0x1e4 cmp r2, #90
 *   test +0x1fc cmp r0, #60
 *   0 block transfer(s), 21 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214b6c; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021f1f1c(void);
extern void native_fn_02214a14(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_021db8b8(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041510(void);
extern void native_fn_02041800(void);
extern void native_fn_02063b40(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f1414(void);
extern void native_fn_021f1438(void);
extern void native_fn_021f14a4(void);


asm u32 native_ov001_02214b6c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242b94
    ldrh r0, [r0, #4]
    bl native_fn_0207afec
    ldr r1, =0x02242b94
    ldrsb r2, [r1]
    cmp r2, #0
    bne ov001_02214b6c_L34
    bl native_fn_021f1f1c
    ldr r0, =0x02242b94
    mov r1, #10
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L34:
    cmp r2, #10
    bne ov001_02214b6c_L58
    bl native_fn_02214a14
    ldr r0, =0x02242b94
    mov r1, #20
    strb r1, [r0]
    mov r1, #0
    strb r1, [r0, #0x2]
    b ov001_02214b6c_L23c
ov001_02214b6c_L58:
    cmp r2, #20
    bne ov001_02214b6c_L80
    ldrsb r0, [r1, #2]
    add r0, r0, #1
    strb r0, [r1, #0x2]
    ldrsb r0, [r1, #2]
    cmp r0, #30
    movgt r0, #30
    strgtb r0, [r1]
    b ov001_02214b6c_L23c
ov001_02214b6c_L80:
    cmp r2, #30
    bne ov001_02214b6c_Lbc
    mov r0, #0
    mov r1, r0
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_02214b6c_Lac
    ldr r0, =0x02242b94
    mov r1, #40
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_Lac:
    ldr r0, =0x02242b94
    mov r1, #60
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_Lbc:
    cmp r2, #40
    bne ov001_02214b6c_Le8
    ldr r0, [r1, #0x8]
    mov r1, #0
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_02214b6c_L23c
    ldr r0, =0x02242b94
    mov r1, #50
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_Le8:
    cmp r2, #50
    bne ov001_02214b6c_L128
    mov r0, #0
    bl native_fn_021db8b8
    cmp r0, #0
    beq ov001_02214b6c_L118
    ldr r0, =0x02242b94
    mov r1, #0
    strb r1, [r0]
    mov r1, #4
    strb r1, [r0, #0x3]
    b ov001_02214b6c_L23c
ov001_02214b6c_L118:
    ldr r0, =0x02242b94
    mov r1, #60
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L128:
    cmp r2, #60
    bne ov001_02214b6c_L158
    mov r0, #1
    bl native_fn_020414b0
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r0, =0x02242b94
    mov r1, #70
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L158:
    cmp r2, #70
    bne ov001_02214b6c_L17c
    bl native_fn_02041800
    cmp r0, #1
    beq ov001_02214b6c_L23c
    ldr r0, =0x02242b94
    mov r1, #80
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L17c:
    cmp r2, #80
    bne ov001_02214b6c_L1e4
    mov r0, #65
    bl native_fn_02063b40
    cmp r0, #0
    bne ov001_02214b6c_L1d4
    mov r0, #1
    mov r3, r0
    mov r1, #0
    mov r2, #18
    bl native_fn_021f1354
    ldr r0, =0x02242b94
    ldr r0, [r0, #0x8]
    ldrb r0, [r0, #0x31e]
    bl native_fn_021f1414
    bl native_fn_021f1438
    ldr r0, =0x02242b94
    mov r1, #90
    strb r1, [r0]
    mov r1, #0
    strb r1, [r0, #0x2]
    b ov001_02214b6c_L23c
ov001_02214b6c_L1d4:
    ldr r0, =0x02242b94
    mov r1, #100
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L1e4:
    cmp r2, #90
    bne ov001_02214b6c_L218
    ldrsb r0, [r1, #2]
    add r0, r0, #1
    strb r0, [r1, #0x2]
    ldrsb r0, [r1, #2]
    cmp r0, #60
    blt ov001_02214b6c_L23c
    bl native_fn_021f14a4
    ldr r0, =0x02242b94
    mov r1, #100
    strb r1, [r0]
    b ov001_02214b6c_L23c
ov001_02214b6c_L218:
    mov r0, #63
    bl native_fn_020414b0
    ldr r0, =0x02242b94
    mov r1, #1
    strb r1, [r0, #0x1]
    mov r1, #0
    strb r1, [r0]
    mov r1, #4
    strb r1, [r0, #0x3]
ov001_02214b6c_L23c:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
