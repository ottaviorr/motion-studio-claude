// motion-design · shaders WebGL como função do tempo (seek-safe: o mesmo t desenha sempre o mesmo quadro).
// Uso numa cena:  <canvas id="fx" class="shader"></canvas>  →  const FX = SHADER($('fx'), 'liquido', {cores:[...]});  e no frame(t): FX(t, {...})
// queima modo 0 = cobre com tinta (k 0→1 revela) · modo 1 = só máscara (alfa = parte revelada, para mask-image) · modo 2 = só a borda que brilha
// Efeitos: 'liquido' (fundo de tinta que flui) · 'queima' (entrada/saída: dissolve com borda que brilha) ·
//          'vazamento' (light leak que atravessa) · 'halftone' (campo de pontos que respira).
// Cores em hex. preserveDrawingBuffer: true — senão a captura quadro a quadro pega o canvas vazio.
(function () {
  const NOISE = `
  vec3 mod289(vec3 x){return x-floor(x*(1./289.))*289.;} vec2 mod289(vec2 x){return x-floor(x*(1./289.))*289.;}
  vec3 permute(vec3 x){return mod289(((x*34.)+1.)*x);}
  float snoise(vec2 v){const vec4 C=vec4(.211324865405187,.366025403784439,-.577350269189626,.024390243902439);
    vec2 i=floor(v+dot(v,C.yy)); vec2 x0=v-i+dot(i,C.xx); vec2 i1=(x0.x>x0.y)?vec2(1.,0.):vec2(0.,1.);
    vec4 x12=x0.xyxy+C.xxzz; x12.xy-=i1; i=mod289(i);
    vec3 p=permute(permute(i.y+vec3(0.,i1.y,1.))+i.x+vec3(0.,i1.x,1.));
    vec3 m=max(.5-vec3(dot(x0,x0),dot(x12.xy,x12.xy),dot(x12.zw,x12.zw)),0.); m=m*m; m=m*m;
    vec3 x=2.*fract(p*C.www)-1.; vec3 h=abs(x)-.5; vec3 ox=floor(x+.5); vec3 a0=x-ox;
    m*=1.79284291400159-.85373472095314*(a0*a0+h*h);
    vec3 g; g.x=a0.x*x0.x+h.x*x0.y; g.yz=a0.yz*x12.xz+h.yz*x12.yw; return 130.*dot(m,g);}
  float fbm(vec2 p){float f=0.,a=.5; for(int i=0;i<5;i++){f+=a*snoise(p); p*=2.02; a*=.5;} return f;}`;
  const FS = {
    // tinta que flui: domain warping em 2 níveis, 3 cores + brilho
    liquido: `uniform vec3 c0,c1,c2,c3; uniform float vel,brilho;
      void main(){vec2 uv=gl_FragCoord.xy/res; vec2 p=uv*vec2(res.x/res.y,1.)*.55; float t=T*vel;
        vec2 q=vec2(fbm(p+vec2(0.,t*.07)),fbm(p+vec2(5.2,1.3)-t*.06));
        vec2 r=vec2(fbm(p+2.*q+vec2(1.7,9.2)+t*.08),fbm(p+2.*q+vec2(8.3,2.8)-t*.07));
        float onda=sin((p.x*.9+p.y*1.4)*2.6+1.5*r.x+.8*q.y+t*.45)*.5+.5;
        vec3 col=mix(c0,c1,smoothstep(.15,.95,onda)*.85);
        col=mix(col,c2,pow(onda,5.)*.85*(.6+.4*q.x));
        col+=c3*pow(smoothstep(.985,1.,onda),2.)*brilho*.55;
        col*=.55+.6*smoothstep(1.25,.15,length((uv-vec2(.5,.5))*vec2(1.,1.2)));
        gl_FragColor=vec4(col,1.);}`,
    // dissolve por ruído: k 0→1 revela (alfa 0 onde já revelou); borda que brilha na cor 'borda'
    queima: `uniform vec3 c0,c1,borda; uniform float k,larg,modo;
      void main(){vec2 uv=gl_FragCoord.xy/res; vec2 p=uv*vec2(res.x/res.y,1.)*2.2;
        float n=fbm(p*.8+vec2(T*.05,0.))*.5+.5; n=mix(n,uv.x*.9+uv.y*.1,.6); float lim=k*1.3-.15;
        float a=smoothstep(lim-.02,lim+.02,n); float e=smoothstep(larg,0.,abs(n-lim))*step(.001,k)*step(k,.999);
        vec3 col=mix(c0,c1,n); col=mix(col,borda,e);
        if(modo>1.5) gl_FragColor=vec4(mix(borda,vec3(1.),e*e*.35),e); else if(modo>.5) gl_FragColor=vec4(1.,1.,1.,1.-a); else gl_FragColor=vec4(col*max(a,e)+borda*e*.6,max(a,e));}`,
    // light leak: mancha quente que atravessa em diagonal (aditiva, alfa = intensidade)
    vazamento: `uniform vec3 c0,c1; uniform float k,forca;
      void main(){vec2 uv=gl_FragCoord.xy/res; vec2 p=uv*vec2(res.x/res.y,1.); float x=mix(-.6,2.4,k);
        float d=length((p-vec2(x,.35+.25*sin(k*3.)))*vec2(.7,1.4)); float n=fbm(p*2.+k*2.)*.5+.5;
        float i=exp(-d*d*2.2)*(.6+.6*n)*forca*sin(3.14159*k); vec3 col=mix(c0,c1,clamp(uv.y+n*.4,0.,1.));
        gl_FragColor=vec4(col*i,i);}`,
    // halftone: pontos cujo tamanho segue um campo de ruído que flui
    halftone: `uniform vec3 c0,c1; uniform float celula,forca; // celula em px de CSS (multiplicada pelo dpr no JS)
      void main(){vec2 g=gl_FragCoord.xy/celula; vec2 id=floor(g), f=fract(g)-.5; vec2 p=id*celula/res.y;
        float n=fbm(p*1.6+vec2(T*.08,T*.05))*.5+.5; float r=.5*pow(n,1.6)*forca;
        float dot_=smoothstep(r,r-.08,length(f)); gl_FragColor=vec4(mix(c0,c1,n)*dot_,dot_*n);}`,
  };
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
  window.SHADER = function (cv, tipo, base = {}) {
    // base.escala < 1: o shader calcula menos pixels e o navegador amplia (fundo suave não perde nada; .5 = 4× mais rápido)
    const dpr = (window.devicePixelRatio || 1) * (base.escala || 1), W = cv.width = Math.round((cv.clientWidth || 1920) * dpr), H = cv.height = Math.round((cv.clientHeight || 1080) * dpr);
    const gl = cv.getContext('webgl', { preserveDrawingBuffer: true, premultipliedAlpha: false, alpha: true, antialias: false });
    if (!gl) { console.warn('sem WebGL'); return () => {}; }
    const sh = (t, src) => { const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
    const pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}'));
    gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, 'precision highp float;uniform vec2 res;uniform float T;' + NOISE + FS[tipo]));
    gl.linkProgram(pr); gl.useProgram(pr);
    const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(pr, 'a'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.uniform2f(gl.getUniformLocation(pr, 'res'), W, H);
    return function (t, o = {}) {
      const u = { ...base, ...o };
      gl.uniform1f(gl.getUniformLocation(pr, 'T'), t);
      if (u.celula) u.celula *= dpr;
      for (const [k, v] of Object.entries(u)) {
        const l = gl.getUniformLocation(pr, k); if (!l) continue;
        if (typeof v === 'string') gl.uniform3fv(l, hex(v)); else gl.uniform1f(l, v);
      }
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    };
  };
})();
