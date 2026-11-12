/* ov001 row 0x021f7a40: 816 bytes.
 *
 * What it does: 203 instructions; 25 call(s) to 0x0207afec, 0x0207afec, 0x0203d294, +22 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 25 calls (203 instructions, 25 calls, 18 branches, 21 back edges, 1 literal slot).
 *
 *   pool +0x32c -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x28 -> +0x84
 *   branch +0x80 -> +0x324
 *   branch +0x88 -> +0x11c
 *   branch +0x118 -> +0x324
 *   branch +0x120 -> +0x21c
 *   branch +0x138 -> +0x324
 *   branch +0x148 -> +0x184
 *   back edge +0x170 -> +0x150
 *   branch +0x180 -> +0x324
 *   branch +0x1b4 -> +0x1c0
 *   back edge +0x1cc -> +0x190
 *   branch +0x1fc -> +0x324
 *   branch +0x218 -> +0x324
 *   branch +0x220 -> +0x258
 *   branch +0x238 -> +0x324
 *   branch +0x254 -> +0x324
 *   branch +0x25c -> +0x288
 *   branch +0x274 -> +0x324
 *   branch +0x284 -> +0x324
 *   branch +0x28c -> +0x324
 *   branch +0x298 -> +0x2d8
 *   branch +0x2ac -> +0x2d8
 *   branch +0x310 -> +0x324
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r0, #0
 *   test +0x84 cmp r0, #5
 *   test +0x98 cmp r2, #0
 *   test +0xdc cmp r2, r0
 *   test +0x11c cmp r0, #10
 *   test +0x134 cmp r0, #10
 *   test +0x144 cmp r1, r0
 *   test +0x16c cmp r0, #0
 *   test +0x1b0 cmp r1, #0
 *   test +0x1c4 cmp r5, #3
 *   test +0x1e8 cmp r1, #0
 *   test +0x1f8 cmp r0, #0
 *   test +0x21c cmp r0, #20
 *   test +0x234 cmp r0, #20
 *   test +0x258 cmp r0, #30
 *   test +0x270 cmp r0, #0
 *   test +0x288 cmp r0, #100
 *   test +0x294 cmp r0, #0
 *   test +0x2a8 cmp r0, #0
 *   test +0x2e0 cmp r1, #0
 *   test +0x304 cmp r1, #0
 *   0 block transfer(s), 22 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f7a40; the literal pool and
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
extern void native_fn_0203d294(void);
extern void native_fn_021f2304(void);
extern void native_fn_021db438(void);
extern void native_fn_021f7544(void);
extern void native_fn_021ea428(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021e2390(void);
extern void native_fn_021f2120(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021f4210(void);


asm u32 native_ov001_021f7a40 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0223989c
    ldr r7, =0x0223989c
    ldr r1, [r0, #0x84]
    ldrb r0, [r1, #0x31e]
    cmp r0, #0
    ldrb r0, [r7, #0x34]
    moveq r4, #1
    movne r4, #0
    cmp r0, #0
    bne ov001_021f7a40_L84
    ldrh r0, [r7, #80]
    bl native_fn_0207afec
    mov r1, r7
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r1, [r4, #26]
    ldrsh r0, [r0, #24]
    sub r0, r1, r0
    add r0, r0, #1
    bl native_fn_0203d294
    mov r1, r7
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r2, [r0, #24]
    mov r0, r7
    mov r1, #5
    add r2, r4, r2
    strb r2, [r0, #0x32]
    strb r1, [r0, #0x34]
    b ov001_021f7a40_L324
ov001_021f7a40_L84:
    cmp r0, #5
    bne ov001_021f7a40_L11c
    mov r0, #1
    strb r0, [r1, #0x356]
    ldrb r2, [r7, #0x10]
    cmp r2, #0
    ldreqb r0, [r7, #0x33]
    addeq r0, r0, #1
    ldrneb r0, [r7, #0x32]
    strb r0, [r7, #0x33]
    ldr r0, =0x0223989c
    ldrh r1, [r0, #80]
    ldr r0, [r0, #0x80]
    bl native_fn_021f2304
    mov r1, r0
    mov r0, r4
    bl native_fn_021db438
    ldr r2, =0x0223989c
    mov r1, r0
    ldr r0, [r2, #0x80]
    ldrb r2, [r1, #0x31f]
    ldrb r0, [r0, #0x31f]
    cmp r2, r0
    ldr r0, =0x0223989c
    movne r2, #1
    ldr r0, [r0, #0x84]
    moveq r2, #0
    bl native_fn_021f7544
    ldr r0, =0x0223989c
    ldrh r1, [r0, #80]
    ldr r0, [r0, #0x80]
    bl native_fn_021ea428
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x34]
    mov r1, #0
    strb r1, [r0, #0x31]
    b ov001_021f7a40_L324
ov001_021f7a40_L11c:
    cmp r0, #10
    bne ov001_021f7a40_L21c
    ldrb r0, [r7, #0x31]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r7, #0x31]
    cmp r0, #10
    blo ov001_021f7a40_L324
    ldrb r1, [r7, #0x33]
    ldrb r0, [r7, #0x32]
    cmp r1, r0
    bhs ov001_021f7a40_L184
    mov r5, #3
ov001_021f7a40_L150:
    mov r0, r5
    bl native_fn_0203d294
    mov r1, r0
    mov r0, r4
    bl native_fn_021db438
    str r0, [r7, #0x80]
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f7a40_L150
    ldr r0, =0x0223989c
    mov r1, #5
    strb r1, [r0, #0x34]
    b ov001_021f7a40_L324
ov001_021f7a40_L184:
    mov r5, #0
    mov r6, r5
    mov r4, r5
ov001_021f7a40_L190:
    ldr r0, [r7, #0x80]
    mov r1, r4
    ldrb r0, [r0, #0x31e]
    bl native_fn_021db438
    ldr r1, [r7, #0x84]
    add r1, r1, r5, lsl #1
    add r1, r1, #768
    ldrsh r1, [r1, #78]
    cmp r1, #0
    ble ov001_021f7a40_L1c0
    add r0, r0, r6
    bl native_fn_021e2390
ov001_021f7a40_L1c0:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_021f7a40_L190
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x34]
    mov r2, #0
    strb r2, [r0, #0x31]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    strneb r2, [r0, #0x2b]
    ldr r0, =0x0223989c
    ldrsb r0, [r0, #43]
    cmp r0, #0
    ble ov001_021f7a40_L324
    mov r0, #0
    mov r1, #249
    bl native_fn_021f2120
    mov r0, #0
    mov r1, #176
    bl native_fn_021f2120
    b ov001_021f7a40_L324
ov001_021f7a40_L21c:
    cmp r0, #20
    bne ov001_021f7a40_L258
    ldrb r0, [r7, #0x31]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r7, #0x31]
    cmp r0, #20
    blo ov001_021f7a40_L324
    mov r0, r4
    bl native_fn_0220f868
    mov r1, r7
    mov r2, #30
    strb r0, [r1, #0x2e]
    strb r2, [r1, #0x34]
    b ov001_021f7a40_L324
ov001_021f7a40_L258:
    cmp r0, #30
    bne ov001_021f7a40_L288
    ldrb r1, [r7, #0x2e]
    mov r2, r4
    mov r0, #0
    bl native_fn_021f2230
    cmp r0, #0
    beq ov001_021f7a40_L324
    mov r0, r7
    mov r1, #100
    strb r1, [r0, #0x34]
    b ov001_021f7a40_L324
ov001_021f7a40_L288:
    cmp r0, #100
    bne ov001_021f7a40_L324
    ldrb r0, [r7, #0x10]
    cmp r0, #0
    bne ov001_021f7a40_L2d8
    ldrh r0, [r7, #80]
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f7a40_L2d8
    mov r0, r7
    ldr r0, [r0, #0x84]
    mov r2, #0
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    mov r1, #8
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
ov001_021f7a40_L2d8:
    ldr r0, =0x0223989c
    ldrsb r1, [r0, #43]
    cmp r1, #0
    movgt r1, #1
    movle r1, #0
    strb r1, [r0, #0x10]
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x34]
    strb r1, [r0, #0x33]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    moveq r1, #27
    streqb r1, [r0, #0x1b]
    beq ov001_021f7a40_L324
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f7a40_L324:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
