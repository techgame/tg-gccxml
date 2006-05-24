// This is a silly header file
//
//

#define A_STRING_DEF "a string value"
#define AN_INT_DEF 1234

#define A_MACRO(A_MARCO_ARG_1, A_MACRO_ARG_2) A_MACRO_ARG_1##A_MACRO_ARG_2

#ifdef WEIRD || LUMA

#define SHANE_A

#elif defined(LEEMA)

#define SHANE_B

#else

#define SHANE_C

typedef struct {
    int anInt;
    char* aString;
} AStruct;

#endif

void aFuncWithStruct(AStruct* aRef);

void aFuncWithInt(int anInt);

