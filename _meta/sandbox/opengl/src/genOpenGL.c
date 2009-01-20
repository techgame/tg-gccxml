// Grab the externs first
#undef __gl_h_
#undef GL_GLEXT_FUNCTION_POINTERS
#define GL_GLEXT_LEGACY
#include <OpenGL/gl.h>

// Now start over and grab the function pointers
#undef __gl_h_
#define GL_GLEXT_FUNCTION_POINTERS
#define GL_GLEXT_LEGACY
#include <OpenGL/gl.h>

// Grab glu's types
#include <OpenGL/glu.h>

// Finally, grab the extensions
#define GL_GLEXT_PROTOTYPES
#include <OpenGL/glext.h>

