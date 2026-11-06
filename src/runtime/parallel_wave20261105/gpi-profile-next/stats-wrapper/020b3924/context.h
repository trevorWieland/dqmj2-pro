typedef unsigned int u32;typedef struct bucketset_s*bucketset_t;typedef enum{bt_int,bt_float,bt_string}BucketType;typedef void*(*BucketFunc)(bucketset_t,char*,void*);
typedef struct statsgame_s{int connid,sesskey,usebuckets;bucketset_t buckets;char challenge[9];void*playernums,*teamnums;int totalplayers,totalteams;u32 sttime;}*statsgame_t;
#define NULL ((void*)0)
#define GSI_UNUSED(x) ((void)(x))
#define FIXGAME(g,r) if(g==NULL)g=g_statsgame;if(g==NULL)return r;
#define DoFunc(f,g,n,v,t,r) if(g==NULL)g=g_statsgame;if(!g)r=v;else{r=f(g->buckets,n,v);if(!r)r=BucketNew(g->buckets,n,t,v);}
#define MULTIPLIER -1664117991
typedef struct{unsigned char opaque[12];statsgame_t game;}StatsGlobalsView;
extern StatsGlobalsView native_data_021d2514;
#define g_statsgame native_data_021d2514.game
void*native_fn_020a8644(void*,int);void*native_fn_020b2ce8(bucketset_t,char*,BucketType,void*);int native_fn_0200616c(char*,const char*,...);
int native_fn_020b3700(statsgame_t,int);int native_fn_020b3720(statsgame_t,int);int native_fn_020b3740(statsgame_t,char*,BucketFunc,int,int);double native_fn_020b3780(statsgame_t,char*,BucketFunc,double,int);char*native_fn_020b37c4(statsgame_t,char*,BucketFunc,char*,int);
#define ArrayNth native_fn_020a8644
#define BucketNew native_fn_020b2ce8
#define sprintf native_fn_0200616c
#define GetTeamIndex native_fn_020b3700
#define GetPlayerIndex native_fn_020b3720
#define ServerOpInt native_fn_020b3740
#define ServerOpFloat native_fn_020b3780
#define ServerOpString native_fn_020b37c4
extern const char native_data_020e16d8[],native_data_020e16e0[];
