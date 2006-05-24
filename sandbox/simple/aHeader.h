// This is a silly header file
//
//

#define A_STRING_DEF "a string value"
#define AN_INT_DEF 1234

#define A_MACRO(A_MARCO_ARG_1, A_MACRO_ARG_2) A_MACRO_ARG_1##A_MACRO_ARG_2

#ifdef STUPID

#elif FARGO \
    || FUMA

#elif LEEMA

#else
struct {
    int anInt;
    char* aString;
} AStruct;
#endif

void stupid(AStruct& aRef);

