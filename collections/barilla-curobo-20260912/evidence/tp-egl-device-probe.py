exec(open('/tmp/tp-egl-probe.py').read().split('d=x.eglGetDisplay')[0])
x.eglGetProcAddress.argtypes=[ctypes.c_char_p];x.eglGetProcAddress.restype=ctypes.c_void_p
query=ctypes.CFUNCTYPE(ctypes.c_uint,ctypes.c_int,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_int))(x.eglGetProcAddress(b'eglQueryDevicesEXT'))
platform=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_uint,ctypes.c_void_p,ctypes.c_void_p)(x.eglGetProcAddress(b'eglGetPlatformDisplayEXT'))
devices=(ctypes.c_void_p*16)();count=ctypes.c_int();print('query',query(16,devices,ctypes.byref(count)),'devices',count.value)
for i in range(count.value):
 d=platform(0x313F,devices[i],None);a,b=ctypes.c_int(),ctypes.c_int();ok=x.eglInitialize(d,ctypes.byref(a),ctypes.byref(b));print('device',i,'eglInitialize',ok,'error',hex(x.eglGetError()),'version',a.value,b.value,'vendor',x.eglQueryString(d,0x3053))
 if not ok: continue
 x.eglBindAPI.argtypes=[ctypes.c_uint];x.eglBindAPI.restype=ctypes.c_uint
 x.eglChooseConfig.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.POINTER(ctypes.c_int)];x.eglChooseConfig.restype=ctypes.c_uint
 x.eglCreateContext.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)];x.eglCreateContext.restype=ctypes.c_void_p
 x.eglMakeCurrent.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p];x.eglMakeCurrent.restype=ctypes.c_uint
 x.eglBindAPI(0x30A0)
 attrib=(ctypes.c_int*7)(0x3033,1,0x3040,4,0x3024,8,0x3038);cfg=ctypes.c_void_p();ncfg=ctypes.c_int()
 print('chooseConfig',x.eglChooseConfig(d,attrib,ctypes.byref(cfg),1,ctypes.byref(ncfg)),ncfg.value)
 attrs=(ctypes.c_int*3)(0x3098,2,0x3038);ctx=x.eglCreateContext(d,cfg,None,attrs);print('context',bool(ctx),'current',x.eglMakeCurrent(d,None,None,ctx))
 glstr=ctypes.CFUNCTYPE(ctypes.c_char_p,ctypes.c_uint)(x.eglGetProcAddress(b'glGetString'))
 print('GL_VENDOR',glstr(0x1F00),'GL_RENDERER',glstr(0x1F01),'GL_VERSION',glstr(0x1F02))
