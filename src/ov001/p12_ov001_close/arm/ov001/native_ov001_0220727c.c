/* ov001 row 0x0220727c: 916 bytes.
 *
 * What it does: 225 instructions; 26 call(s) to 0x022068a0, 0x020449d4, 0x02049ffc, +23 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 26 calls (225 instructions, 26 calls, 7 branches, 26 back edges, 4 literal slots).
 *
 *   pool +0x384 -> constant 0x020dbc18 (image word 0x020dbc18)
 *   pool +0x388 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x38c -> native_data_0222f044 (image word 0x0222f044)
 *   pool +0x390 -> native_data_0222f048 (image word 0x0222f048)
 *   branch +0xb4 -> +0x364
 *   branch +0xcc -> +0x364
 *   branch +0x21c -> +0x25c
 *   branch +0x258 -> +0x29c
 *   branch +0x2a4 -> +0x364
 *   branch +0x2ec -> +0x324
 *   branch +0x320 -> +0x364
 *   back edge +0x378 -> +0xac
 *   test +0xb0 cmp r6, #0
 *   test +0xc8 cmp r8, #0
 *   test +0x218 cmp r0, #100
 *   test +0x220 cmp r0, r11
 *   test +0x2a0 cmp r2, #0
 *   test +0x2e8 cmp r9, #100
 *   test +0x300 cmp r9, r11
 *   test +0x374 cmp r8, #2
 *   0 block transfer(s), 30 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220727c; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_020449d4(void);
extern void native_fn_02049ffc(void);
extern void native_fn_020630b0(void);
extern void native_fn_02008be0(void);
extern void native_fn_020602ec(void);
extern void native_fn_02202320(void);
extern void native_fn_021fe6b8(void);
extern void native_fn_0206006c(void);
extern void native_fn_02085284(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087a48(void);
extern u8 native_data_0222f044[];
extern void native_fn_020877bc(void);
extern void native_fn_021fe738(void);
extern void native_fn_02065818(void);
extern u8 native_data_0222f048[];
extern void native_fn_0204a154(void);


asm u32 native_ov001_0220727c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #64
    mov r5, r0
    bl native_fn_022068a0
    mov r4, r0
    add r1, r4, r5, lsl #5
    ldr r1, [r1, #0x24]
    mov r0, r5
    str r1, [sp, #0xc]
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    add r2, r4, #20
    add r10, r2, r5, lsl #5
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    add r0, r0, #13
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    add r1, r0, #123
    mov r2, r5, lsl #1
    mov r8, #0
    add r0, sp, #28
    strh r8, [r0]
    strh r8, [r0, #2]
    add r0, r1, #256
    mov r1, r8
    add r1, r1, #16
    mov r1, r1, lsl #16
    mov r3, #16
    mov r7, r1, asr #16
    add r1, r3, #16
    mov r2, r2, lsl #24
    mov r6, r0, lsl #1
    mov r0, r2, asr #24
    str r0, [sp, #0x8]
    mov r0, r1, lsl #16
    str r0, [sp, #0x18]
    mov r0, r7, asr #3
    ldr r3, =0x020dbc18
    str r0, [sp, #0x14]
    ldrh r0, [r3, r6]
    add r4, r4, r5, lsl #5
    str r0, [sp, #0x10]
ov001_0220727c_Lac:
    ldr r6, [r10]
    cmp r6, #0
    beq ov001_0220727c_L364
    ldr r0, [r6]
    ldr r5, [r0, #0x4]
    mov r0, r5
    bl native_fn_02049ffc
    cmp r8, #0
    bne ov001_0220727c_L364
    ldr r0, [r4, #0x24]
    ldr r0, [r0, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    mov r11, r0
    mov r0, #0
    add r1, sp, #32
    mov r2, #32
    bl native_fn_02008be0
    ldr r0, [sp, #0x10]
    mov r3, #16
    strh r0, [sp, #32]
    ldr r0, [sp, #0xc]
    ldr r2, [r0, #0x1e8]
    mov r0, #0
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r2, #42]
    ldr r0, [r6]
    add r2, r2, #178
    bl native_fn_020602ec
    ldrsb r0, [r6, #5]
    bl native_fn_02202320
    bl native_fn_021fe6b8
    ldrsb r1, [r5, #31]
    str r1, [sp]
    ldrsb r1, [r5, #28]
    ldrsb r2, [r5, #29]
    ldrsb r3, [r5, #30]
    bl native_fn_0206006c
    ldrsb r0, [r6, #5]
    bl native_fn_02202320
    bl native_fn_021fe6b8
    ldrsb r1, [r5, #31]
    str r1, [sp]
    ldrsb r1, [r5, #28]
    ldrsb r2, [r5, #29]
    ldrsb r3, [r5, #30]
    bl native_fn_0206006c
    mov r2, #1
    add r0, r5, #60
    mov r1, #5
    mov r3, r2
    bl native_fn_02085284
    add r0, sp, #32
    str r0, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    ldr r1, [r5, #0x68]
    mov r2, #30
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    str r0, [sp]
    add r0, sp, #32
    str r0, [sp, #0x4]
    mov r0, r5
    mov r1, #0
    mov r2, #16
    mov r3, r7
    bl native_fn_02087a48
    mov r0, #1
    str r0, [sp]
    ldr r0, =native_data_0222f044
    mov r1, #0
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x18]
    mov r3, r7
    mov r6, r0, asr #16
    mov r0, r5
    mov r2, r6
    bl native_fn_02087a48
    add r0, r6, #8
    mov r0, r0, lsl #16
    mov r6, r0, asr #16
    mov r0, #0
    add r1, sp, #32
    mov r2, #32
    bl native_fn_02008be0
    ldrb r0, [r4, #0x30]
    cmp r0, #100
    bhs ov001_0220727c_L25c
    cmp r0, r11
    movlo r9, #1
    movhs r9, #5
    add r1, sp, #32
    mov r2, #32
    mov r3, #2
    bl native_fn_020877bc
    str r9, [sp]
    str r0, [sp, #0x4]
    mov r0, r5
    mov r1, #0
    mov r2, r6
    mov r3, r7
    bl native_fn_02087a48
    b ov001_0220727c_L29c
ov001_0220727c_L25c:
    mov r0, #9
    bl native_fn_021fe738
    ldrb r1, [r5, #0x1c]
    add r1, r1, r6, asr #3
    strh r1, [sp, #28]
    ldrb r3, [r5, #0x1d]
    ldr r1, [sp, #0x14]
    ldrsh r2, [sp, #28]
    add r1, r3, r1
    strh r1, [sp, #30]
    mov r1, r2, lsl #24
    ldrsh r2, [sp, #30]
    mov r1, r1, asr #24
    mov r2, r2, lsl #24
    mov r2, r2, asr #24
    bl native_fn_02065818
ov001_0220727c_L29c:
    ldrb r2, [r4, #0x32]
    cmp r2, #0
    beq ov001_0220727c_L364
    ldrb r1, [r4, #0x30]
    add r0, r6, #16
    mov r0, r0, lsl #16
    mov r6, r0, asr #16
    mov r0, #1
    add r9, r1, r2
    str r0, [sp]
    ldr r0, =native_data_0222f048
    mov r1, #0
    str r0, [sp, #0x4]
    mov r0, r5
    mov r2, r6
    mov r3, r7
    bl native_fn_02087a48
    add r6, r6, #8
    strh r6, [sp, #28]
    cmp r9, #100
    bge ov001_0220727c_L324
    strh r7, [sp, #30]
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    cmp r9, r11
    movlt r2, #1
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x8]
    movge r2, #5
    mov r3, r9
    add r1, sp, #28
    bl native_fn_0204a154
    b ov001_0220727c_L364
ov001_0220727c_L324:
    mov r0, #9
    bl native_fn_021fe738
    ldrb r1, [r5, #0x1c]
    add r1, r1, r6, asr #3
    strh r1, [sp, #28]
    ldrb r3, [r5, #0x1d]
    ldr r1, [sp, #0x14]
    ldrsh r2, [sp, #28]
    add r1, r3, r1
    strh r1, [sp, #30]
    mov r1, r2, lsl #24
    ldrsh r2, [sp, #30]
    mov r1, r1, asr #24
    mov r2, r2, lsl #24
    mov r2, r2, asr #24
    bl native_fn_02065818
ov001_0220727c_L364:
    add r10, r10, #8
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #2
    blt ov001_0220727c_Lac
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
