/* ov006 row 0x02204f6c: 556 bytes.
 *
 * What it does: 134 instructions; 17 call(s) to 0x02204f58, 0x020bb144, 0x020685f0, +14 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x218 -> native_data_0220bc44 (image word 0x0220bc44)
 *   pool +0x21c -> constant 0x00000fff (image word 0x00000fff)
 *   pool +0x220 -> constant 0x0221c1fc (image word 0x0221c1fc)
 *   pool +0x224 -> native_data_0220e91c (image word 0x0220e91c)
 *   pool +0x228 -> native_data_0220e920 (image word 0x0220e920)
 *   branch +0x24 -> +0x1d4
 *   back edge +0xd8 -> +0xbc
 *   back edge +0x12c -> +0x98
 *   branch +0x16c -> +0x184
 *   branch +0x180 -> +0x1a4
 *   test +0x54 cmp r4, #4
 *   test +0xd0 cmp r0, #2
 *   test +0x124 cmp r10, #2
 *   test +0x158 cmp r3, #0
 *   test +0x160 cmpeq r0, #0
 *   test +0x168 cmpeq r0, #0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204f6c; the literal pool and
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

extern void native_fn_02204f58(void);
extern void native_fn_020bb144(void);
extern void native_fn_020685f0(void);
extern void native_fn_021e92cc(void);
extern u8 native_data_0220bc44[];
extern void native_fn_021e749c(void);
extern void native_fn_021e7b64(void);
extern void native_fn_02045994(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021e7824(void);
extern u8 native_data_0220e91c[];
extern void native_fn_020211c0(void);
extern u8 native_data_0220e920[];
extern void native_fn_021e775c(void);
extern void native_fn_021e75ec(void);
extern void native_fn_021e791c(void);


asm u32 native_ov006_02204f6c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #16
    mov r7, r1
    mov r4, r2
    mov r6, r0
    mov r0, r7
    mov r1, r4
    bl native_fn_02204f58
    movs r5, r0
    bmi ov006_02204f6c_L1d4
    bl native_fn_020bb144
    mov r4, r0
    mov r0, r5
    bl native_fn_020685f0
    mov r7, r0
    mov r0, r6
    bl native_fn_021e92cc
    movs r8, r0
    addeq sp, sp, #16
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    ldrb r0, [r8, #0x1e]
    cmp r4, #4
    movne r10, #1
    sub r5, r0, #4
    mov r4, #2
    ldr r9, =native_data_0220bc44
    moveq r10, #0
    mov r0, r6
    mov r3, r5
    mov r1, #4
    mov r2, #0
    str r4, [sp]
    add r9, r9, r10, lsl #7
    bl native_fn_021e749c
    mov r0, r6
    bl native_fn_021e7b64
    mov r10, #0
    mov r4, r10
ov006_02204f6c_L98:
    ldrb r1, [r8, #0x5e]
    ldr r2, [r8, #0x58]
    ldr r3, =0x00000fff
    mla r1, r10, r1, r2
    add r1, r1, #2
    mov r1, r1, lsl #16
    mov r2, r1, lsr #16
    mov r0, #0
    add r1, sp, #12
ov006_02204f6c_Lbc:
    and lr, r2, r3
    mov r12, r0, lsl #1
    orr lr, lr, #8192
    add r0, r0, #1
    strh lr, [r1, r12]
    cmp r0, #2
    add r2, r2, #1
    blt ov006_02204f6c_Lbc
    ldrb r3, [r8, #0x5c]
    ldrb r2, [r8, #0x5d]
    mov r0, #2
    add r3, r3, #2
    add r2, r2, r10
    add r2, r3, r2, lsl #5
    mov r3, #4
    bl native_fn_02045994
    ldrb r1, [r8, #0x5e]
    ldr r2, [r8, #0x44]
    add r0, r9, r4
    mul r1, r10, r1
    ldr r2, [r2]
    add r1, r1, #2
    add r1, r2, r1, lsl #5
    mov r2, #64
    bl native_fn_02008e0c
    add r10, r10, #1
    cmp r10, #2
    add r4, r4, #64
    blt ov006_02204f6c_L98
    str r5, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r3, #0
    mov r0, r6
    mov r1, r7
    str r3, [sp, #0x8]
    mov r2, #4
    bl native_fn_021e7824
    ldr r3, [r7, #0x3c]
    cmp r3, #0
    ldreq r0, [r7, #0x40]
    cmpeq r0, #0
    ldreq r0, [r7, #0x44]
    cmpeq r0, #0
    bne ov006_02204f6c_L184
    ldr r0, =0x0221c1fc
    ldr r2, =native_data_0220e91c
    mov r1, #64
    bl native_fn_020211c0
    b ov006_02204f6c_L1a4
ov006_02204f6c_L184:
    ldr r1, [r7, #0x40]
    ldr r0, =0x0221c1fc
    str r1, [sp]
    ldr r4, [r7, #0x44]
    ldr r2, =native_data_0220e920
    mov r1, #64
    str r4, [sp, #0x4]
    bl native_fn_020211c0
ov006_02204f6c_L1a4:
    mov r0, #9
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    ldr r1, =0x0221c1fc
    mov r0, r6
    mov r2, #18
    mov r3, #0
    str r4, [sp, #0x8]
    bl native_fn_021e775c
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov006_02204f6c_L1d4:
    mov r0, r6
    bl native_fn_021e75ec
    mov r0, r6
    bl native_fn_021e7b64
    mov r0, #12
    mov r2, #10
    mla r1, r7, r0, r4
    str r2, [sp]
    mov r2, #1
    mov r0, r6
    str r2, [sp, #0x4]
    mov r3, #0
    mov r2, #2
    str r3, [sp, #0x8]
    bl native_fn_021e791c
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
