/* ov000 row 0x0221bd3c: 348 bytes.
 *
 * What it does: 85 instructions; 18 call(s) to 0x020c1540, 0x0206a0fc, 0x0206bf44, +15 more; loops (back edge at +0x18); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x154 -> constant 0x022460d4 (image word 0x022460d4)
 *   pool +0x158 -> constant 0x02246090 (image word 0x02246090)
 *   branch +0x3c -> +0x7c
 *   branch +0x78 -> +0xf0
 *   branch +0x84 -> +0x98
 *   branch +0x94 -> +0xf0
 *   branch +0xa0 -> +0xf0
 *   branch +0xf8 -> +0x108
 *   branch +0x104 -> +0x110
 *   branch +0x10c -> +0x114
 *   branch +0x124 -> +0x130
 *   branch +0x12c -> +0x140
 *   branch +0x134 -> +0x148
 *   branch +0x13c -> +0x148
 *   test +0x10 cmp r0, #10
 *   test +0x20 tst r0, #255
 *   test +0x38 cmp r1, #1
 *   test +0x80 cmp r0, #2
 *   test +0x9c cmp r0, #1
 *   test +0xf4 cmp r0, #0
 *   test +0x100 cmp r0, #0
 *   test +0x120 cmp r0, #0
 *   test +0x128 cmp r4, #0
 *   test +0x130 cmp r0, #0
 *   test +0x138 cmp r4, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221bd3c; the literal pool and
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

extern void native_fn_020c1540(void);
extern void native_fn_0206a0fc(void);
extern void native_fn_0206bf44(void);
extern void native_fn_021ead88(void);
extern void native_fn_021eb030(void);
extern void native_fn_02041538(void);
extern void native_fn_0206a49c(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);
extern void native_fn_02068f60(void);
extern void native_fn_0221e6cc(void);
extern void native_fn_0206c0b0(void);
extern void native_fn_0206c0e0(void);
extern void native_fn_0221c000(void);


asm u32 native_ov000_0221bd3c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x022460d4
    mov r4, r0
    ldrsb r0, [r1, #16]
    cmp r0, #10
    ldmneia sp!, {r4, pc}
    bl native_fn_020c1540
    strb r0, [r4]
    tst r0, #255
    ldmneia sp!, {r4, pc}
    mov r0, #1
    bl native_fn_0206a0fc
    and r1, r0, #255
    strb r0, [r4]
    cmp r1, #1
    bne ov000_0221bd3c_L7c
    bl native_fn_0206bf44
    mov r0, #0
    mov r1, r0
    bl native_fn_021ead88
    bl native_fn_021eb030
    ldr r3, =0x02246090
    mov r0, #11
    strb r0, [r3, #0x3]
    mov r12, #7
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r12, [r3, #0x7]
    bl native_fn_02041538
    b ov000_0221bd3c_Lf0
ov000_0221bd3c_L7c:
    bl native_fn_0206a49c
    cmp r0, #2
    bne ov000_0221bd3c_L98
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    b ov000_0221bd3c_Lf0
ov000_0221bd3c_L98:
    bl native_fn_0206a49c
    cmp r0, #1
    bne ov000_0221bd3c_Lf0
    bl native_fn_020c48bc
    mov r0, #5
    mov r1, #6
    mov r2, #42
    bl native_fn_020c48d0
    mvn r0, #0
    bl native_fn_020c48e8
    mov r0, #0
    bl native_fn_02068f60
    ldr r1, =0x02246090
    ldr r0, =0x022460d4
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    ldr r0, =0x02246090
    mov r1, #5
    strb r1, [r0, #0x7]
ov000_0221bd3c_Lf0:
    bl native_fn_0206c0b0
    cmp r0, #0
    bne ov000_0221bd3c_L108
    bl native_fn_0206c0e0
    cmp r0, #0
    beq ov000_0221bd3c_L110
ov000_0221bd3c_L108:
    mov r1, #1
    b ov000_0221bd3c_L114
ov000_0221bd3c_L110:
    mov r1, #0
ov000_0221bd3c_L114:
    ldr r0, =0x02246090
    and r4, r1, #255
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    bne ov000_0221bd3c_L130
    cmp r4, #0
    bne ov000_0221bd3c_L140
ov000_0221bd3c_L130:
    cmp r0, #0
    beq ov000_0221bd3c_L148
    cmp r4, #0
    bne ov000_0221bd3c_L148
ov000_0221bd3c_L140:
    mov r0, #1
    bl native_fn_0221c000
ov000_0221bd3c_L148:
    ldr r0, =0x02246090
    strb r4, [r0, #0x2]
    ldmia sp!, {r4, pc}
}
