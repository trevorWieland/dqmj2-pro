typedef unsigned char u8;
typedef unsigned int u32;
typedef short s16;
typedef struct Point { s16 x; s16 y; } Point;
typedef struct FieldObject { u8 reserved[0x7c]; u32 field7c; } FieldObject;
typedef struct LayoutState { u8 reserved[0x14]; Point position; u8 gap18[4]; void *group; u8 gap20[12]; u32 step; } LayoutState;
extern FieldObject *native_fn_0205f98c(void *, u8);
extern void native_fn_02048a60(FieldObject *, int, int);
extern int native_fn_0204b4b8(LayoutState *);
extern void native_fn_0204b53c(LayoutState *, const Point *);
extern void native_fn_0204b6dc(LayoutState *, const Point *);
extern void native_fn_0204b1c4(LayoutState *, u32, const Point *, u32, u32, u8);
extern void native_fn_0202a498(u32, void *);
typedef char PointSize[(sizeof(Point) == 4) ? 1 : -1];
typedef char GroupOffset[((u32)&((LayoutState *)0)->group == 0x1c) ? 1 : -1];
typedef char StepOffset[((u32)&((LayoutState *)0)->step == 0x2c) ? 1 : -1];
typedef char FlagOffset[((u32)&((FieldObject *)0)->field7c == 0x7c) ? 1 : -1];

typedef char StatePrefix[(sizeof(LayoutState) == 48) ? 1 : -1];
typedef char PositionOffset[((u32)&((LayoutState *)0)->position == 20) ? 1 : -1];
typedef char SignedFieldWidth[(sizeof(s16) == 2) ? 1 : -1];
typedef char PointerWidth[(sizeof(void *) == 4) ? 1 : -1];

typedef char SignedHalfword[((s16)-1 < 0) ? 1 : -1];
typedef char ChildPrefix[(sizeof(FieldObject) == 128) ? 1 : -1];
