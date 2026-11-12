/* ov001 row 0x0222cf34: 780 bytes.
 *
 * What it does: 183 instructions; 25 call(s) to 0x020449d4, 0x02044cdc, 0x0203d294, +22 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 12 literal slot(s) in the extent
 *
 * Decoded shape: loop with 25 calls (183 instructions, 25 calls, 10 branches, 21 back edges, 12 literal slots).
 *
 *   pool +0x2dc -> constant 0x02249830 (image word 0x02249830)
 *   pool +0x2e0 -> constant 0x02249976 (image word 0x02249976)
 *   pool +0x2e4 -> constant 0x022498fc (image word 0x022498fc)
 *   pool +0x2e8 -> constant 0x02249938 (image word 0x02249938)
 *   pool +0x2ec -> native_data_0222fcf0 (image word 0x0222fcf0)
 *   pool +0x2f0 -> constant 0x0224992c (image word 0x0224992c)
 *   pool +0x2f4 -> constant 0x40a00000 (image word 0x40a00000)
 *   pool +0x2f8 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x2fc -> constant 0x000003e7 (image word 0x000003e7)
 *   pool +0x300 -> constant 0x02249916 (image word 0x02249916)
 *   pool +0x304 -> constant 0x02249914 (image word 0x02249914)
 *   pool +0x308 -> constant 0x0224983c (image word 0x0224983c)
 *   branch +0x58 -> +0x70
 *   branch +0x60 -> +0x78
 *   branch +0x6c -> +0x7c
 *   branch +0x74 -> +0x7c
 *   branch +0x80 -> +0x108
 *   branch +0xb4 -> +0x100
 *   branch +0xc0 -> +0xe8
 *   branch +0xd4 -> +0xe8
 *   back edge +0xe4 -> +0xc4
 *   branch +0xec -> +0x100
 *   back edge +0x104 -> +0x94
 *   branch +0x128 -> +0x1b0
 *   branch +0x148 -> +0x1a4
 *   back edge +0x1a0 -> +0x154
 *   branch +0x1b8 -> +0x1fc
 *   branch +0x240 -> +0x268
 *   back edge +0x264 -> +0x250
 *   branch +0x270 -> +0x29c
 *   back edge +0x298 -> +0x27c
 *   test +0x54 cmp r0, #0
 *   test +0x5c cmp r0, #1
 *   test +0x64 cmp r0, #2
 *   test +0x7c cmp r5, r6
 *   test +0xb0 cmp r0, #0
 *   test +0xbc cmp r5, #0
 *   test +0xcc cmp r7, r0
 *   test +0xe0 cmp r1, r5
 *   test +0xe8 cmp r8, #0
 *   test +0x100 cmp r5, r6
 *   test +0x144 cmp r0, #0
 *   test +0x19c cmp r10, r0
 *   test +0x1b4 cmp r0, #40
 *   test +0x1e8 cmp r1, r0, lsr #16
 *   test +0x224 cmp r4, #100
 *   test +0x234 cmp r5, #0
 *   test +0x260 cmp r6, r5
 *   test +0x268 cmp r0, #0
 *   test +0x294 cmp r5, r0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222cf34; the literal pool and
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

extern void native_fn_020449d4(void);
extern void native_fn_02044cdc(void);
extern void native_fn_0203d294(void);
extern void native_fn_0207aa98(void);
extern u8 native_data_0222fcf0[];
extern void native_fn_0203cc2c(void);
extern void native_fn_02025a70(void);
extern void native_fn_02025578(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02025930(void);
extern void native_fn_02022480(void);
extern void native_fn_02024394(void);
extern void native_fn_0203cf9c(void);
extern void native_fn_02026144(void);
extern void native_fn_0207b460(void);


asm u32 native_ov001_0222cf34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    ldr r3, =0x02249830
    str r0, [sp]
    mov r2, #132
    mov r0, r0
    mul r9, r0, r2
    ldr r0, [r3, r0, lsl #2]
    mov r5, #0
    str r1, [sp, #0x4]
    mov r6, r5
    bl native_fn_020449d4
    ldrb r4, [r0, #0x5f]
    add r2, r5, #1
    ldr r1, =0x02249830
    ldr r0, [sp]
    ldr r3, =0x02249976
    ldr r0, [r1, r0, lsl #2]
    strb r4, [r3, r9]
    and r5, r2, #255
    bl native_fn_02044cdc
    cmp r0, #0
    beq ov001_0222cf34_L70
    cmp r0, #1
    beq ov001_0222cf34_L78
    cmp r0, #2
    moveq r6, #5
    b ov001_0222cf34_L7c
ov001_0222cf34_L70:
    mov r6, #3
    b ov001_0222cf34_L7c
ov001_0222cf34_L78:
    mov r6, #4
ov001_0222cf34_L7c:
    cmp r5, r6
    beq ov001_0222cf34_L108
    ldr r0, =0x022498fc
    mov r4, #0
    add r10, r0, r9
    mov r11, #255
ov001_0222cf34_L94:
    mov r0, r11
    mov r8, r4
    bl native_fn_0203d294
    add r0, r0, #1
    and r7, r0, #255
    mov r0, r7
    bl native_fn_0207aa98
    cmp r0, #0
    beq ov001_0222cf34_L100
    mov r1, #0
    cmp r5, #0
    bls ov001_0222cf34_Le8
ov001_0222cf34_Lc4:
    add r0, r10, r1, lsl #1
    ldrb r0, [r0, #0x7a]
    cmp r7, r0
    moveq r8, #1
    beq ov001_0222cf34_Le8
    add r0, r1, #1
    and r1, r0, #255
    cmp r1, r5
    blo ov001_0222cf34_Lc4
ov001_0222cf34_Le8:
    cmp r8, #0
    bne ov001_0222cf34_L100
    add r1, r10, r5, lsl #1
    add r0, r5, #1
    strb r7, [r1, #0x7a]
    and r5, r0, #255
ov001_0222cf34_L100:
    cmp r5, r6
    bne ov001_0222cf34_L94
ov001_0222cf34_L108:
    mov r0, #50
    mul r3, r5, r0
    ldr r2, =0x02249938
    ldr r0, =native_data_0222fcf0
    mov r1, #1
    strh r3, [r2, r9]
    bl native_fn_0203cc2c
    movs r7, r0
    beq ov001_0222cf34_L1b0
    mov r0, r6
    bl native_fn_02025a70
    ldr r1, =0x0224992c
    mov r11, r0
    ldrb r0, [r1, r9]
    mov r10, #0
    cmp r0, #0
    bls ov001_0222cf34_L1a4
    ldr r0, =0x022498fc
    add r8, r0, r9
ov001_0222cf34_L154:
    ldrb r0, [r7, r10]
    bl native_fn_02025a70
    mov r4, r0
    ldr r1, =0x40a00000
    mov r0, r11
    bl native_fn_02025578
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_02025930
    bl native_fn_02022480
    bl native_fn_02024394
    ldrsh r2, [r8, #60]
    add r1, r10, #1
    and r10, r1, #255
    add r0, r2, r0
    strh r0, [r8, #60]
    ldrb r0, [r8, #0x30]
    cmp r10, r0
    blo ov001_0222cf34_L154
ov001_0222cf34_L1a4:
    mov r1, r7
    mov r0, #1
    bl native_fn_0203cf9c
ov001_0222cf34_L1b0:
    ldr r0, [sp, #0x4]
    cmp r0, #40
    blo ov001_0222cf34_L1fc
    sub r1, r0, #40
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    ldr r0, =0x02249938
    ldr r1, =0x000003e7
    ldrsh r2, [r0, r9]
    add r0, r3, #1
    mul r0, r2, r0
    mov r0, r0, lsl #16
    cmp r1, r0, lsr #16
    mov r2, r0, lsr #16
    ldr r0, =0x02249938
    movls r2, r1
    strh r2, [r0, r9]
ov001_0222cf34_L1fc:
    ldr r0, =0x02249938
    mov r1, r6
    ldrsh r4, [r0, r9]
    mov r0, r4
    bl native_fn_02026144
    mov r2, r0, lsl #16
    mov r0, r4
    mov r1, r6
    mov r4, r2, lsr #16
    bl native_fn_02026144
    cmp r4, #100
    movhs r4, #100
    and r0, r1, #255
    mov r1, r4, lsl #16
    cmp r5, #0
    mov r2, r1, lsr #16
    mov r6, #0
    bls ov001_0222cf34_L268
    ldr r1, =0x022498fc
    and r3, r2, #255
    add r4, r1, r9
ov001_0222cf34_L250:
    add r1, r6, #1
    add r2, r4, r6, lsl #1
    and r6, r1, #255
    strb r3, [r2, #0x7b]
    cmp r6, r5
    blo ov001_0222cf34_L250
ov001_0222cf34_L268:
    cmp r0, #0
    mov r5, #0
    bls ov001_0222cf34_L29c
    ldr r1, =0x022498fc
    add r4, r1, r9
ov001_0222cf34_L27c:
    add r3, r4, r5, lsl #1
    ldrb r2, [r3, #0x7b]
    add r1, r5, #1
    and r5, r1, #255
    add r1, r2, #1
    strb r1, [r3, #0x7b]
    cmp r5, r0
    blo ov001_0222cf34_L27c
ov001_0222cf34_L29c:
    ldr r0, [sp]
    mov r1, #132
    mul r5, r0, r1
    ldr r1, =0x02249916
    ldr r0, =0x022498fc
    ldr r3, =0x02249914
    add r2, r0, r5
    ldrsh r0, [r3, r5]
    ldr r4, =0x0224983c
    ldr r3, [sp]
    ldrb r1, [r1, r5]
    add r2, r2, #122
    add r3, r4, r3, lsl #6
    bl native_fn_0207b460
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
