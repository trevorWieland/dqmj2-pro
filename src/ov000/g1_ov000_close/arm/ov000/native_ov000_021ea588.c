/* ov000 row 0x021ea588: 460 bytes.
 *
 * What it does: 113 instructions; 16 call(s) to 0x0202ac4c, 0x0202ac08, 0x0202a1e0, +13 more; loops (back edge at +0x28); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c4 -> constant 0x02236950 (image word 0x02236950)
 *   pool +0x1c8 -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0x5c -> +0x1b4
 *   branch +0x7c -> +0x1b4
 *   branch +0x108 -> +0x140
 *   branch +0x13c -> +0x160
 *   branch +0x1a0 -> +0x1b4
 *   test +0x18 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x104 cmpne r4, #63
 *   test +0x19c cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ea588; the literal pool and
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
extern void native_fn_0202a1e0(void);
extern void native_fn_02041ccc(void);
extern void native_fn_02041e50(void);
extern void native_fn_02211084(void);
extern void native_fn_02041f34(void);
extern void native_fn_02041f90(void);
extern void native_fn_020430b4(void);
extern void native_fn_02042464(void);
extern void native_fn_02044d14(void);
extern void native_fn_021ea518(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021ea754(void);
extern void native_fn_021eae2c(void);


asm u32 native_ov000_021ea588 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r1, =0x02236950
    ldr r0, [r1, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    cmp r0, #0
    addeq sp, sp, #4
    ldmeqia sp!, {r3, r4, pc}
    ldr r0, [r1, #0x14]
    bl native_fn_0202ac4c
    ldr r0, =0x02236950
    ldr r0, [r0, #0x14]
    bl native_fn_0202ac08
    mov r0, #1
    bl native_fn_0202a1e0
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    add r0, r0, #52
    bl native_fn_02041ccc
    cmp r0, #0
    beq ov000_021ea588_L1b4
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r1, r0, #256
    ldrsh r1, [r1, #240]
    add r1, r1, #52
    bl native_fn_02041e50
    cmp r0, #0
    beq ov000_021ea588_L1b4
    ldr r0, =0x02236950
    ldr r2, [r0, #0x18]
    add r0, r2, #256
    ldrsh r0, [r0, #240]
    ldrb r1, [r2, #0x1f4]
    bl native_fn_02211084
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    ldr r1, [r0, #0x1e0]
    ldr r2, [r0, #0x1e4]
    ldr r3, [r0, #0x1e8]
    bl native_fn_02041f34
    ldr r0, =0x02236950
    mov r2, #0
    ldr r0, [r0, #0x18]
    ldr r1, [r0, #0x1ec]
    bl native_fn_02041f90
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #106]
    bl native_fn_020430b4
    ldrsh r1, [r0, #4]
    ldr r0, =0x02236950
    mov r2, #1
    ldr r0, [r0, #0x18]
    bl native_fn_02042464
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_02044d14
    movs r4, r0
    cmpne r4, #63
    bne ov000_021ea588_L140
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_021ea518
    ldr r1, =0x02236950
    ldr r2, [r1, #0x18]
    str r0, [r2, #0x7c]
    ldr r2, [r1, #0x18]
    str r0, [r2, #0x80]
    ldr r1, [r1, #0x18]
    str r0, [r1, #0x84]
    b ov000_021ea588_L160
ov000_021ea588_L140:
    ldr r0, =0x02236950
    ldr r2, =0x0000019a
    ldr r1, [r0, #0x18]
    str r2, [r1, #0x7c]
    ldr r1, [r0, #0x18]
    str r2, [r1, #0x80]
    ldr r0, [r0, #0x18]
    str r2, [r0, #0x84]
ov000_021ea588_L160:
    ldr r0, =0x02236950
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_02044cdc
    ldr r1, =0x02236950
    str r4, [sp]
    ldr r2, [r1, #0x18]
    mov r3, r0
    ldr r0, [r1, #0x20]
    add r2, r2, #480
    mov r1, #1
    bl native_fn_021ea754
    ldr r0, =0x02236950
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    beq ov000_021ea588_L1b4
    bl native_fn_021eae2c
    ldr r0, =0x02236950
    mov r1, #0
    strb r1, [r0, #0x1]
ov000_021ea588_L1b4:
    mov r0, #2
    bl native_fn_0202a1e0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
