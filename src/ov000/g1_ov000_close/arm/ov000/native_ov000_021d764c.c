/* ov000 row 0x021d764c: 1208 bytes.
 *
 * What it does: 290 instructions; 49 call(s) to 0x0203cb2c, 0x02002e5c, 0x020030ec, +46 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 12 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x488 -> constant 0x04000008 (image word 0x04000008)
 *   pool +0x48c -> constant 0x00004210 (image word 0x00004210)
 *   pool +0x490 -> native_data_0222e130 (image word 0x0222e130)
 *   pool +0x494 -> native_data_0222e144 (image word 0x0222e144)
 *   pool +0x498 -> native_data_0222e158 (image word 0x0222e158)
 *   pool +0x49c -> constant 0x022300f8 (image word 0x022300f8)
 *   pool +0x4a0 -> native_data_0222e128 (image word 0x0222e128)
 *   pool +0x4a4 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x4a8 -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0x4ac -> native_data_0222e16c (image word 0x0222e16c)
 *   pool +0x4b0 -> native_data_0222e120 (image word 0x0222e120)
 *   pool +0x4b4 -> constant 0x022300c0 (image word 0x022300c0)
 *   back edge +0x1d4 -> +0x174
 *   test +0x1bc cmp r9, #2
 *   1 block transfer(s), 45 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d764c; the literal pool and
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

extern void native_fn_0203cb2c(void);
extern void native_fn_02002e5c(void);
extern void native_fn_020030ec(void);
extern void native_fn_02002c98(void);
extern void native_fn_02008c58(void);
extern u8 native_data_0222e130[];
extern void native_fn_0201d444(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern u8 native_data_0222e144[];
extern void native_fn_02004e58(void);
extern u8 native_data_0222e158[];
extern void native_fn_02004b58(void);
extern u8 native_data_0222e128[];
extern void native_fn_02084924(void);
extern void native_fn_02049ffc(void);
extern void native_fn_020bedd8(void);
extern void native_fn_02046af4(void);
extern void native_fn_021d7b04(void);
extern void native_fn_020bede4(void);
extern void native_fn_020489f0(void);
extern u8 native_data_0222e16c[];
extern void native_fn_02048404(void);
extern u8 native_data_0222e120[];
extern void native_fn_0204854c(void);
extern void native_fn_0202a37c(void);
extern void native_fn_021d75e4(void);
extern void native_fn_021d7f50(void);
extern void native_fn_021d7b64(void);


asm u32 native_ov000_021d764c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #120
    bl native_fn_0203cb2c
    mov r0, #9
    bl native_fn_02002e5c
    mov r0, #2
    bl native_fn_020030ec
    mov r1, #0
    mov r2, r1
    mov r0, #1
    bl native_fn_02002c98
    ldr r3, =0x04000008
    ldr r0, =0x00004210
    ldrh r1, [r3]
    add r4, r0, #512
    mov r0, #0
    and r1, r1, #67
    orr r1, r1, #4
    strh r1, [r3]
    ldrh r5, [r3, #2]
    mov r1, #100663296
    mov r2, #524288
    and r5, r5, #67
    orr r5, r5, #528
    orr r5, r5, #16384
    strh r5, [r3, #2]
    ldrh r5, [r3, #4]
    and r5, r5, #67
    orr r4, r5, r4
    strh r4, [r3, #4]
    ldrh r4, [r3, #6]
    and r4, r4, #67
    orr r4, r4, #536
    orr r4, r4, #1024
    strh r4, [r3, #6]
    bl native_fn_02008c58
    ldr r1, =native_data_0222e130
    add r0, sp, #88
    bl native_fn_0201d444
    add r0, sp, #88
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #88
    bl native_fn_0202a8e0
    mov r2, r0
    mov r0, r4
    mov r1, #0
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    ldr r1, =native_data_0222e144
    add r0, sp, #88
    bl native_fn_0201d444
    add r0, sp, #88
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #88
    bl native_fn_0202a8e0
    mov r2, r0
    mov r0, r4
    mov r1, #0
    bl native_fn_02004e58
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    ldr r1, =native_data_0222e158
    add r0, sp, #88
    bl native_fn_0201d444
    add r0, sp, #88
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r1, #0
    mov r2, #1536
    bl native_fn_02004b58
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    ldr r1, =0x022300f8
    mov r0, #0
    mov r2, #40
    mov r10, #1
    bl native_fn_02008c58
    ldr r7, =native_data_0222e128
    ldr r4, =0x022300f8
    mov r9, #0
    mov r6, #3
    mov r5, r10
    mov r11, #6
ov000_021d764c_L174:
    add r8, r7, r9, lsl #2
    ldrb r1, [r8, #0x3]
    mov r0, r11
    stmia sp, {r1, r6}
    str r6, [sp, #0x8]
    str r10, [sp, #0xc]
    str r5, [sp, #0x10]
    str r5, [sp, #0x14]
    ldrb r1, [r7, r9, lsl #2]
    ldrb r2, [r8, #0x1]
    ldrb r3, [r8, #0x2]
    bl native_fn_02084924
    str r0, [r4, r9, lsl #2]
    bl native_fn_02049ffc
    ldr r2, [r4, r9, lsl #2]
    add r0, r9, #1
    and r9, r0, #255
    ldr r1, [r2, #0x18]
    cmp r9, #2
    orr r0, r1, #2
    str r0, [r2, #0x18]
    ldrb r1, [r8, #0x2]
    ldrb r0, [r8, #0x3]
    mla r10, r1, r0, r10
    blo ov000_021d764c_L174
    bl native_fn_020bedd8
    add r2, sp, #24
    mov r1, r0
    str r2, [sp]
    mov r4, #255
    ldr r0, =0x021c9698
    mov r2, #31
    mov r3, #0
    str r4, [sp, #0x4]
    bl native_fn_02046af4
    add r1, sp, #24
    mov r0, #0
    bl native_fn_021d7b04
    bl native_fn_020bede4
    add r2, sp, #24
    mov r1, r0
    str r2, [sp]
    mov r0, r4
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    mov r2, #31
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    add r1, sp, #24
    bl native_fn_021d7b04
    ldr r2, =0x04000008
    mov r0, #0
    ldrh r1, [r2]
    bic r1, r1, #3
    orr r1, r1, #3
    strh r1, [r2]
    ldrh r1, [r2, #2]
    bic r1, r1, #3
    orr r1, r1, #2
    strh r1, [r2, #2]
    ldrh r1, [r2, #4]
    bic r1, r1, #3
    orr r1, r1, #1
    strh r1, [r2, #4]
    ldrh r1, [r2, #6]
    bic r1, r1, #3
    strh r1, [r2, #6]
    str r0, [r2, #0x8]
    str r0, [r2, #0xc]
    str r0, [r2, #0x10]
    str r0, [r2, #0x14]
    bl native_fn_020489f0
    mov r3, #67108864
    ldr r2, [r3]
    ldr r1, =0xffcfffef
    mov r0, #0
    and r1, r2, r1
    orr r1, r1, #16
    str r1, [r3]
    mov r1, #104857600
    mov r2, #262144
    bl native_fn_02008c58
    ldr r1, =native_data_0222e16c
    mov r0, #0
    mov r2, #4
    mov r3, #2
    bl native_fn_02048404
    mov r3, r0
    ldr r2, =native_data_0222e120
    and r1, r3, #255
    mov r0, #0
    strb r3, [r2]
    bl native_fn_0204854c
    ldr r3, =0x022300c0
    mov r1, #144
    str r0, [r3, #0x1c]
    ldr r4, [r0, #0x4]
    mov r0, #2
    mov r2, #4
    str r4, [r3, #0x20]
    bl native_fn_0202a37c
    ldr r1, =0x022300c0
    mov r2, #3
    str r0, [r1, #0x14]
    str r2, [sp]
    mov r3, #0
    str r3, [sp, #0x4]
    ldr r0, [r1, #0x14]
    mov r1, #128
    mov r2, #96
    bl native_fn_021d75e4
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x022300c0
    mov r2, #0
    str r0, [r1, #0x10]
    str r2, [sp]
    str r2, [sp, #0x4]
    ldr r0, [r1, #0x10]
    mov r1, #128
    mov r2, #96
    mov r3, #37
    bl native_fn_021d75e4
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x022300c0
    mov r2, #0
    str r0, [r1, #0x8]
    str r2, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    ldr r0, [r1, #0x8]
    mov r1, #128
    mov r2, #96
    mov r3, #38
    bl native_fn_021d75e4
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    ldr r2, =0x022300c0
    mov r1, #144
    str r0, [r2, #0x28]
    mov r0, #2
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x022300c0
    str r0, [r1, #0x2c]
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    ldr r0, [r1, #0x28]
    mov r1, #152
    mov r2, #16
    mov r3, #39
    bl native_fn_021d75e4
    mov r0, #3
    str r0, [sp]
    mov r1, #0
    ldr r0, =0x022300c0
    str r1, [sp, #0x4]
    ldr r0, [r0, #0x2c]
    mov r1, #8
    mov r2, #112
    mov r3, #39
    bl native_fn_021d75e4
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x022300c0
    mov r2, #3
    str r0, [r1, #0x18]
    str r2, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    ldr r0, [r1, #0x18]
    mov r1, #128
    mov r2, #96
    mov r3, #40
    bl native_fn_021d75e4
    bl native_fn_02048308
    bl native_fn_021d7f50
    bl native_fn_021d7b64
    mov r1, #67108864
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #5888
    str r0, [r1]
    add sp, sp, #120
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
