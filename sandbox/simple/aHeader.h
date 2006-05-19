// This is a silly header file
//
//

#define A_STRING_DEF "a string value"
#define AN_INT_DEF 1234

#ifdef STUPID

#elif FARGO

#elif LEEMA

#else
struct {
    int anInt;
    char* aString;
} AStruct;
#endif

void stupid(AStruct& aRef);

