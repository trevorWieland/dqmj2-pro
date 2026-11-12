/* ov001 row 0x021ddf34: 800 bytes.
 *
 * What it does: 197 instructions; 23 call(s) to 0x021db438, 0x021db438, 0x020444ec, +20 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 23 calls (197 instructions, 23 calls, 34 branches, 23 back edges, 3 literal slots).
 *
 *   pool +0x314 -> native_data_0222defc (image word 0x0222defc)
 *   pool +0x318 -> constant 0x022388ec (image word 0x022388ec)
 *   pool +0x31c -> constant 0x02238a08 (image word 0x02238a08)
 *   back edge +0x34 -> +0x18
 *   branch +0x78 -> +0x94
 *   branch +0x90 -> +0xb0
 *   branch +0xac -> +0xc8
 *   branch +0xcc -> +0x2fc
 *   branch +0xf0 -> +0x134
 *   branch +0xf4 -> +0x188
 *   branch +0xfc -> +0x110
 *   branch +0x100 -> +0x168
 *   branch +0x10c -> +0x1a4
 *   branch +0x11c -> +0x1a4
 *   branch +0x120 -> +0x170
 *   branch +0x124 -> +0x178
 *   branch +0x128 -> +0x180
 *   branch +0x12c -> +0x190
 *   branch +0x130 -> +0x198
 *   branch +0x138 -> +0x14c
 *   branch +0x13c -> +0x1a0
 *   branch +0x148 -> +0x1a4
 *   branch +0x150 -> +0x15c
 *   branch +0x158 -> +0x1a4
 *   branch +0x164 -> +0x1a4
 *   branch +0x16c -> +0x1a4
 *   branch +0x174 -> +0x1a4
 *   branch +0x17c -> +0x1a4
 *   branch +0x184 -> +0x1a4
 *   branch +0x18c -> +0x1a4
 *   branch +0x194 -> +0x1a4
 *   branch +0x19c -> +0x1a4
 *   branch +0x1ac -> +0x1c8
 *   branch +0x1c4 -> +0x244
 *   back edge +0x200 -> +0x1d0
 *   back edge +0x23c -> +0x20c
 *   branch +0x240 -> +0x2bc
 *   back edge +0x27c -> +0x24c
 *   back edge +0x2b8 -> +0x288
 *   back edge +0x2c8 -> +0xe8
 *   branch +0x2d0 -> +0x2ec
 *   branch +0x2e8 -> +0x308
 *   branch +0x2f8 -> +0x308
 *   test +0x74 cmp r0, #0
 *   test +0x8c cmp r1, r0
 *   test +0xc8 cmp r5, #0
 *   test +0xec cmp r1, #188
 *   test +0xf8 cmp r1, #72
 *   test +0x104 cmp r1, #42
 *   test +0x114 cmp r0, #4
 *   test +0x134 cmp r1, #190
 *   test +0x140 cmp r1, #189
 *   test +0x14c cmp r1, #236
 *   test +0x15c cmp r1, #237
 *   test +0x1a8 cmp r0, #0
 *   test +0x1c0 cmp r1, r0
 *   test +0x1e4 cmp r0, #0
 *   test +0x1f8 cmp r5, #3
 *   test +0x220 cmp r0, #0
 *   test +0x234 cmp r9, #3
 *   test +0x260 cmp r0, #0
 *   test +0x274 cmp r9, #3
 *   test +0x29c cmp r0, #0
 *   test +0x2b0 cmp r9, #3
 *   test +0x2c0 cmp r11, #15
 *   test +0x2cc cmp r6, #0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ddf34; the literal pool and
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

extern u8 native_data_0222defc[];
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_020444ec(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_021dde98(void);
extern void native_fn_02008d78(void);
extern void native_fn_021ddedc(void);


asm u32 native_ov001_021ddf34 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r3, =native_data_0222defc
    add r4, sp, #0
    mov r5, #0
    mov r2, #7
ov001_021ddf34_L18:
    ldrb r1, [r3]
    ldrb r0, [r3, #0x1]
    add r3, r3, #2
    strb r1, [r4]
    strb r0, [r4, #0x1]
    add r4, r4, #2
    subs r2, r2, #1
    bne ov001_021ddf34_L18
    ldrb r3, [r3]
    ldr r2, =0x022388ec
    mov r6, #0
    mov r0, r6
    mov r1, r6
    strb r3, [r4]
    strb r6, [r2, #0x18]
    strb r6, [r2, #0x19]
    bl ov001_side_slot_record_021db438
    mov r10, r0
    mov r0, #1
    mov r1, r6
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl native_fn_020444ec
    cmp r0, #0
    beq ov001_021ddf34_L94
    bl native_fn_01ffa824
    mov r8, r0
    bl native_fn_01ffa84c
    and r1, r8, #255
    cmp r1, r0
    bhs ov001_021ddf34_Lb0
ov001_021ddf34_L94:
    mov r0, r10
    bl native_fn_021dde98
    orr r5, r5, r0
    mov r0, r4
    bl native_fn_021dde98
    orr r5, r5, r0
    b ov001_021ddf34_Lc8
ov001_021ddf34_Lb0:
    mov r0, r4
    bl native_fn_021dde98
    orr r5, r5, r0
    mov r0, r10
    bl native_fn_021dde98
    orr r5, r5, r0
ov001_021ddf34_Lc8:
    cmp r5, #0
    beq ov001_021ddf34_L2fc
    ldr r0, =0x02238a08
    mov r1, #0
    mov r2, #200
    bl native_fn_02008d78
    add r8, sp, #0
    mov r11, #0
ov001_021ddf34_Le8:
    ldrb r1, [r8]
    cmp r1, #188
    bgt ov001_021ddf34_L134
    bge ov001_021ddf34_L188
    cmp r1, #72
    bgt ov001_021ddf34_L110
    bge ov001_021ddf34_L168
    cmp r1, #42
    moveq r7, #64
    b ov001_021ddf34_L1a4
ov001_021ddf34_L110:
    sub r0, r1, #123
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov001_021ddf34_L1a4
    b ov001_021ddf34_L170
    b ov001_021ddf34_L178
    b ov001_021ddf34_L180
    b ov001_021ddf34_L190
    b ov001_021ddf34_L198
ov001_021ddf34_L134:
    cmp r1, #190
    bgt ov001_021ddf34_L14c
    bge ov001_021ddf34_L1a0
    cmp r1, #189
    moveq r7, #134217728
    b ov001_021ddf34_L1a4
ov001_021ddf34_L14c:
    cmp r1, #236
    bgt ov001_021ddf34_L15c
    moveq r7, #2097152
    b ov001_021ddf34_L1a4
ov001_021ddf34_L15c:
    cmp r1, #237
    moveq r7, #4194304
    b ov001_021ddf34_L1a4
ov001_021ddf34_L168:
    mov r7, #8192
    b ov001_021ddf34_L1a4
ov001_021ddf34_L170:
    mov r7, #32768
    b ov001_021ddf34_L1a4
ov001_021ddf34_L178:
    mov r7, #65536
    b ov001_021ddf34_L1a4
ov001_021ddf34_L180:
    mov r7, #131072
    b ov001_021ddf34_L1a4
ov001_021ddf34_L188:
    mov r7, #33554432
    b ov001_021ddf34_L1a4
ov001_021ddf34_L190:
    mov r7, #262144
    b ov001_021ddf34_L1a4
ov001_021ddf34_L198:
    mov r7, #1048576
    b ov001_021ddf34_L1a4
ov001_021ddf34_L1a0:
    mov r7, #67108864
ov001_021ddf34_L1a4:
    bl native_fn_020444ec
    cmp r0, #0
    beq ov001_021ddf34_L1c8
    bl native_fn_01ffa824
    mov r5, r0
    bl native_fn_01ffa84c
    and r1, r5, #255
    cmp r1, r0
    bhs ov001_021ddf34_L244
ov001_021ddf34_L1c8:
    mov r9, r10
    mov r5, #0
ov001_021ddf34_L1d0:
    ldrb r0, [r8]
    mov r1, r9
    mov r2, r7
    mov r3, r6
    bl native_fn_021ddedc
    cmp r0, #0
    addne r0, r6, #1
    movne r0, r0, lsl #24
    add r5, r5, #1
    movne r6, r0, asr #24
    cmp r5, #3
    add r9, r9, #1088
    blt ov001_021ddf34_L1d0
    mov r5, r4
    mov r9, #0
ov001_021ddf34_L20c:
    ldrb r0, [r8]
    mov r1, r5
    mov r2, r7
    mov r3, r6
    bl native_fn_021ddedc
    cmp r0, #0
    addne r0, r6, #1
    movne r0, r0, lsl #24
    add r9, r9, #1
    movne r6, r0, asr #24
    cmp r9, #3
    add r5, r5, #1088
    blt ov001_021ddf34_L20c
    b ov001_021ddf34_L2bc
ov001_021ddf34_L244:
    mov r5, r4
    mov r9, #0
ov001_021ddf34_L24c:
    ldrb r0, [r8]
    mov r1, r5
    mov r2, r7
    mov r3, r6
    bl native_fn_021ddedc
    cmp r0, #0
    addne r0, r6, #1
    movne r0, r0, lsl #24
    add r9, r9, #1
    movne r6, r0, asr #24
    cmp r9, #3
    add r5, r5, #1088
    blt ov001_021ddf34_L24c
    mov r5, r10
    mov r9, #0
ov001_021ddf34_L288:
    ldrb r0, [r8]
    mov r1, r5
    mov r2, r7
    mov r3, r6
    bl native_fn_021ddedc
    cmp r0, #0
    addne r0, r6, #1
    movne r0, r0, lsl #24
    add r9, r9, #1
    movne r6, r0, asr #24
    cmp r9, #3
    add r5, r5, #1088
    blt ov001_021ddf34_L288
ov001_021ddf34_L2bc:
    add r11, r11, #1
    cmp r11, #15
    add r8, r8, #1
    blt ov001_021ddf34_Le8
    cmp r6, #0
    ble ov001_021ddf34_L2ec
    ldr r0, =0x022388ec
    mov r1, #0
    strb r1, [r0, #0x1c]
    mov r1, #39
    strb r1, [r0, #0x8]
    b ov001_021ddf34_L308
ov001_021ddf34_L2ec:
    ldr r0, =0x022388ec
    mov r1, #1
    strb r1, [r0, #0x8]
    b ov001_021ddf34_L308
ov001_021ddf34_L2fc:
    ldr r0, =0x022388ec
    mov r1, #1
    strb r1, [r0, #0x8]
ov001_021ddf34_L308:
    mov r0, #1
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
