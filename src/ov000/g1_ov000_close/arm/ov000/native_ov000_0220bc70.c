/* ov000 row 0x0220bc70: 736 bytes.
 *
 * What it does: 184 instructions; 20 call(s) to 0x02042c0c, 0x0221089c, 0x020c56b4, +17 more; loops (back edge at +0x3c); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x5c
 *   branch +0x60 -> +0x144
 *   branch +0xc4 -> +0xe8
 *   branch +0xf8 -> +0x110
 *   branch +0x148 -> +0x200
 *   branch +0x16c -> +0x19c
 *   branch +0x17c -> +0x19c
 *   branch +0x198 -> +0x1d8
 *   branch +0x204 -> +0x260
 *   branch +0x2a4 -> +0x2b8
 *   test +0x14 cmp r2, #0
 *   test +0x5c cmp r2, #10
 *   test +0xc0 cmp r3, r0
 *   test +0xf4 cmp r2, r0
 *   test +0x110 cmp r1, #0
 *   test +0x144 cmp r2, #20
 *   test +0x168 tst r0, #3
 *   test +0x178 cmp r0, #60
 *   test +0x1bc cmp r0, #40
 *   test +0x200 cmp r2, #30
 *   test +0x23c cmp r1, #0
 *   test +0x260 cmp r2, #40
 *   test +0x2a0 cmp r0, #0
 *   6 block transfer(s), 18 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220bc70; the literal pool and
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

extern void native_fn_02042c0c(void);
extern void native_fn_0221089c(void);
extern void native_fn_020c56b4(void);
extern void native_fn_021dc374(void);
extern void native_fn_0203d294(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02026144(void);
extern void native_fn_02042bfc(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02041f90(void);


asm u32 native_ov000_0220bc70 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r4, r0
    ldrb r2, [r4, #0x279]
    mov r1, #0
    cmp r2, #0
    bne ov000_0220bc70_L5c
    add r0, r4, #112
    add r3, r4, #656
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r2, #1
    mov r0, r4
    mov r1, #31
    strb r2, [r4, #0x2c1]
    bl native_fn_02042c0c
    mov r0, r4
    mov r1, #1
    bl native_fn_0221089c
    mov r0, #10
    add sp, sp, #12
    strb r0, [r4, #0x279]
    ldmia sp!, {r4, r5, r6, r7, pc}
ov000_0220bc70_L5c:
    cmp r2, #10
    bne ov000_0220bc70_L144
    add r2, r4, #512
    ldrsh r7, [r2, #122]
    mov r0, #89
    ldr r12, [r4, #0x70]
    ldr r3, [r4, #0x284]
    smulbb r14, r7, r0
    ldr r6, [r4, #0x28c]
    ldr r5, [r4, #0x288]
    add r0, r12, r3
    str r0, [r4, #0x70]
    mul r3, r7, r14
    ldr r0, [r4, #0x78]
    sub r3, r5, r3, asr #1
    add r0, r0, r6
    str r0, [r4, #0x78]
    ldr r0, [r4, #0x74]
    add r0, r0, r3
    str r0, [r4, #0x74]
    ldrsh r0, [r2, #122]
    add r0, r0, #1
    strh r0, [r2, #122]
    ldr r3, [r4, #0x74]
    ldr r0, [r4, #0x294]
    cmp r3, r0
    bge ov000_0220bc70_Le8
    ldrsh r0, [r2, #118]
    bl native_fn_020c56b4
    ldrb r3, [r0, #0xc]
    add r2, sp, #0
    add r0, r4, #112
    add r1, r4, #528
    bl native_fn_021dc374
    mov r1, r0
ov000_0220bc70_Le8:
    ldr r0, [r4, #0x294]
    ldr r2, [r4, #0x74]
    sub r0, r0, #4194304
    cmp r2, r0
    bge ov000_0220bc70_L110
    add r0, r4, #112
    add r3, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r1, #1
ov000_0220bc70_L110:
    cmp r1, #0
    addeq sp, sp, #12
    ldmeqia sp!, {r4, r5, r6, r7, pc}
    add r0, sp, #0
    add r3, r4, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    strb r0, [r4, #0x2c1]
    mov r0, #20
    add sp, sp, #12
    strb r0, [r4, #0x279]
    ldmia sp!, {r4, r5, r6, r7, pc}
ov000_0220bc70_L144:
    cmp r2, #20
    bne ov000_0220bc70_L200
    mov r0, #60
    bl native_fn_0203d294
    add r2, r0, #30
    add r1, r4, #512
    mvn r0, #-2147483648
    strh r2, [r1, #122]
    bl native_fn_0203d294
    tst r0, #3
    bne ov000_0220bc70_L19c
    add r0, r4, #512
    ldrsh r0, [r0, #122]
    cmp r0, #60
    bge ov000_0220bc70_L19c
    mov r1, #0
    mov r0, r4
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, #0
    str r0, [r4, #0x27c]
    b ov000_0220bc70_L1d8
ov000_0220bc70_L19c:
    mov r0, r4
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    mov r0, #360
    bl native_fn_0203d294
    sub r2, r0, #180
    add r0, r2, #20
    cmp r0, #40
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    movlo r2, #0
    mov r0, r2, lsl #12
    bl native_fn_02026144
    str r0, [r4, #0x27c]
ov000_0220bc70_L1d8:
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldr r1, [r0, #0x14]
    mov r0, r4
    bl native_fn_02042bfc
    mov r0, #30
    add sp, sp, #12
    strb r0, [r4, #0x279]
    ldmia sp!, {r4, r5, r6, r7, pc}
ov000_0220bc70_L200:
    cmp r2, #30
    bne ov000_0220bc70_L260
    bl native_fn_02042c2c
    ldr r1, [r4, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    mov r1, r0
    mov r0, r4
    mov r2, #0
    bl native_fn_02041f90
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r1, [r0, #122]
    cmp r1, #0
    addgt sp, sp, #12
    ldmgtia sp!, {r4, r5, r6, r7, pc}
    mov r1, #31
    strh r1, [r0, #122]
    mov r0, #40
    add sp, sp, #12
    strb r0, [r4, #0x279]
    ldmia sp!, {r4, r5, r6, r7, pc}
ov000_0220bc70_L260:
    cmp r2, #40
    addne sp, sp, #12
    ldmneia sp!, {r4, r5, r6, r7, pc}
    bl native_fn_02042c2c
    ldr r1, [r4, #0x27c]
    add r0, r0, r1
    bl native_fn_02028158
    mov r1, r0
    mov r0, r4
    mov r2, #0
    bl native_fn_02041f90
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    bgt ov000_0220bc70_L2b8
    mov r0, #50
    strb r0, [r4, #0x279]
    mov r0, #0
    strb r0, [r4, #0x274]
ov000_0220bc70_L2b8:
    add r0, r4, #512
    ldrsh r1, [r0, #122]
    mov r0, r4
    and r1, r1, #255
    bl native_fn_02042c0c
    mov r0, r4
    mov r1, #0
    bl native_fn_0221089c
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
