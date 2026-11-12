/* ov001 row 0x02226764: 1144 bytes.
 *
 * What it does: 286 instructions; 52 call(s) to 0x02225414, 0x02225414, 0x02225414, +49 more; loops (back edge at +0xd8); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: block load (286 instructions, 52 calls, 44 branches, 52 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0xcc
 *   branch +0x1c -> +0xe0
 *   branch +0x20 -> +0xf4
 *   branch +0x24 -> +0x108
 *   branch +0x28 -> +0x11c
 *   branch +0x2c -> +0x130
 *   branch +0x30 -> +0x140
 *   branch +0x34 -> +0x150
 *   branch +0x38 -> +0x18c
 *   branch +0x3c -> +0x1a0
 *   branch +0x40 -> +0x1b4
 *   branch +0x44 -> +0x1c8
 *   branch +0x48 -> +0x1dc
 *   branch +0x4c -> +0x1f0
 *   branch +0x50 -> +0x204
 *   branch +0x54 -> +0x218
 *   branch +0x58 -> +0x27c
 *   branch +0x5c -> +0x290
 *   branch +0x60 -> +0x2a4
 *   branch +0x64 -> +0x2b8
 *   branch +0x68 -> +0x2e4
 *   branch +0x6c -> +0x2f0
 *   branch +0x70 -> +0x2fc
 *   branch +0x74 -> +0x308
 *   branch +0x78 -> +0x314
 *   branch +0x7c -> +0x320
 *   branch +0x80 -> +0x334
 *   branch +0x84 -> +0x348
 *   branch +0x88 -> +0x35c
 *   branch +0x8c -> +0x370
 *   branch +0x90 -> +0x384
 *   branch +0x94 -> +0x398
 *   branch +0x98 -> +0x3ac
 *   branch +0x9c -> +0x3c0
 *   branch +0xa0 -> +0x3cc
 *   branch +0xa4 -> +0x3dc
 *   branch +0xa8 -> +0x3ec
 *   branch +0xac -> +0x3fc
 *   branch +0xb4 -> +0x410
 *   branch +0xb8 -> +0x420
 *   branch +0xbc -> +0x434
 *   branch +0xc0 -> +0x444
 *   branch +0xc4 -> +0x450
 *   branch +0xc8 -> +0x464
 *   test +0x0c cmp r2, #44
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02226764; the literal pool and
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

extern void native_fn_02225414(void);
extern void native_fn_0222602c(void);
extern void native_fn_0207afec(void);
extern void native_fn_02225600(void);
extern void native_fn_02225854(void);
extern void native_fn_022249f8(void);
extern void native_fn_02224e40(void);
extern void native_fn_02224ed0(void);
extern void native_fn_022260bc(void);
extern void native_fn_022254a4(void);
extern void native_fn_02226190(void);
extern void native_fn_02225c64(void);
extern void native_fn_022242bc(void);
extern void native_fn_02224350(void);
extern void native_fn_02224ba4(void);
extern void native_fn_02226290(void);


asm u32 native_ov001_02226764 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldmia r1, {r3, r4, r5}
    mov r7, r0
    cmp r2, #44
    addls pc, pc, r2, lsl #2
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    b ov001_02226764_Lcc
    b ov001_02226764_Le0
    b ov001_02226764_Lf4
    b ov001_02226764_L108
    b ov001_02226764_L11c
    b ov001_02226764_L130
    b ov001_02226764_L140
    b ov001_02226764_L150
    b ov001_02226764_L18c
    b ov001_02226764_L1a0
    b ov001_02226764_L1b4
    b ov001_02226764_L1c8
    b ov001_02226764_L1dc
    b ov001_02226764_L1f0
    b ov001_02226764_L204
    b ov001_02226764_L218
    b ov001_02226764_L27c
    b ov001_02226764_L290
    b ov001_02226764_L2a4
    b ov001_02226764_L2b8
    b ov001_02226764_L2e4
    b ov001_02226764_L2f0
    b ov001_02226764_L2fc
    b ov001_02226764_L308
    b ov001_02226764_L314
    b ov001_02226764_L320
    b ov001_02226764_L334
    b ov001_02226764_L348
    b ov001_02226764_L35c
    b ov001_02226764_L370
    b ov001_02226764_L384
    b ov001_02226764_L398
    b ov001_02226764_L3ac
    b ov001_02226764_L3c0
    b ov001_02226764_L3cc
    b ov001_02226764_L3dc
    b ov001_02226764_L3ec
    b ov001_02226764_L3fc
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    b ov001_02226764_L410
    b ov001_02226764_L420
    b ov001_02226764_L434
    b ov001_02226764_L444
    b ov001_02226764_L450
    b ov001_02226764_L464
ov001_02226764_Lcc:
    mov r1, r4
    mov r2, #32
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_Le0:
    mov r1, r4
    mov r2, #25
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_Lf4:
    mov r1, r4
    mov r2, #33
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L108:
    mov r1, r4
    mov r2, #28
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L11c:
    mov r1, r4
    mov r2, #39
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L130:
    mov r1, r4
    mov r2, #149
    bl native_fn_0222602c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L140:
    mov r1, r4
    mov r2, #1
    bl native_fn_0222602c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L150:
    mov r1, r4
    mov r2, #19
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #20
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #21
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L18c:
    mov r1, r4
    mov r2, #16
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L1a0:
    mov r1, r4
    mov r2, #18
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L1b4:
    mov r1, r4
    mov r2, #17
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L1c8:
    mov r1, r4
    mov r2, #24
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L1dc:
    mov r1, r4
    mov r2, #44
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L1f0:
    mov r1, r4
    mov r2, #9
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L204:
    mov r1, r4
    mov r2, #10
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L218:
    mov r1, r4
    mov r2, #12
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #13
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #14
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #15
    mov r3, #1
    bl native_fn_02225414
    mov r0, r7
    mov r1, r4
    mov r2, #34
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L27c:
    mov r1, r4
    mov r2, #11
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L290:
    mov r1, r4
    mov r2, #6
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L2a4:
    mov r1, r4
    mov r2, #6
    mov r3, #2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L2b8:
    mov r0, r5
    bl native_fn_0207afec
    ldrb r6, [r0, #0x1f]
    mov r0, r5
    bl native_fn_0207afec
    ldrb r3, [r0, #0x20]
    mov r0, r7
    mov r1, r4
    mov r2, r6
    bl native_fn_02225600
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L2e4:
    mov r1, r4
    bl native_fn_02225854
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L2f0:
    mov r1, r4
    bl native_fn_022249f8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L2fc:
    mov r1, r4
    bl native_fn_02224e40
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L308:
    mov r1, r4
    bl native_fn_02224ed0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L314:
    mov r1, r4
    bl native_fn_022260bc
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L320:
    mov r1, r4
    mov r2, #1
    mov r3, #2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L334:
    mov r2, #1
    mov r1, r4
    sub r3, r2, #3
    bl native_fn_022254a4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L348:
    mov r2, #2
    mov r1, r4
    mov r3, r2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L35c:
    mov r2, #2
    mov r1, r4
    sub r3, r2, #4
    bl native_fn_022254a4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L370:
    mov r1, r4
    mov r2, #3
    mov r3, #2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L384:
    mov r2, #3
    mov r1, r4
    sub r3, r2, #5
    bl native_fn_022254a4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L398:
    mov r1, r4
    mov r2, #4
    mov r3, #2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3ac:
    mov r2, #4
    mov r1, r4
    sub r3, r2, #6
    bl native_fn_022254a4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3c0:
    mov r1, r4
    bl native_fn_02226190
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3cc:
    mov r1, r4
    mov r2, #2
    bl native_fn_02225c64
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3dc:
    mov r1, r4
    mov r2, #8
    bl native_fn_02225c64
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3ec:
    mov r1, r4
    mov r2, #4
    bl native_fn_02225c64
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L3fc:
    mov r1, r4
    mov r2, #5
    mov r3, #2
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L410:
    mov r1, r3
    mov r2, r4
    bl native_fn_022242bc
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L420:
    mov r1, r3
    mov r2, r4
    mov r3, r5
    bl native_fn_02224350
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L434:
    mov r1, r3
    mov r2, r4
    bl native_fn_02224ba4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L444:
    mov r1, r4
    bl native_fn_02226290
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L450:
    mov r1, r4
    mov r2, #40
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02226764_L464:
    mov r1, r4
    mov r2, #41
    mov r3, #1
    bl native_fn_02225414
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
