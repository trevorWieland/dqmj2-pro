/* ov000 row 0x02214344: 488 bytes.
 *
 * What it does: 115 instructions; 21 call(s) to 0x0202ac4c, 0x0202ac08, 0x0202a260, +18 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1cc -> constant 0x02245228 (image word 0x02245228)
 *   pool +0x1d0 -> constant 0x02244f1c (image word 0x02244f1c)
 *   pool +0x1d4 -> constant 0x02244efc (image word 0x02244efc)
 *   pool +0x1d8 -> constant 0x02244f7c (image word 0x02244f7c)
 *   pool +0x1dc -> constant 0x02245128 (image word 0x02245128)
 *   pool +0x1e0 -> constant 0x0000019a (image word 0x0000019a)
 *   pool +0x1e4 -> constant 0x02244f10 (image word 0x02244f10)
 *   back edge +0xa8 -> +0x7c
 *   branch +0xb8 -> +0x1a8
 *   branch +0xcc -> +0x190
 *   branch +0x130 -> +0x140
 *   branch +0x18c -> +0x1bc
 *   branch +0x1a4 -> +0x1bc
 *   test +0x10 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x90 cmp r0, #0
 *   test +0xa0 cmp r7, #5
 *   test +0xb4 cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   test +0x128 cmpne r4, #63
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214344; the literal pool and
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

extern void native_fn_0202ac4c(void);
extern void native_fn_0202ac08(void);
extern void native_fn_0202a260(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_020430b4(void);
extern void native_fn_0204199c(void);
extern void native_fn_02041af0(void);
extern void native_fn_02041ccc(void);
extern void native_fn_02041e50(void);
extern void native_fn_02041f34(void);
extern void native_fn_02041f90(void);
extern void native_fn_02042464(void);
extern void native_fn_02044d14(void);
extern void native_fn_021ea518(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021ea754(void);
extern void native_fn_02211084(void);
extern void native_fn_0202a280(void);


asm u32 native_ov000_02214344 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    ldr r0, =0x02245228
    ldrsh r0, [r0, #226]
    cmp r0, #0
    addle sp, sp, #4
    movle r0, #3
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, pc}
    ldr r0, =0x02244f1c
    bl native_fn_0202ac4c
    ldr r0, =0x02244f1c
    bl native_fn_0202ac08
    bl native_fn_0202a260
    mov r0, #1
    bl native_fn_0202a1e0
    ldr r0, =0x02245228
    ldrsh r4, [r0, #226]
    add r0, r4, #52
    bl native_fn_020430b4
    ldrsh r0, [r0, #2]
    bl native_fn_0204199c
    cmp r0, #0
    ldreq r0, =0x02244efc
    moveq r1, #1
    mov r7, #0
    ldrne r0, =0x02244efc
    movne r1, #0
    ldr r8, =0x02244f7c
    strb r1, [r0, #0x2]
    mov r5, r7
    mov r6, #1
ov000_02214344_L7c:
    add r0, r4, #52
    bl native_fn_020430b4
    add r0, r0, r7, lsl #1
    ldrsh r0, [r0, #4]
    bl native_fn_02041af0
    cmp r0, #0
    streqb r6, [r8]
    strneb r5, [r8]
    add r7, r7, #1
    cmp r7, #5
    add r8, r8, #1
    blt ov000_02214344_L7c
    add r0, r4, #52
    bl native_fn_02041ccc
    cmp r0, #0
    beq ov000_02214344_L1a8
    ldr r0, =0x02245128
    add r1, r4, #52
    bl native_fn_02041e50
    cmp r0, #0
    beq ov000_02214344_L190
    ldr r3, =0x02244efc
    ldr r0, =0x02245128
    ldr r1, [r3, #0x14]
    ldr r2, [r3, #0x18]
    ldr r3, [r3, #0x1c]
    bl native_fn_02041f34
    ldr r1, =0x02244efc
    ldr r0, =0x02245128
    ldr r1, [r1, #0xc]
    mov r2, #0
    bl native_fn_02041f90
    ldr r0, =0x02245228
    ldrsh r0, [r0, #106]
    bl native_fn_020430b4
    ldrsh r1, [r0, #4]
    ldr r0, =0x02245128
    mov r2, #1
    bl native_fn_02042464
    ldr r0, =0x02245228
    ldrsh r0, [r0, #226]
    bl native_fn_02044d14
    movs r4, r0
    cmpne r4, #63
    ldrne r0, =0x0000019a
    bne ov000_02214344_L140
    ldr r0, =0x02245228
    ldrsh r0, [r0, #226]
    bl native_fn_021ea518
ov000_02214344_L140:
    ldr r2, =0x02245128
    ldr r1, =0x02245228
    str r0, [r2, #0x7c]
    str r0, [r2, #0x80]
    str r0, [r2, #0x84]
    ldrsh r0, [r1, #226]
    bl native_fn_02044cdc
    ldr r1, =0x02244efc
    str r4, [sp]
    mov r3, r0
    ldr r0, [r1, #0x8]
    ldr r2, =0x02244f10
    mov r1, #1
    bl native_fn_021ea754
    ldr r0, =0x02245228
    ldr r2, =0x02245128
    ldrsh r0, [r0, #226]
    ldrb r1, [r2, #0x1e6]
    bl native_fn_02211084
    b ov000_02214344_L1bc
ov000_02214344_L190:
    ldr r1, =0x02245228
    mov r2, #0
    ldr r0, =0x02245128
    strh r2, [r1, #226]
    strb r2, [r0, #0x1e6]
    b ov000_02214344_L1bc
ov000_02214344_L1a8:
    ldr r1, =0x02245228
    mov r2, #0
    ldr r0, =0x02245128
    strh r2, [r1, #226]
    strb r2, [r0, #0x1e6]
ov000_02214344_L1bc:
    bl native_fn_0202a280
    mov r0, #3
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
