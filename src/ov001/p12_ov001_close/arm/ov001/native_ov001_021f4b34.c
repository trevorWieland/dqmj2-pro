/* ov001 row 0x021f4b34: 492 bytes.
 *
 * What it does: 120 instructions; 12 call(s) to 0x0207afec, 0x021f47b8, 0x021f2120, +9 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (120 instructions, 12 calls, 11 branches, 11 back edges, 3 literal slots).
 *
 *   pool +0x1e0 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1e4 -> constant 0x00000119 (image word 0x00000119)
 *   pool +0x1e8 -> constant 0x0000010d (image word 0x0000010d)
 *   branch +0x28 -> +0x40
 *   branch +0x4c -> +0xb4
 *   branch +0x80 -> +0xb4
 *   branch +0xc0 -> +0xe0
 *   branch +0xec -> +0x108
 *   branch +0x114 -> +0x138
 *   branch +0x144 -> +0x1d8
 *   branch +0x150 -> +0x190
 *   branch +0x164 -> +0x190
 *   branch +0x19c -> +0x1a8
 *   branch +0x1c4 -> +0x1d8
 *   test +0x20 cmp r2, #0
 *   test +0x48 cmp r1, #0
 *   test +0x7c cmp r0, #0
 *   test +0xbc cmp r1, #10
 *   test +0xd0 cmp r1, #45
 *   test +0xe8 cmp r0, #40
 *   test +0x110 cmp r1, #50
 *   test +0x128 cmp r0, #0
 *   test +0x140 cmp r1, #100
 *   test +0x14c cmp r1, #0
 *   test +0x160 cmp r0, #0
 *   test +0x198 cmp r1, #0
 *   test +0x1b8 cmp r1, #0
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f4b34; the literal pool and
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
extern void native_fn_021f47b8(void);
extern void native_fn_021f2120(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021e2278(void);
extern void native_fn_021f4210(void);


asm u32 native_ov001_021f4b34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x0223989c
    ldrh r0, [r1, #80]
    ldr r1, [r1, #0x84]
    ldrb r4, [r1, #0x31e]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    ldrb r2, [r1, #0x10]
    cmp r2, #0
    ldrne r5, [r1, #0x80]
    bne ov001_021f4b34_L40
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    ldreq r5, [r1, #0x80]
    movne r5, #0
ov001_021f4b34_L40:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0xc]
    cmp r1, #0
    bne ov001_021f4b34_Lb4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x84]
    mov r1, r5
    bl native_fn_021f47b8
    ldr r1, =0x0223989c
    mov r2, #0
    strb r0, [r1, #0xb]
    strb r2, [r1, #0xd]
    mov r0, #10
    strb r0, [r1, #0xc]
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    beq ov001_021f4b34_Lb4
    mov r0, r5
    mov r1, #176
    bl native_fn_021f2120
    mov r0, r5
    mov r1, #249
    bl native_fn_021f2120
    ldr r1, =0x00000119
    mov r0, r5
    bl native_fn_021f2120
    ldr r1, =0x0000010d
    mov r0, r5
    bl native_fn_021f2120
ov001_021f4b34_Lb4:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0xc]
    cmp r1, #10
    bne ov001_021f4b34_Le0
    ldrb r1, [r0, #0xd]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #45
    strb r2, [r0, #0xd]
    movhi r1, #40
    strhib r1, [r0, #0xc]
ov001_021f4b34_Le0:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0xc]
    cmp r0, #40
    bne ov001_021f4b34_L108
    mov r0, r4
    bl native_fn_0220f868
    ldr r1, =0x0223989c
    mov r2, #50
    strb r0, [r1, #0x5]
    strb r2, [r1, #0xc]
ov001_021f4b34_L108:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0xc]
    cmp r1, #50
    bne ov001_021f4b34_L138
    ldrb r1, [r0, #0x5]
    mov r0, r5
    mov r2, r4
    bl native_fn_021f2230
    cmp r0, #0
    ldrne r0, =0x0223989c
    movne r1, #100
    strneb r1, [r0, #0xc]
ov001_021f4b34_L138:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0xc]
    cmp r1, #100
    bne ov001_021f4b34_L1d8
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    bne ov001_021f4b34_L190
    ldrh r0, [r0, #80]
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f4b34_L190
    ldr r0, =0x0223989c
    mov r1, #8
    ldr r0, [r0, #0x84]
    mov r2, #0
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
ov001_021f4b34_L190:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0xb]
    cmp r1, #0
    beq ov001_021f4b34_L1a8
    ldr r0, [r0, #0x84]
    bl native_fn_021e2278
ov001_021f4b34_L1a8:
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0xc]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    moveq r1, #27
    streqb r1, [r0, #0x1b]
    beq ov001_021f4b34_L1d8
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f4b34_L1d8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
