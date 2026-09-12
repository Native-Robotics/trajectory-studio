import ctypes
x=ctypes.CDLL('libEGL.so.1')
x.eglGetDisplay.argtypes=[ctypes.c_void_p];x.eglGetDisplay.restype=ctypes.c_void_p
x.eglInitialize.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)];x.eglInitialize.restype=ctypes.c_uint
x.eglGetError.restype=ctypes.c_uint
x.eglQueryString.argtypes=[ctypes.c_void_p,ctypes.c_int];x.eglQueryString.restype=ctypes.c_char_p
d=x.eglGetDisplay(None);a,b=ctypes.c_int(),ctypes.c_int();ok=x.eglInitialize(d,ctypes.byref(a),ctypes.byref(b));print('eglInitialize',ok,'error',hex(x.eglGetError()),'version',a.value,b.value,'vendor',x.eglQueryString(d,0x3053))
