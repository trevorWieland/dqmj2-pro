/* ov000 row 0x02204a90: 608 bytes.
 *
 * What it does: 150 instructions; 22 call(s) to 0x02061944, 0x0206ea80, 0x02204dec, +19 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x258 -> native_data_0222f548 (image word 0x0222f548)
 *   pool +0x25c -> constant 0x02238190 (image word 0x02238190)
 *   branch +0x30 -> +0x40
 *   branch +0x38 -> +0x90
 *   branch +0x3c -> +0x250
 *   branch +0x6c -> +0x90
 *   branch +0xa0 -> +0xbc
 *   branch +0xb8 -> +0x10c
 *   branch +0xe4 -> +0x10c
 *   branch +0x110 -> +0x198
 *   branch +0x138 -> +0x158
 *   branch +0x154 -> +0x168
 *   branch +0x1b4 -> +0x250
 *   back edge +0x204 -> +0x1e8
 *   branch +0x214 -> +0x23c
 *   back edge +0x234 -> +0x21c
 *   branch +0x238 -> +0x240
 *   test +0x2c cmp r0, #0
 *   test +0x34 cmp r0, #1
 *   test +0x68 cmp r3, r0
 *   test +0x9c cmp r2, r12
 *   test +0xe0 cmp r1, r0
 *   test +0xe8 cmp r1, #0
 *   test +0x10c cmp r7, #0
 *   test +0x130 cmp r7, #1
 *   test +0x144 cmp r1, #2
 *   test +0x160 tst r1, #255
 *   test +0x168 cmp r7, #1
 *   test +0x1a4 cmp r0, #42
 *   test +0x1b0 cmp r0, #0
 *   test +0x200 cmp r4, #11
 *   test +0x210 cmp r0, #0
 *   test +0x230 cmp r4, #11
 *   0 block transfer(s), 21 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02204a90; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_0206ea80(void);
extern void native_fn_02204dec(void);
extern void native_fn_02204d28(void);
extern u8 native_data_0222f548[];
extern void native_fn_0206238c(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062134(void);
extern void native_fn_02062358(void);
extern void native_fn_0206e6c0(void);
extern void native_fn_0206e60c(void);
extern void native_fn_0206e474(void);
extern void native_fn_02062144(void);
extern void native_fn_0206e378(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02204fbc(void);
extern void native_fn_02204f6c(void);


asm u32 native_ov000_02204a90 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_02061944
    mov r4, r0
    bl native_fn_0206ea80
    add r1, r4, #512
    ldrsb r2, [r1, #105]
    mov r6, #0
    mov r5, r0
    strb r2, [sp]
    ldrsb r0, [r1, #106]
    mov r7, r6
    cmp r0, #0
    beq ov000_02204a90_L40
    cmp r0, #1
    beq ov000_02204a90_L90
    b ov000_02204a90_L250
ov000_02204a90_L40:
    bl native_fn_02204dec
    bl native_fn_02204d28
    mov lr, #1
    strb lr, [r4, #0x26a]
    ldr r1, =native_data_0222f548
    strb lr, [r5, #0xc]
    ldr r2, =0x02238190
    ldr r3, [r1]
    sub r0, lr, #2
    strb lr, [r2, #0xa]
    cmp r3, r0
    beq ov000_02204a90_L90
    strb r3, [r2, #0x9]
    ldrb r12, [r2, #0x3]
    mov r3, r0
    mov r0, r6
    strb r12, [r2, #0x8]
    str r3, [r1]
    strb r0, [r2, #0x3]
    strb r0, [r2, #0x2]
ov000_02204a90_L90:
    ldr r1, =native_data_0222f548
    mvn r12, #0
    ldr r2, [r1]
    cmp r2, r12
    bne ov000_02204a90_Lbc
    mov r1, #14
    add r0, sp, #0
    mov r2, r1
    bl native_fn_0206238c
    mov r7, r0
    b ov000_02204a90_L10c
ov000_02204a90_Lbc:
    ldr r0, =0x02238190
    str r12, [r1]
    strb r2, [r0, #0x9]
    ldrb r2, [r0, #0x3]
    mov r1, #0
    strb r2, [r0, #0x8]
    strb r1, [r0, #0x3]
    ldrb r1, [r0, #0x2]
    ldrb r0, [r0, #0x7]
    cmp r1, r0
    beq ov000_02204a90_L10c
    cmp r1, #0
    mov r3, #14
    movne r12, #1
    mov r2, r12, lsl #24
    sub r0, r3, #15
    mov r1, #86
    strb r3, [sp]
    mov r7, r2, asr #24
    bl native_fn_0205e7a8
ov000_02204a90_L10c:
    cmp r7, #0
    beq ov000_02204a90_L198
    ldrsb r0, [sp]
    bl native_fn_020620b4
    mov r0, #1
    bl native_fn_02062134
    ldr r0, =0x02238190
    mov r2, #1
    strb r2, [r0, #0x1]
    cmp r7, #1
    ldrb r1, [r0, #0x7]
    bne ov000_02204a90_L158
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #2
    strb r2, [r0, #0x7]
    movhs r1, #0
    strhsb r1, [r0, #0x7]
    b ov000_02204a90_L168
ov000_02204a90_L158:
    sub r1, r1, #1
    strb r1, [r0, #0x7]
    tst r1, #255
    strneb r2, [r0, #0x7]
ov000_02204a90_L168:
    cmp r7, #1
    movne r0, #0
    moveq r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02062358
    ldr r0, =0x02238190
    ldrb r0, [r0, #0x7]
    bl native_fn_0206e6c0
    mov r0, #0
    bl native_fn_0206e60c
    mov r6, #1
ov000_02204a90_L198:
    bl native_fn_0206e474
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    ldrsb r0, [r5, #12]
    movne r6, #1
    cmp r0, #0
    beq ov000_02204a90_L250
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    ldr r0, =0x02238190
    ldrb r0, [r0, #0x7]
    bl native_fn_0206e6c0
    mov r0, #1
    bl native_fn_0206e60c
    mov r0, #0
    bl native_fn_0206e378
    mov r4, #0
ov000_02204a90_L1e8:
    mov r0, r4
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #11
    blt ov000_02204a90_L1e8
    ldr r0, =0x02238190
    ldrb r0, [r0, #0xa]
    cmp r0, #0
    beq ov000_02204a90_L23c
    mov r4, #0
ov000_02204a90_L21c:
    mov r0, r4
    bl native_fn_02204fbc
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #11
    blt ov000_02204a90_L21c
    b ov000_02204a90_L240
ov000_02204a90_L23c:
    bl native_fn_02204f6c
ov000_02204a90_L240:
    mov r1, #0
    ldr r0, =0x02238190
    strb r1, [r5, #0xc]
    strb r1, [r0, #0xa]
ov000_02204a90_L250:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
